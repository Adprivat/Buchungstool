#!/usr/bin/env python3
import socket
import threading
import json
import random
import mysql.connector
import gladiator_types  # Enthält die Definitionen der Gladiator-Typen
from config import db_config, server_config

# Verbindung zur MySQL-Datenbank herstellen
db = mysql.connector.connect(**db_config)
cursor = db.cursor()

def setup_database():
    # Tabelle für Nutzer erstellen
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            currency INT DEFAULT 1000
        )
    ''')
    # Tabelle für Gladiatoren erstellen – verwende "gladiator_type" statt "type"
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gladiators (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            name VARCHAR(255),
            gladiator_type VARCHAR(50),
            lp INT,
            agilitaet INT,
            konstitution INT,
            staerke INT,
            ausdauer INT,
            praezision INT,
            grundruestung INT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    db.commit()
    # Falls sich die Tabellendefinition geändert hat, werden fehlende Spalten ergänzt
    ensure_gladiator_table_columns()

def ensure_gladiator_table_columns():
    """
    Prüft, ob alle erwarteten Spalten in der Tabelle 'gladiators' vorhanden sind.
    Falls nicht, werden sie mittels ALTER TABLE hinzugefügt.
    """
    expected_columns = {
        "gladiator_type": "VARCHAR(50)",
        "lp": "INT NOT NULL DEFAULT 100",
        "agilitaet": "INT NOT NULL DEFAULT 10",
        "konstitution": "INT NOT NULL DEFAULT 10",
        "staerke": "INT NOT NULL DEFAULT 10",
        "ausdauer": "INT NOT NULL DEFAULT 10",
        "praezision": "INT NOT NULL DEFAULT 10",
        "grundruestung": "INT NOT NULL DEFAULT 0"
    }
    for column, definition in expected_columns.items():
        cursor.execute("SHOW COLUMNS FROM gladiators LIKE %s", (column,))
        if cursor.fetchone() is None:
            print(f"Spalte '{column}' fehlt. Füge hinzu...")
            alter_stmt = f"ALTER TABLE gladiators ADD COLUMN {column} {definition}"
            cursor.execute(alter_stmt)
    db.commit()

setup_database()

# Liste wartender Spieler für den Kampf
waiting_players = []

def handle_client(client_socket):
    try:
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            try:
                request = json.loads(data.decode())
            except json.JSONDecodeError:
                client_socket.sendall(json.dumps({'status': 'error', 'message': 'Ungültiges JSON-Format'}).encode())
                continue
            response = process_request(request)
            client_socket.sendall(json.dumps(response).encode())
    except Exception as e:
        print("Fehler im Client-Thread:", e)
    finally:
        client_socket.close()

def process_request(request):
    command = request.get('command')
    if command == 'register':
        return register_user(request)
    elif command == 'login':
        return login_user(request)
    elif command == 'recruit_gladiator':
        return recruit_gladiator(request)
    elif command == 'place_bet':
        return place_bet(request)
    elif command == 'join_fight':
        return join_fight(request)
    elif command == 'get_gladiators':
        return get_gladiators(request)
    else:
        return {'status': 'error', 'message': 'Unbekannter Befehl'}

def register_user(request):
    username = request.get('username')
    password = request.get('password')
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        db.commit()
        return {'status': 'success', 'message': 'Registrierung erfolgreich'}
    except mysql.connector.Error as err:
        return {'status': 'error', 'message': str(err)}

def login_user(request):
    username = request.get('username')
    password = request.get('password')
    cursor.execute("SELECT id, currency FROM users WHERE username=%s AND password=%s", (username, password))
    result = cursor.fetchone()
    if result:
        user_id, currency = result
        return {'status': 'success', 'user_id': user_id, 'currency': currency}
    else:
        return {'status': 'error', 'message': 'Ungültige Anmeldedaten'}

# Basiswerte für alle Gladiatoren (Standardwerte, die dann modifiziert werden)
BASE_STATS = {
    "lp": 100,
    "Agilität": 10,
    "Konstitution": 10,
    "Stärke": 10,
    "Ausdauer": 10,
    "Präzision": 10,
    "Grundrüstung": 0
}

def recruit_gladiator(request):
    user_id = request.get('user_id')
    name = request.get('name')
    chosen_type = request.get('type')  # Beispiel: "Retiarius"
    
    if chosen_type not in gladiator_types.gladiator_types:
        return {'status': 'error', 'message': 'Ungültiger Gladiator-Typ'}
    
    g_type = gladiator_types.gladiator_types[chosen_type]
    final_stats = BASE_STATS.copy()
    for stat, mod in g_type.modifiers.items():
        if stat in final_stats:
            final_stats[stat] += mod
        else:
            final_stats[stat] = mod

    cursor.execute('''
        INSERT INTO gladiators (user_id, name, gladiator_type, lp, agilitaet, konstitution, staerke, ausdauer, praezision, grundruestung)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (
        user_id,
        name,
        chosen_type,
        final_stats["lp"],
        final_stats["Agilität"],
        final_stats["Konstitution"],
        final_stats["Stärke"],
        final_stats["Ausdauer"],
        final_stats["Präzision"],
        final_stats["Grundrüstung"]
    ))
    db.commit()
    return {
        'status': 'success',
        'message': f'{chosen_type} {name} angeheuert',
        'gladiator': {
            'name': name,
            'type': chosen_type,
            'stats': final_stats,
            'special_ability': g_type.special_ability
        }
    }

