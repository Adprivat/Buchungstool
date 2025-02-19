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

music_on = True

pygame.mixer.init()
try:
    pygame.mixer.music.load("music/mygladiator.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
except Exception as e:
    print("Fehler beim Laden der Hintergrundmusik:", e)

def toggle_music():
    global music_on
    if music_on:
        pygame.mixer.music.stop()
        music_on = False
    else:
        pygame.mixer.music.play(-1)
        music_on = True

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
