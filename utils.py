import pygame
import socket
import json
import sys
import os
from dotenv import load_dotenv

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

def send_request(request):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((SERVER_IP, SERVER_PORT))
        s.sendall(json.dumps(request).encode())
        response = s.recv(4096)
        s.close()
        if not response:
            raise Exception("Keine Daten vom Server empfangen.")
        return json.loads(response.decode())
    except Exception as e:
        print("Verbindungsfehler:", e)
        return None

def draw_button(screen, font, text, rect, color=(70,130,180)):
    pygame.draw.rect(screen, color, rect)
    text_surf = font.render(text, True, (255,255,255))
    text_rect = text_surf.get_rect(center=(rect[0]+rect[2]//2, rect[1]+rect[3]//2))
    screen.blit(text_surf, text_rect)