def get_gladiators(request):
    user_id = request.get('user_id')
    cursor.execute("SELECT id, name, gladiator_type, lp, agilitaet, konstitution, staerke, ausdauer, praezision, grundruestung FROM gladiators WHERE user_id=%s", (user_id,))
    gladiators = cursor.fetchall()
    gladiator_list = []
    for g in gladiators:
        gladiator_list.append({
            'id': g[0],
            'name': g[1],
            'gladiator_type': g[2],
            'lp': g[3],
            'agilitaet': g[4],
            'konstitution': g[5],
            'staerke': g[6],
            'ausdauer': g[7],
            'praezision': g[8],
            'grundruestung': g[9]
        })
    return {'status': 'success', 'gladiators': gladiator_list}

def place_bet(request):
    user_id = request.get('user_id')
    amount = request.get('amount')
    cursor.execute("SELECT currency FROM users WHERE id=%s", (user_id,))
    result = cursor.fetchone()
    if result and result[0] >= amount:
        new_currency = result[0] - amount
        cursor.execute("UPDATE users SET currency=%s WHERE id=%s", (new_currency, user_id))
        db.commit()
        return {'status': 'success', 'message': f'Wette platziert, {amount} abgezogen'}
    else:
        return {'status': 'error', 'message': 'Nicht genügend Guthaben'}

def join_fight(request):
    user_id = request.get('user_id')
    gladiator_id = request.get('gladiator_id')
    bet_amount = request.get('bet_amount')
    cursor.execute("SELECT currency FROM users WHERE id=%s", (user_id,))
    result = cursor.fetchone()
    if result and result[0] >= bet_amount:
        new_currency = result[0] - bet_amount
        cursor.execute("UPDATE users SET currency=%s WHERE id=%s", (new_currency, user_id))
        db.commit()
        player = {'user_id': user_id, 'gladiator_id': gladiator_id, 'bet': bet_amount}
        waiting_players.append(player)
        if len(waiting_players) >= 2:
            player1 = waiting_players.pop(0)
            player2 = waiting_players.pop(0)
            return simulate_fight(player1, player2)
        else:
            return {'status': 'waiting', 'message': 'Warte auf einen weiteren Gegner'}
    else:
        return {'status': 'error', 'message': 'Nicht genügend Guthaben'}

def simulate_fight(player1, player2):
    cursor.execute("SELECT staerke, agilitaet FROM gladiators WHERE id=%s", (player1['gladiator_id'],))
    g1 = cursor.fetchone()
    cursor.execute("SELECT staerke, agilitaet FROM gladiators WHERE id=%s", (player2['gladiator_id'],))
    g2 = cursor.fetchone()
    if not g1 or not g2:
        return {'status': 'error', 'message': 'Gladiator nicht gefunden'}
    score1 = g1[0] * 0.6 + g1[1] * 0.4 + random.random() * 10
    score2 = g2[0] * 0.6 + g2[1] * 0.4 + random.random() * 10
    winner = player1 if score1 > score2 else player2
    total_pot = player1['bet'] + player2['bet']
    cursor.execute("SELECT currency FROM users WHERE id=%s", (winner['user_id'],))
    current = cursor.fetchone()[0]
    new_currency = current + total_pot
    cursor.execute("UPDATE users SET currency=%s WHERE id=%s", (new_currency, winner['user_id']))
    db.commit()
    return {'status': 'success', 'message': 'Kampf beendet', 'winner': winner['user_id'], 'pot': total_pot}

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_config['host'], server_config['port']))
    server.listen(5)
    print(f"Server gestartet auf {server_config['host']}:{server_config['port']}")
    try:
        while True:
            client_socket, addr = server.accept()
            print("Neue Verbindung von", addr)
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()
    except KeyboardInterrupt:
        print("\nServer wird beendet...")
    finally:
        server.close()

if __name__ == '__main__':
    start_server()