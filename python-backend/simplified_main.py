from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel
import sqlite3
import os
import jwt

# JWT-Konfiguration
SECRET_KEY = "IhrGeheimesPasswort"  # In Produktion sicherer speichern!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Stellen Sie sicher, dass das Verzeichnis existiert
os.makedirs(os.path.dirname(os.path.abspath(__file__)), exist_ok=True)

# SQLite-Datenbankverbindung
DATABASE_FILE = "harmony_heaven.db"

app = FastAPI(title="Harmony Heaven Hotels API - Simplified Version")

# CORS-Konfiguration für die Kommunikation mit dem Next.js-Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend-URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth2 Bearer Token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# Modelle für Anfragen und Antworten
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class BookingCheck(BaseModel):
    hotel_id: Optional[str] = None
    check_in: str
    check_out: str
    adults: int
    children: int
    rooms: int

class BookingCheckResponse(BaseModel):
    available_rooms: int
    price_per_night: float

# Hilfsfunktionen für die Datenbankverbindung
def get_db_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Tabellen erstellen
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
    
    # Beispielzimmer einfügen, wenn noch keine vorhanden
    cursor.execute("SELECT COUNT(*) FROM rooms")
    if cursor.fetchone()[0] == 0:
        rooms = [
            ("Standard Zimmer Berlin", "Komfortables Zimmer mit Blick auf die Stadt", 199.0, 2, "standard", "/room-1.jpg"),
            ("Deluxe Zimmer Berlin", "Geräumiges Zimmer mit Kingsize-Bett", 249.0, 2, "deluxe", "/room-2.jpg"),
            ("Suite Berlin", "Luxuriöse Suite mit separatem Wohnbereich", 349.0, 4, "suite", "/room-3.jpg"),
            ("Standard Zimmer München", "Komfortables Zimmer im bayerischen Stil", 209.0, 2, "standard", "/room-1.jpg"),
            ("Deluxe Zimmer München", "Geräumiges Zimmer mit Blick auf die Alpen", 259.0, 2, "deluxe", "/room-2.jpg"),
            ("Suite München", "Luxuriöse Suite mit Whirlpool", 359.0, 4, "suite", "/room-3.jpg"),
        ]
        cursor.executemany(
            "INSERT INTO rooms (name, description, price_per_night, capacity, room_type, image_url) VALUES (?, ?, ?, ?, ?, ?)",
            rooms
        )
    
    # Benutzer-Tabelle erstellen
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
    
    # Beispielbenutzer einfügen
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        users = [
            ("Max", "Mustermann", "max@example.com", "password123"),
            ("Maria", "Musterfrau", "maria@example.com", "password456"),
        ]
        cursor.executemany(
            "INSERT INTO users (first_name, last_name, email, hashed_password) VALUES (?, ?, ?, ?)",
            users
        )
    
    conn.commit()
    conn.close()

# Datenbank initialisieren
init_db()

# Authentifizierungsfunktionen
def authenticate_user(email: str, password: str):
    """Benutzer anhand von E-Mail und Passwort authentifizieren"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # In einer echten Anwendung würden Sie das Passwort hashen und vergleichen
    cursor.execute("SELECT * FROM users WHERE email = ? AND hashed_password = ?", (email, password))
    user = cursor.fetchone()
    
    conn.close()
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    """JWT-Token erstellen"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# API-Endpunkte
@app.post("/api/auth/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Benutzer anmelden und Token zurückgeben"""
    user = authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Falsche E-Mail oder Passwort",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Token erstellen
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/hotels")
def get_hotels():
    return [
        {"id": "berlin", "name": "Harmony Heaven Berlin", "location": "Berlin"},
        {"id": "munich", "name": "Harmony Heaven München", "location": "München"},
        {"id": "hamburg", "name": "Harmony Heaven Hamburg", "location": "Hamburg"},
        {"id": "frankfurt", "name": "Harmony Heaven Frankfurt", "location": "Frankfurt"},
    ]

@app.post("/api/bookings/check", response_model=BookingCheckResponse)
def check_availability(booking: BookingCheck):
    try:
        # Datumsformatierung
        check_in_date = datetime.strptime(booking.check_in, "%Y-%m-%d").date()
        check_out_date = datetime.strptime(booking.check_out, "%Y-%m-%d").date()
        
        # Prüfen, ob Check-in vor Check-out liegt
        if check_in_date >= check_out_date:
            raise HTTPException(
                status_code=400, 
                detail="Check-out muss nach Check-in liegen"
            )
        
        # Vereinfachte Implementierung: Wir geben feste Werte zurück
        # In einer realen Anwendung würden wir hier Datenbankabfragen durchführen
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verfügbare Zimmer abfragen basierend auf Kapazität
        cursor.execute(
            "SELECT * FROM rooms WHERE capacity >= ?",
            (booking.adults + booking.children,)
        )
        available_rooms = cursor.fetchall()
        
        # Anzahl der verfügbaren Zimmer und durchschnittlicher Preis
        num_available = len(available_rooms)
        avg_price = sum(room["price_per_night"] for room in available_rooms) / num_available if num_available > 0 else 0
        
        conn.close()
        
        return {
            "available_rooms": num_available,
            "price_per_night": round(avg_price, 2)
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Fehler bei der Verfügbarkeitsprüfung: {str(e)}"
        )

@app.post("/api/bookings")
def create_booking(booking: BookingCheck):
    try:
        # In einer echten Implementierung würden wir hier eine Buchung in der Datenbank erstellen
        # Für dieses vereinfachte Beispiel geben wir nur eine erfolgreiche Antwort zurück
        return {
            "id": 1,
            "check_in": booking.check_in,
            "check_out": booking.check_out,
            "room_name": "Deluxe Zimmer",
            "total_price": 249.0 * (datetime.strptime(booking.check_out, "%Y-%m-%d").date() - 
                           datetime.strptime(booking.check_in, "%Y-%m-%d").date()).days,
            "status": "confirmed"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Fehler bei der Buchungserstellung: {str(e)}"
        )

# Server starten mit: python -m uvicorn simplified_main:app --reload