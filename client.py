#!/usr/bin/env python3
import pygame
import socket
import json
import sys
from buttons import ImageButton, MusicButton, RegisterButton  # Importiere die Button-Klasse aus buttons.py
from LoginScreen import LoginScreen
from utils import toggle_music, send_request, draw_button
from registration_screen import show_registration_screen
import os

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Gladiatoren Spiel")
font = pygame.font.SysFont(None, 36)

pygame.mixer.init()
music_on = False
try:
    pygame.mixer.music.load("music/mygladiator.mp3")  # Hier ggf. anpassen – falls andere Musikdatei genutzt wird
    pygame.mixer.music.set_volume(0.3)
    # Musik wird nicht automatisch gestartet
except Exception as e:
    print("Fehler beim Laden der Hintergrundmusik:", e)

def draw_button_wrapper(text, rect, color=(70,130,180)):
    draw_button(screen, font, text, rect, color)

def login_screen():
    login_screen = LoginScreen(screen, font)
    while True:
        login_screen.draw()
        for event in pygame.event.get():
            result = login_screen.handle_event(event)
            if result:
                return result
        pygame.display.flip()
        login_screen.clock.tick(30)

def gladiator_screen(user_id):
    clock = pygame.time.Clock()
    new_name = ""
    active_field = "new_name"
    input_rect_newname = pygame.Rect(300,480,200,40)
    # Dynamisches Layout: Buttons für Gladiator-Typen in mehreren Zeilen, wenn nötig.
    margin = 50
    gap = 10
    button_width = 120
    button_height = 30
    window_width = 800
    x = margin
    y = 420
    available_types = ["Retiarius", "Secutor", "Murmillo", "Thraex", "Hoplomachus", "Dimachaerus", "Provocator"]
    type_buttons = []
    for typ in available_types:
        if x + button_width > window_width - margin:
            x = margin
            y += button_height + gap
        rect = pygame.Rect(x, y, button_width, button_height)
        type_buttons.append((rect, typ))
        x += button_width + gap
    # "Zurück"-Button unterhalb der Typ-Buttons
    button_rect_back = pygame.Rect(300, y + button_height + 20, 200, 50)
    button_rect_recruit = pygame.Rect(300, button_rect_back.y - 60, 200, 50)
    selected_type = None

    def fetch_gladiators():
        req = {'command': 'get_gladiators', 'user_id': user_id}
        response = send_request(req)
        if response and response.get('status') == 'success':
            return response.get('gladiators', [])
        else:
            return []
    gladiators = fetch_gladiators()

    while True:
        screen.fill((40,40,40))
        title = font.render("Deine Gladiatoren", True, (255,255,255))
        screen.blit(title, (300,20))
        y_offset = 60
        if not gladiators:
            no_text = font.render("Keine Gladiatoren gefunden.", True, (200,200,200))
            screen.blit(no_text, (300, y_offset))
        else:
            for g in gladiators:
                text = font.render(f"ID: {g['id']} | {g['name']} ({g['gladiator_type']})", True, (255,255,255))
                screen.blit(text, (50, y_offset))
                y_offset += 30
        prompt = font.render("Wähle Gladiator-Typ:", True, (255,255,255))
        screen.blit(prompt, (50,410))
        for rect, typ in type_buttons:
            if selected_type == typ:
                pygame.draw.rect(screen, (0,255,0), rect)
            else:
                pygame.draw.rect(screen, (100,100,100), rect)
            typ_text = font.render(typ, True, (255,255,255))
            text_rect = typ_text.get_rect(center=(rect.x+rect.width//2, rect.y+rect.height//2))
            screen.blit(typ_text, text_rect)
        prompt_name = font.render("Neuer Gladiator Name:", True, (255,255,255))
        screen.blit(prompt_name, (300,440))
        pygame.draw.rect(screen, (255,255,255), input_rect_newname, 2)
        new_text = font.render(new_name, True, (255,255,255))
        screen.blit(new_text, (input_rect_newname.x+5, input_rect_newname.y+5))
        draw_button_wrapper("Rekrutieren", button_rect_recruit)
        draw_button_wrapper("Zurück", button_rect_back)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for rect, typ in type_buttons:
                    if rect.collidepoint(mouse_pos):
                        selected_type = typ
                if input_rect_newname.collidepoint(mouse_pos):
                    active_field = "new_name"
                elif button_rect_recruit.collidepoint(mouse_pos):
                    if new_name.strip() == "":
                        print("Bitte einen Namen eingeben!")
                    elif selected_type is None:
                        print("Bitte einen Gladiator-Typ auswählen!")
                    else:
                        req = {'command': 'recruit_gladiator', 'user_id': user_id, 'name': new_name, 'type': selected_type}
                        response = send_request(req)
                        if response and response.get('status') == 'success':
                            gladiators = fetch_gladiators()
                            new_name = ""
                        else:
                            print("Fehler beim Rekrutieren:", response.get('message') if response else "Keine Antwort vom Server")
                elif button_rect_back.collidepoint(mouse_pos):
                    return
            if event.type == pygame.KEYDOWN:
                if active_field == "new_name":
                    if event.key == pygame.K_BACKSPACE:
                        new_name = new_name[:-1]
                    elif event.key == pygame.K_RETURN:
                        if new_name.strip() != "":
                            req = {'command': 'recruit_gladiator', 'user_id': user_id, 'name': new_name, 'type': selected_type}
                            response = send_request(req)
                            if response and response.get('status') == 'success':
                                gladiators = fetch_gladiators()
                                new_name = ""
                            else:
                                print("Fehler beim Rekrutieren:", response.get('message') if response else "Keine Antwort vom Server")
                    else:
                        new_name += event.unicode
        pygame.display.flip()
        clock.tick(30)

def fight_setup_screen(user_id):
    clock = pygame.time.Clock()
    screen.fill((0, 0, 0))
    
    # Hole die Liste der Gladiatoren
    response = send_request({
        'command': 'get_gladiators',
        'user_id': user_id
    })
    
    if response and response.get('status') == 'success':
        gladiators = response['gladiators']
        y_pos = 50
        for g in gladiators:
            # Zeige Gladiator-Info
            text = font.render(
                f"ID: {g['id']} - {g['name']} ({g['gladiator_type']}) | "
                f"LP: {g['lebenspunkte']}, A: {g['angriff']}, "
                f"V: {g['verteidigung']}, E: {g['ausdauer']}", 
                True, (255,255,255)
            )
            screen.blit(text, (50, y_pos))
            
            # Kampf-Button für jeden Gladiator
            fight_button_rect = pygame.Rect(600, y_pos, 100, 30)
            draw_button_wrapper("Kämpfen", fight_button_rect)
            
            # Speichere Gladiator-ID für den Button
            g['button_rect'] = fight_button_rect
            
            y_pos += 40
    
    # Zurück-Button
    back_button_rect = pygame.Rect(50, screen.get_height() - 50, 100, 30)
    draw_button_wrapper("Zurück", back_button_rect)
    
    pygame.display.flip()
    
    # Event-Loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                # Prüfe Zurück-Button
                if back_button_rect.collidepoint(mouse_pos):
                    return
                
                # Prüfe Kampf-Buttons
                if response and response.get('status') == 'success':
                    for g in gladiators:
                        if g['button_rect'].collidepoint(mouse_pos):
                            join_fight(user_id, g['id'])
                            return
        
        clock.tick(30)

def main_menu(user_id, username, currency):
    clock = pygame.time.Clock()
    music_button_rect = pygame.Rect(690,10,100,30)
    button_rect_manage = pygame.Rect(250,250,300,50)
    button_rect_fight = pygame.Rect(250,320,300,50)
    while True:
        screen.fill((50,50,100))
        title = font.render("Hauptmenü", True, (255,255,255))
        info = font.render(f"User: {username} | Guthaben: {currency}", True, (255,255,255))
        screen.blit(title, (350,150))
        screen.blit(info, (250,200))
        draw_button_wrapper("Gladiatoren verwalten", button_rect_manage)
        draw_button_wrapper("Kampf beitreten", button_rect_fight)
        if music_on:
            draw_button_wrapper("Musik aus", music_button_rect, color=(180,80,80))
        else:
            draw_button_wrapper("Musik an", music_button_rect, color=(80,180,80))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if button_rect_manage.collidepoint(mouse_pos):
                    gladiator_screen(user_id)
                elif button_rect_fight.collidepoint(mouse_pos):
                    fight_setup_screen(user_id)
                elif music_button_rect.collidepoint(mouse_pos):
                    toggle_music()
        pygame.display.flip()
        clock.tick(30)

def join_fight(user_id, gladiator_id):
    response = send_request({
        'command': 'join_fight',
        'user_id': user_id,
        'gladiator_id': gladiator_id
    })
    
    print("Join Fight Response:", response)  # Debug-Ausgabe
    
    if response:
        if response.get('status') == 'waiting':
            # Zeige Warteschirm an
            show_waiting_screen(response['gladiator'])
        elif response.get('status') == 'success':
            # Zeige Kampfergebnis an
            show_fight_result(response)
        else:
            print("Fehler beim Kampfbeitritt:", response.get('message'))  # Debug-Ausgabe

def show_waiting_screen(gladiator):
    clock = pygame.time.Clock()
    
    # Timer für die Kampfabfrage
    last_check = pygame.time.get_ticks()
    check_interval = 1000  # Prüfe jede Sekunde
    
    while True:
        screen.fill((0, 0, 0))
        
        # Zeige Gladiator-Info
        text = font.render(
            f"Warte auf Gegner mit {gladiator['gladiator_name']} ({gladiator['gladiator_type']})",
            True, (255, 255, 255)
        )
        screen.blit(text, (50, 50))
        
        # Zeige Stats
        stats_text = font.render(
            f"LP: {gladiator['lebenspunkte']}, A: {gladiator['angriff']}, "
            f"V: {gladiator['verteidigung']}, E: {gladiator['ausdauer']}",
            True, (255, 255, 255)
        )
        screen.blit(stats_text, (50, 100))
        
        # Abbrechen-Button
        cancel_button_rect = pygame.Rect(50, screen.get_height() - 50, 100, 30)
        draw_button_wrapper("Abbrechen", cancel_button_rect)
        
        current_time = pygame.time.get_ticks()
        
        # Prüfe regelmäßig, ob ein Kampf begonnen hat
        if current_time - last_check >= check_interval:
            try:
                # Sende eine Anfrage, um den Kampfstatus zu prüfen
                response = send_request({
                    'command': 'check_fight_status',
                    'gladiator_id': gladiator['gladiator_id']
                })
                
                print("Kampfstatus Response:", response)  # Debug-Ausgabe
                
                if response:
                    if response.get('status') == 'success':
                        # Wenn ein Kampf gefunden wurde, zeige das Ergebnis an
                        print("Kampf gefunden, zeige Ergebnis")  # Debug-Ausgabe
                        show_fight_result(response)
                        return
                    elif response.get('status') == 'error':
                        # Bei Fehler zurück zum Hauptmenü
                        error_text = font.render(response.get('message', 'Fehler aufgetreten'), True, (255, 0, 0))
                        screen.blit(error_text, (50, 150))
                        pygame.display.flip()
                        pygame.time.wait(2000)  # Zeige Fehlermeldung für 2 Sekunden
                        return
                    # Bei 'waiting' Status weiterwarten
            except Exception as e:
                print("Fehler beim Prüfen des Kampfstatus:", e)
                error_text = font.render("Verbindungsfehler, versuche erneut...", True, (255, 0, 0))
                screen.blit(error_text, (50, 150))
                pygame.display.flip()
                pygame.time.wait(1000)  # Warte eine Sekunde vor dem nächsten Versuch
                    
            last_check = current_time
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if cancel_button_rect.collidepoint(event.pos):
                    # Sende eine Anfrage, um das Warten abzubrechen
                    try:
                        send_request({
                            'command': 'cancel_fight',
                            'gladiator_id': gladiator['gladiator_id']
                        })
                    except Exception as e:
                        print("Fehler beim Abbrechen des Kampfes:", e)
                    return
        
        pygame.display.flip()
        clock.tick(30)

def show_fight_result(result):
    print("Zeige Kampfergebnis:", result)  # Debug-Ausgabe
    
    clock = pygame.time.Clock()
    scroll_offset = 0
    max_scroll = 0
    
    # Erstelle ein detailliertes Kampflog, wenn keines vorhanden ist
    if not result.get('fight_log'):
        winner = result.get('winner', {})
        loser = result.get('loser', {})
        result['fight_log'] = [
            f"Kampf zwischen {winner.get('gladiator_name')} und {loser.get('gladiator_name')}",
            f"",
            f"{winner.get('gladiator_name')} ({winner.get('gladiator_type')})",
            f"LP: {winner.get('lebenspunkte')}, A: {winner.get('angriff')}, V: {winner.get('verteidigung')}, E: {winner.get('ausdauer')}",
            f"",
            f"{loser.get('gladiator_name')} ({loser.get('gladiator_type')})",
            f"LP: {loser.get('lebenspunkte')}, A: {loser.get('angriff')}, V: {loser.get('verteidigung')}, E: {loser.get('ausdauer')}",
            f"",
            result.get('message', 'Kampf beendet!')
        ]
    
    while True:
        screen.fill((0, 0, 0))
        
        # Zeige Kampfergebnis
        title = font.render(result.get('message', 'Kampf beendet!'), True, (255, 255, 255))
        screen.blit(title, (50, 50))
        
        # Zeige Kampfprotokoll
        y_pos = 100 - scroll_offset
        if result.get('fight_log'):
            for log_entry in result['fight_log']:
                if y_pos >= 100 and y_pos < screen.get_height() - 100:  # Nur sichtbare Einträge rendern
                    text = font.render(str(log_entry), True, (255, 255, 255))
                    screen.blit(text, (50, y_pos))
                y_pos += 30
            
            # Aktualisiere maximalen Scroll-Wert
            max_scroll = max(0, len(result['fight_log']) * 30 - (screen.get_height() - 200))
        else:
            text = font.render("Kein Kampfprotokoll verfügbar", True, (255, 255, 255))
            screen.blit(text, (50, y_pos))
        
        # Zurück-Button
        back_button_rect = pygame.Rect(50, screen.get_height() - 50, 100, 30)
        draw_button_wrapper("Zurück", back_button_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Mausrad hoch
                    scroll_offset = max(0, scroll_offset - 30)
                elif event.button == 5:  # Mausrad runter
                    scroll_offset = min(max_scroll, scroll_offset + 30)
                elif back_button_rect.collidepoint(event.pos):
                    return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    scroll_offset = max(0, scroll_offset - 30)
                elif event.key == pygame.K_DOWN:
                    scroll_offset = min(max_scroll, scroll_offset + 30)
                    
        clock.tick(30)

def main():
    user_id, username, currency = login_screen()
    main_menu(user_id, username, currency)

if __name__ == '__main__':
    main()
