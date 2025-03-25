import sqlite3
import os
from datetime import datetime, timedelta

# Pfad zur Datenbank
DATABASE_FILE = "harmony_heaven.db"

def create_test_data():
    # Verbindung zur Datenbank herstellen
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    print("Erstelle Testdaten für Harmony Heaven Hotels...")
    
    # Tabellen erstellen, falls sie noch nicht existieren
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS rooms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        price_per_night REAL NOT NULL,
        capacity INTEGER NOT NULL,
        room_type TEXT,
        image_url TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        hashed_password TEXT,
        is_active INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        room_id INTEGER,
        check_in DATE NOT NULL,
        check_out DATE NOT NULL,
        adults INTEGER NOT NULL,
        children INTEGER DEFAULT 0,
        total_price REAL NOT NULL,
        status TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (room_id) REFERENCES rooms (id)
    )
    ''')
    
    # Prüfen, ob bereits Testdaten vorhanden sind
    cursor.execute("SELECT COUNT(*) FROM rooms")
    room_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM bookings")
    booking_count = cursor.fetchone()[0]
    
    # Beispiel-Zimmer einfügen, wenn noch keine vorhanden
    if room_count == 0:
        print("Füge Zimmerdaten hinzu...")
        rooms = [
            # Berlin
            ("Standard Zimmer Berlin", "Komfortables Zimmer mit Blick auf die Stadt", 199.0, 2, "standard", "/room-1.jpg"),
            ("Deluxe Zimmer Berlin", "Geräumiges Zimmer mit Kingsize-Bett", 249.0, 2, "deluxe", "/room-2.jpg"),
            ("Suite Berlin", "Luxuriöse Suite mit separatem Wohnbereich", 349.0, 4, "suite", "/room-3.jpg"),
            
            # München
            ("Standard Zimmer München", "Komfortables Zimmer im bayerischen Stil", 209.0, 2, "standard", "/room-1.jpg"),
            ("Deluxe Zimmer München", "Geräumiges Zimmer mit Blick auf die Alpen", 259.0, 2, "deluxe", "/room-2.jpg"),
            ("Suite München", "Luxuriöse Suite mit Whirlpool", 359.0, 4, "suite", "/room-3.jpg"),
            
            # Hamburg
            ("Standard Zimmer Hamburg", "Komfortables Zimmer mit Hafenblick", 219.0, 2, "standard", "/room-1.jpg"),
            ("Deluxe Zimmer Hamburg", "Geräumiges Zimmer mit Panoramablick", 269.0, 2, "deluxe", "/room-2.jpg"),
            ("Suite Hamburg", "Luxuriöse Suite mit Alsterblick", 369.0, 4, "suite", "/room-3.jpg"),
            
            # Frankfurt
            ("Standard Zimmer Frankfurt", "Komfortables Zimmer mit Skylineblick", 189.0, 2, "standard", "/room-1.jpg"),
            ("Deluxe Zimmer Frankfurt", "Geräumiges Zimmer mit Mainblick", 239.0, 2, "deluxe", "/room-2.jpg"),
            ("Suite Frankfurt", "Luxuriöse Suite im Bankenviertel", 339.0, 4, "suite", "/room-3.jpg"),
        ]
        
        cursor.executemany(
            "INSERT INTO rooms (name, description, price_per_night, capacity, room_type, image_url) VALUES (?, ?, ?, ?, ?, ?)",
            rooms
        )
        print(f"{len(rooms)} Zimmer wurden hinzugefügt.")
    else:
        print(f"{room_count} Zimmer sind bereits in der Datenbank vorhanden.")
    
    # Beispiel-Benutzer einfügen, wenn noch keine vorhanden
    if user_count == 0:
        print("Füge Benutzerdaten hinzu...")
        users = [
            ("Max", "Mustermann", "max.mustermann@example.com", "password123"),
            ("Maria", "Musterfrau", "maria.musterfrau@example.com", "password456"),
            ("John", "Doe", "john.doe@example.com", "password789"),
        ]
        
        cursor.executemany(
            "INSERT INTO users (first_name, last_name, email, hashed_password) VALUES (?, ?, ?, ?)",
            users
        )
        print(f"{len(users)} Benutzer wurden hinzugefügt.")
    else:
        print(f"{user_count} Benutzer sind bereits in der Datenbank vorhanden.")
    
    # Beispiel-Buchungen einfügen, wenn noch keine vorhanden
    if booking_count == 0:
        print("Füge Buchungsdaten hinzu...")
        
        # Aktuelle Datum und zukünftige Daten für Buchungen
        today = datetime.now().date()
        
        # Buchungen für verschiedene Zeiträume erstellen
        bookings = [
            # Buchung für nächste Woche
            (1, 2, (today + timedelta(days=7)).isoformat(), (today + timedelta(days=10)).isoformat(), 2, 0, 249.0 * 3, "confirmed"),
            # Buchung für übernächste Woche
            (2, 5, (today + timedelta(days=14)).isoformat(), (today + timedelta(days=18)).isoformat(), 2, 1, 259.0 * 4, "confirmed"),
            # Buchung für den aktuellen Monat
            (3, 8, (today + timedelta(days=21)).isoformat(), (today + timedelta(days=25)).isoformat(), 2, 0, 269.0 * 4, "confirmed"),
            # Vergangene Buchung
            (1, 3, (today - timedelta(days=10)).isoformat(), (today - timedelta(days=5)).isoformat(), 3, 1, 349.0 * 5, "completed"),
            # Stornierte Buchung
            (2, 6, (today + timedelta(days=30)).isoformat(), (today + timedelta(days=35)).isoformat(), 2, 2, 359.0 * 5, "cancelled"),
        ]
        
        cursor.executemany(
            "INSERT INTO bookings (user_id, room_id, check_in, check_out, adults, children, total_price, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            bookings
        )
        print(f"{len(bookings)} Buchungen wurden hinzugefügt.")
    else:
        print(f"{booking_count} Buchungen sind bereits in der Datenbank vorhanden.")
    
    # Änderungen speichern und Verbindung schließen
    conn.commit()
    conn.close()
    
    print("Testdaten wurden erfolgreich erstellt!")

if __name__ == "__main__":
    create_test_data()