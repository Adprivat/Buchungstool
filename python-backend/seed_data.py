from database import SessionLocal, engine
import models
from datetime import datetime, timedelta

# Datenbank-Verbindung
db = SessionLocal()

# Beispiel-Zimmer für jedes Hotel erstellen
def seed_rooms():
    try:
        # Überprüfen, ob bereits Zimmer vorhanden sind
        room_count = db.query(models.Room).count()
        if room_count > 0:
            print(f"{room_count} Zimmer bereits in der Datenbank vorhanden. Keine neuen Zimmer werden erstellt.")
            return
        
        # Zimmer für das Berlin Hotel
        berlin_rooms = [
            models.Room(
                name="Standard Zimmer Berlin",
                description="Komfortables Zimmer mit Blick auf die Stadt",
                price_per_night=199.0,
                capacity=2,
                room_type="standard",
                image_url="/room-1.jpg"
            ),
            models.Room(
                name="Deluxe Zimmer Berlin",
                description="Geräumiges Zimmer mit Kingsize-Bett",
                price_per_night=249.0,
                capacity=2,
                room_type="deluxe",
                image_url="/room-2.jpg"
            ),
            models.Room(
                name="Suite Berlin",
                description="Luxuriöse Suite mit separatem Wohnbereich",
                price_per_night=349.0,
                capacity=4,
                room_type="suite",
                image_url="/room-3.jpg"
            )
        ]
        
        # Zimmer für das München Hotel
        munich_rooms = [
            models.Room(
                name="Standard Zimmer München",
                description="Komfortables Zimmer im bayerischen Stil",
                price_per_night=209.0,
                capacity=2,
                room_type="standard",
                image_url="/room-1.jpg"
            ),
            models.Room(
                name="Deluxe Zimmer München",
                description="Geräumiges Zimmer mit Blick auf die Alpen",
                price_per_night=259.0,
                capacity=2,
                room_type="deluxe",
                image_url="/room-2.jpg"
            ),
            models.Room(
                name="Suite München",
                description="Luxuriöse Suite mit Whirlpool",
                price_per_night=359.0,
                capacity=4,
                room_type="suite",
                image_url="/room-3.jpg"
            )
        ]
        
        # Zimmer für das Hamburg Hotel
        hamburg_rooms = [
            models.Room(
                name="Standard Zimmer Hamburg",
                description="Komfortables Zimmer mit Hafenblick",
                price_per_night=219.0,
                capacity=2,
                room_type="standard",
                image_url="/room-1.jpg"
            ),
            models.Room(
                name="Deluxe Zimmer Hamburg",
                description="Geräumiges Zimmer mit Panoramablick",
                price_per_night=269.0,
                capacity=2,
                room_type="deluxe",
                image_url="/room-2.jpg"
            ),
            models.Room(
                name="Suite Hamburg",
                description="Luxuriöse Suite mit Alsterblick",
                price_per_night=369.0,
                capacity=4,
                room_type="suite",
                image_url="/room-3.jpg"
            )
        ]
        
        # Zimmer für das Frankfurt Hotel
        frankfurt_rooms = [
            models.Room(
                name="Standard Zimmer Frankfurt",
                description="Komfortables Zimmer mit Skylineblick",
                price_per_night=189.0,
                capacity=2,
                room_type="standard",
                image_url="/room-1.jpg"
            ),
            models.Room(
                name="Deluxe Zimmer Frankfurt",
                description="Geräumiges Zimmer mit Mainblick",
                price_per_night=239.0,
                capacity=2,
                room_type="deluxe",
                image_url="/room-2.jpg"
            ),
            models.Room(
                name="Suite Frankfurt",
                description="Luxuriöse Suite im Bankenviertel",
                price_per_night=339.0,
                capacity=4,
                room_type="suite",
                image_url="/room-3.jpg"
            )
        ]
        
        # Alle Zimmer zur Datenbank hinzufügen
        all_rooms = berlin_rooms + munich_rooms + hamburg_rooms + frankfurt_rooms
        db.add_all(all_rooms)
        db.commit()
        
        print(f"{len(all_rooms)} Zimmer erfolgreich zur Datenbank hinzugefügt.")
    except Exception as e:
        db.rollback()
        print(f"Fehler beim Hinzufügen der Zimmer: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    # Tabellen erstellen (falls noch nicht vorhanden)
    models.Base.metadata.create_all(bind=engine)
    
    # Beispiel-Zimmer einfügen
    seed_rooms()