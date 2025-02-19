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
            lebenspunkte INT NOT NULL DEFAULT 10,
            angriff INT NOT NULL DEFAULT 0,
            verteidigung INT NOT NULL DEFAULT 0,
            ausdauer INT NOT NULL DEFAULT 0,
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
        "lebenspunkte": "INT NOT NULL DEFAULT 10",
        "angriff": "INT NOT NULL DEFAULT 0",
        "verteidigung": "INT NOT NULL DEFAULT 0",
        "ausdauer": "INT NOT NULL DEFAULT 0"
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
    elif command == 'check_fight_status':
        return check_fight_status(request)
    elif command == 'cancel_fight':
        return cancel_fight(request)
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
    "lebenspunkte": 10,
    "angriff": 10,
    "verteidigung": 10,
    "ausdauer": 10
}

def recruit_gladiator(request):
    user_id = request.get('user_id')
    name = request.get('name')
    chosen_type = request.get('type')
    
    if chosen_type not in gladiator_types.gladiator_types:
        return {'status': 'error', 'message': 'Ungültiger Gladiator-Typ'}
    
    g_type = gladiator_types.gladiator_types[chosen_type]
    final_stats = BASE_STATS.copy()
    
    # Wende die Modifikatoren an
    for stat, mod in g_type.modifiers.items():
        if stat in final_stats:
            final_stats[stat] += mod

    cursor.execute('''
        INSERT INTO gladiators (user_id, name, gladiator_type, lebenspunkte, angriff, verteidigung, ausdauer)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    ''', (
        user_id,
        name,
        chosen_type,
        final_stats["lebenspunkte"],
        final_stats["angriff"],
        final_stats["verteidigung"],
        final_stats["ausdauer"]
    ))
    db.commit()
    
    return {
        'status': 'success',
        'message': f'Gladiator {name} ({chosen_type}) wurde rekrutiert',
        'gladiator': {
            'name': name,
            'gladiator_type': chosen_type,
            'lebenspunkte': final_stats["lebenspunkte"],
            'angriff': final_stats["angriff"],
            'verteidigung': final_stats["verteidigung"],
            'ausdauer': final_stats["ausdauer"],
            'staerken': g_type.strengths,
            'schwaechen': g_type.weaknesses
        }
    }

