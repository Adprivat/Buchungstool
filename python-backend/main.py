from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel
import jwt
import bcrypt
import models
from database import engine, SessionLocal

# Datenbank-Tabellen erstellen
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Harmony Heaven Hotels API")

# CORS-Konfiguration für die Kommunikation mit dem Next.js-Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend-URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JWT-Konfiguration
SECRET_KEY = "IhrGeheimesPasswort"  # In Produktion sicherer speichern!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Abhängigkeit für Datenbankverbindung
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic-Modelle für Anfragen und Antworten
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class BookingCheck(BaseModel):
    check_in: str
    check_out: str
    adults: int
    children: int
    rooms: int

class BookingCheckResponse(BaseModel):
    available_rooms: int
    price_per_night: float

# Zusätzliche Pydantic-Modelle für Anfragen und Antworten
class BookingCreate(BaseModel):
    hotel_id: str
    room_id: Optional[int] = None
    check_in: str
    check_out: str
    adults: int
    children: int
    rooms: int
    
class BookingResponse(BaseModel):
    id: int
    check_in: str
    check_out: str
    room_name: str
    total_price: float
    status: str
    
    class Config:
        orm_mode = True

# Authentifizierungsfunktionen
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Ungültige Anmeldedaten",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except jwt.PyJWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user

# API-Endpunkte
@app.post("/api/auth/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="E-Mail bereits registriert")
    
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/api/auth/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Falsche E-Mail oder Passwort",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
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
def check_availability(booking: BookingCheck, db: Session = Depends(get_db)):
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
            
        # Zimmer abfragen, die in diesem Zeitraum bereits gebucht sind
        booked_rooms = db.query(models.Room.id).join(models.Booking).filter(
            models.Booking.check_in < check_out_date,
            models.Booking.check_out > check_in_date
        ).all()
        
        # IDs der gebuchten Zimmer extrahieren
        booked_room_ids = [room[0] for room in booked_rooms]
        
        # Verfügbare Zimmer abfragen
        available_rooms = db.query(models.Room).filter(
            models.Room.id.notin_(booked_room_ids),
            models.Room.capacity >= booking.adults + booking.children
        ).all()
        
        # Anzahl der verfügbaren Zimmer und durchschnittlicher Preis
        num_available = len(available_rooms)
        avg_price = sum(room.price_per_night for room in available_rooms) / num_available if num_available > 0 else 0
        
        return {
            "available_rooms": num_available,
            "price_per_night": round(avg_price, 2)
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Fehler bei der Verfügbarkeitsprüfung: {str(e)}"
        )

@app.post("/api/bookings", response_model=BookingResponse)
def create_booking(booking: BookingCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        # Datumsformatierung
        check_in_date = datetime.strptime(booking.check_in, "%Y-%m-%d").date()
        check_out_date = datetime.strptime(booking.check_out, "%Y-%m-%d").date()
        
        # Verfügbares Zimmer finden
        available_room = db.query(models.Room).filter(
            models.Room.id == booking.room_id
        ).first()
        
        if not available_room:
            raise HTTPException(
                status_code=404,
                detail="Das gewählte Zimmer ist nicht verfügbar"
            )
        
        # Anzahl der Übernachtungen berechnen
        nights = (check_out_date - check_in_date).days
        total_price = available_room.price_per_night * nights
        
        # Buchung erstellen
        new_booking = models.Booking(
            user_id=current_user.id,
            room_id=available_room.id,
            check_in=check_in_date,
            check_out=check_out_date,
            adults=booking.adults,
            children=booking.children,
            total_price=total_price,
            status="confirmed"
        )
        
        db.add(new_booking)
        db.commit()
        db.refresh(new_booking)
        
        return {
            "id": new_booking.id,
            "check_in": booking.check_in,
            "check_out": booking.check_out,
            "room_name": available_room.name,
            "total_price": total_price,
            "status": "confirmed"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Fehler bei der Buchungserstellung: {str(e)}"
        )

# Server starten mit: uvicorn main:app --reload

