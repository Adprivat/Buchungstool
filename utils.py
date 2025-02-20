import pygame
import socket
import json
import sys
import os
from dotenv import load_dotenv
import time

# Lade Umgebungsvariablen
load_dotenv()

# Client-Verbindungsdaten
SERVER_IP = os.getenv('CLIENT_HOST', 'maglev.proxy.rlwy.net')
SERVER_PORT = int(os.getenv('CLIENT_PORT', '44200'))

# Musik-Steuerung
music_on = False  # Startzustand: Musik ist aus

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def init_music():
    """Initialisiert die Musik beim Programmstart, startet sie aber nicht automatisch."""
    global music_on
    try:
        pygame.mixer.music.load(resource_path("music/mygladiator.mp3"))
        pygame.mixer.music.set_volume(0.3)
        # Musik wird geladen, aber NICHT abgespielt – Musik bleibt aus
        music_on = False
    except Exception as e:
        print("Fehler beim Laden der Musik:", e)
        music_on = False


def toggle_music():
    """Schaltet die Musik ein/aus"""
    global music_on
    try:
        if music_on:
            pygame.mixer.music.pause()
            music_on = False
        else:
            # Wenn die Musik noch nicht geladen wurde, lade sie
            try:
                pygame.mixer.music.load(resource_path("music/mygladiator.mp3"))
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play(-1)
            except:
                pass
            pygame.mixer.music.unpause()
            music_on = True
    except Exception as e:
        print("Fehler beim Umschalten der Musik:", e)
        music_on = False

def send_request(request, max_retries=3):
    """Sendet eine Anfrage an den Server mit Wiederholungsversuchen bei Verbindungsfehlern."""
    for attempt in range(max_retries):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((SERVER_IP, SERVER_PORT))
            client.sendall(json.dumps(request).encode())
            
            # Empfange die Antwort in Chunks
            response_data = b""
            while True:
                chunk = client.recv(4096)
                if not chunk:
                    break
                response_data += chunk
                
                # Versuche die Antwort zu parsen
                try:
                    response = json.loads(response_data.decode())
                    client.close()
                    return response
                except json.JSONDecodeError:
                    # Wenn die Antwort noch nicht vollständig ist, sammle weitere Chunks
                    continue
                    
        except Exception as e:
            print(f"Verbindungsfehler (Versuch {attempt + 1}/{max_retries}):", e)
            if attempt < max_retries - 1:
                time.sleep(1)  # Warte eine Sekunde vor dem nächsten Versuch
            client.close()
            
    print("Maximale Anzahl an Wiederholungsversuchen erreicht")
    return None

def draw_button(screen, font, text, rect, color=(70,130,180)):
    pygame.draw.rect(screen, color, rect)
    text_surf = font.render(text, True, (255,255,255))
    text_rect = text_surf.get_rect(center=(rect[0]+rect[2]//2, rect[1]+rect[3]//2))
    screen.blit(text_surf, text_rect)