def get_gladiators(request):
    user_id = request.get('user_id')
    cursor.execute("SELECT id, name, gladiator_type, lebenspunkte, angriff, verteidigung, ausdauer FROM gladiators WHERE user_id=%s", (user_id,))
    gladiators = cursor.fetchall()
    gladiator_list = []
    for g in gladiators:
        gladiator_list.append({
            'id': g[0],
            'name': g[1],
            'gladiator_type': g[2],
            'lebenspunkte': g[3],
            'angriff': g[4],
            'verteidigung': g[5],
            'ausdauer': g[6]
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
    
    # Prüfe, ob der Gladiator existiert und dem Benutzer gehört
    cursor.execute("""
        SELECT id, name, gladiator_type, lebenspunkte, angriff, verteidigung, ausdauer 
        FROM gladiators 
        WHERE id=%s AND user_id=%s
    """, (gladiator_id, user_id))
    gladiator = cursor.fetchone()
    
    if not gladiator:
        return {'status': 'error', 'message': 'Gladiator nicht gefunden oder gehört nicht dir'}
    
    # Erstelle ein Spieler-Objekt mit allen relevanten Informationen
    player = {
        'user_id': user_id,
        'gladiator_id': gladiator_id,
        'gladiator_name': gladiator[1],
        'gladiator_type': gladiator[2],
        'lebenspunkte': gladiator[3],
        'angriff': gladiator[4],
        'verteidigung': gladiator[5],
        'ausdauer': gladiator[6]
    }
    
    # Prüfe zuerst, ob bereits ein Kampfergebnis vorliegt
    if str(gladiator_id) in current_fight_results:
        result = current_fight_results[str(gladiator_id)]
        del current_fight_results[str(gladiator_id)]
        return result
    
    # Füge den Spieler zur Warteliste hinzu
    waiting_players.append(player)
    
    # Wenn zwei Spieler warten, starte den Kampf
    if len(waiting_players) >= 2:
        player1 = waiting_players.pop(0)
        player2 = waiting_players.pop(0)
        fight_result = simulate_fight(player1, player2)
        
        # Speichere das Kampfergebnis in einer globalen Variable
        global current_fight_results
        current_fight_results = {
            str(player1['gladiator_id']): fight_result,
            str(player2['gladiator_id']): fight_result
        }
        
        # Lösche das Ergebnis für den aktuellen Spieler
        if str(gladiator_id) in current_fight_results:
            result = current_fight_results[str(gladiator_id)]
            del current_fight_results[str(gladiator_id)]
            return result
    
    return {
        'status': 'waiting',
        'message': 'Warte auf einen Gegner...',
        'gladiator': player
    }

def check_fight_status(request):
    gladiator_id = request.get('gladiator_id')
    
    # Prüfe zuerst, ob ein Kampfergebnis vorliegt
    if str(gladiator_id) in current_fight_results:
        result = current_fight_results[str(gladiator_id)]
        # Lösche das Ergebnis nach dem Abrufen
        del current_fight_results[str(gladiator_id)]
        return result
    
    # Suche nach einem laufenden Kampf mit diesem Gladiator
    for player in waiting_players:
        if player['gladiator_id'] == gladiator_id:
            return {'status': 'waiting'}
    
    return {'status': 'error', 'message': 'Gladiator nicht in der Warteschlange'}

# Globale Variable für Kampfergebnisse
current_fight_results = {}

def simulate_fight(player1, player2):
    # Kampfprotokoll für detaillierte Ausgabe
    fight_log = []
    
    # Initialisiere aktuelle Werte für den Kampf
    p1_current = {
        'lebenspunkte': player1['lebenspunkte'],
        'ausdauer': player1['ausdauer']
    }
    p2_current = {
        'lebenspunkte': player2['lebenspunkte'],
        'ausdauer': player2['ausdauer']
    }
    
    # Kampfrunde
    while p1_current['lebenspunkte'] > 0 and p2_current['lebenspunkte'] > 0:
        # Spieler 1 greift an
        attack_roll = random.randint(1, 20)
        defense_roll = random.randint(1, 20)
        
        # Berechne Angriffswert (mit Ausdauer-Malus)
        attack_value = attack_roll + player1['angriff']
        if p1_current['ausdauer'] <= 0:
            attack_value -= 5
            fight_log.append(f"{player1['gladiator_name']} ist erschöpft (-5 auf Angriff)")
        
        # Berechne Verteidigungswert
        defense_value = defense_roll + player2['verteidigung']
        
        fight_log.append(f"{player1['gladiator_name']} greift an: {attack_roll}+{player1['angriff']} = {attack_value}")
        fight_log.append(f"{player2['gladiator_name']} verteidigt: {defense_roll}+{player2['verteidigung']} = {defense_value}")
        
        # Reduziere Ausdauer des Angreifers
        p1_current['ausdauer'] -= 1
        
        # Berechne Schaden
        if attack_value > defense_value:
            damage = attack_value - defense_value
            p2_current['lebenspunkte'] -= damage
            fight_log.append(f"Treffer! {player2['gladiator_name']} verliert {damage} Lebenspunkte")
        else:
            fight_log.append("Verteidigung erfolgreich!")
        
        # Wenn Spieler 2 noch lebt, kontert er
        if p2_current['lebenspunkte'] > 0:
            attack_roll = random.randint(1, 20)
            defense_roll = random.randint(1, 20)
            
            # Berechne Angriffswert (mit Ausdauer-Malus)
            attack_value = attack_roll + player2['angriff']
            if p2_current['ausdauer'] <= 0:
                attack_value -= 5
                fight_log.append(f"{player2['gladiator_name']} ist erschöpft (-5 auf Angriff)")
            
            # Berechne Verteidigungswert
            defense_value = defense_roll + player1['verteidigung']
            
            fight_log.append(f"{player2['gladiator_name']} greift an: {attack_roll}+{player2['angriff']} = {attack_value}")
            fight_log.append(f"{player1['gladiator_name']} verteidigt: {defense_roll}+{player1['verteidigung']} = {defense_value}")
            
            # Reduziere Ausdauer des Angreifers
            p2_current['ausdauer'] -= 1
            
            # Berechne Schaden
            if attack_value > defense_value:
                damage = attack_value - defense_value
                p1_current['lebenspunkte'] -= damage
                fight_log.append(f"Treffer! {player1['gladiator_name']} verliert {damage} Lebenspunkte")
            else:
                fight_log.append("Verteidigung erfolgreich!")
        
        fight_log.append(f"\nStatus nach der Runde:")
        fight_log.append(f"{player1['gladiator_name']}: LP={p1_current['lebenspunkte']}, AUS={p1_current['ausdauer']}")
        fight_log.append(f"{player2['gladiator_name']}: LP={p2_current['lebenspunkte']}, AUS={p2_current['ausdauer']}\n")
    
    # Bestimme den Gewinner
    winner = player1 if p1_current['lebenspunkte'] > 0 else player2
    loser = player2 if p1_current['lebenspunkte'] > 0 else player1
    
    # Aktualisiere die Gladiatoren in der Datenbank
    cursor.execute("""
        UPDATE gladiators 
        SET lebenspunkte = %s, ausdauer = %s 
        WHERE id = %s
    """, (p1_current['lebenspunkte'], p1_current['ausdauer'], player1['gladiator_id']))
    
    cursor.execute("""
        UPDATE gladiators 
        SET lebenspunkte = %s, ausdauer = %s 
        WHERE id = %s
    """, (p2_current['lebenspunkte'], p2_current['ausdauer'], player2['gladiator_id']))
    
    db.commit()
    
    return {
        'status': 'success',
        'message': f"Kampf beendet! {winner['gladiator_name']} hat gewonnen!",
        'winner': winner,
        'loser': loser,
        'fight_log': fight_log
    }

def cancel_fight(request):
    gladiator_id = request.get('gladiator_id')
    
    # Entferne den Spieler aus der Warteschlange
    for i, player in enumerate(waiting_players):
        if player['gladiator_id'] == gladiator_id:
            waiting_players.pop(i)
            # Lösche auch eventuell vorhandene Kampfergebnisse
            if str(gladiator_id) in current_fight_results:
                del current_fight_results[str(gladiator_id)]
            return {'status': 'success', 'message': 'Kampf abgebrochen'}
    
    return {'status': 'error', 'message': 'Gladiator nicht in der Warteschlange'}

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