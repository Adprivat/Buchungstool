#!/usr/bin/env python3
import pygame
import socket
import json
import sys
from buttons import ImageButton, MusicButton, RegisterButton, FightButton, GladiatorButton, Fight_s_Button  # Importiere die Button-Klasse aus buttons.py
from LoginScreen import LoginScreen
from utils import toggle_music, send_request, draw_button
from registration_screen import show_registration_screen
from animated_background import AnimatedBackground
import os

# Initialisierung von Pygame und Einstellung des Fensters
pygame.init()
screen = pygame.display.set_mode((800, 600))  # Erstelle ein 800x600 Pixel großes Fenster
pygame.display.set_caption("Gladiator")  # Setze den Fenstertitel
font = pygame.font.SysFont(None, 36)  # Lade die Standard-Schriftart in Größe 36

# Initialisierung der Musik
pygame.mixer.init()
music_on = False  # Musik standardmäßig aus
try:
    pygame.mixer.music.load("music/mygladiator.mp3")  # Hier ggf. anpassen – falls andere Musikdatei genutzt wird
    pygame.mixer.music.set_volume(0.3)  # Setze Lautstärke auf 30%
    # Musik wird nicht automatisch gestartet
except Exception as e:
    print("Fehler beim Laden der Hintergrundmusik:", e)

# Hilfsfunktion zum Zeichnen von Buttons
def draw_button_wrapper(text, rect, color=(70,130,180)):
    """Wrapper-Funktion für das Zeichnen von Buttons mit den korrekten Screen- und Font-Parametern"""
    draw_button(screen, font, text, rect, color)

def login_screen():
    """
    Zeigt den Login-Bildschirm an und verarbeitet die Login-Logik
    Returns:
        tuple: (user_id, username, currency) bei erfolgreichem Login
    """
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
    input_rect_newname = pygame.Rect(400,490,260,40)
    
    # Initialisiere animierten Hintergrund
    background = AnimatedBackground(
        'assets/LoginBackground',
        'ezgif-frame-{:03d}.png',
        28,
        target_size=(800, 600),
        frame_delay=100
    )
    
    # Dynamisches Layout: Buttons für Gladiator-Typen in mehreren Zeilen, wenn nötig.
    margin = 50
    gap = 10
    button_width = 160
    button_height = 40
    window_width = 800
    x = margin
    y = 350
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
    button_rect_back = pygame.Rect(50, y + button_height + 80, 200, 50)
    button_rect_recruit = pygame.Rect(50, button_rect_back.y - 60, 200, 50)
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
        # Update und zeichne den Hintergrund
        background.update()
        background.draw(screen)
        
        title = font.render("Deine Gladiatoren", True, (255,255,255))
        screen.blit(title, (300,20))
        
        # Zeige die Kosten für einen neuen Gladiator an
        cost_text = font.render("Kosten für einen neuen Gladiator: 100 Gold", True, (255,215,0))  # Gold-Farbe
        screen.blit(cost_text, (50,300))
        
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
        screen.blit(prompt, (50,250))
        for rect, typ in type_buttons:
            if selected_type == typ:
                pygame.draw.rect(screen, (0,255,0), rect)
            else:
                pygame.draw.rect(screen, (100,100,100), rect)
            typ_text = font.render(typ, True, (255,255,255))
            text_rect = typ_text.get_rect(center=(rect.x+rect.width//2, rect.y+rect.height//2))
            screen.blit(typ_text, text_rect)
        prompt_name = font.render("Neuer Gladiator Name:", True, (255,255,255))
        screen.blit(prompt_name, (400,445))
        pygame.draw.rect(screen, (255,255,255), input_rect_newname, 2)
        new_text = font.render(new_name, True, (255,255,255))
        screen.blit(new_text, (input_rect_newname.x+5, input_rect_newname.y+5))
        draw_button_wrapper("Rekrutieren (100 Gold)", button_rect_recruit)
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
    """
    Zeigt den Bildschirm zur Kampfvorbereitung an
    Args:
        user_id: ID des eingeloggten Benutzers
    """
    clock = pygame.time.Clock()
    
    # Initialisiere animierten Hintergrund
    background = AnimatedBackground(
        'assets/LoginBackground',
        'ezgif-frame-{:03d}.png',
        28,
        target_size=(800, 600),
        frame_delay=100
    )
    
    # Hole die Liste der Gladiatoren
    response = send_request({
        'command': 'get_gladiators',
        'user_id': user_id
    })
    
    if response and response.get('status') == 'success':
        gladiators = response['gladiators']
        fight_buttons = []  # Liste für die Fight-Buttons
        
        # Erstelle Fight-Buttons für jeden Gladiator
        for i, g in enumerate(gladiators):
            y_pos = 50 + (i * 70)  # Vertikaler Abstand zwischen den Gladiatoren
            fight_button = Fight_s_Button(pos=(600, y_pos))
            fight_buttons.append((fight_button, g))  # Speichere Button und komplettes Gladiator-Dict
    
    # Event-Loop
    while True:
        # Update und zeichne den Hintergrund
        background.update()
        background.draw(screen)
        
        # Zeichne Gladiatoren und ihre Buttons
        if response and response.get('status') == 'success':
            for i, (button, g) in enumerate(fight_buttons):
                y_pos = 50 + (i * 70)
                # Zeige Gladiator-Info
                text = font.render(
                    f"{g['name']} ({g['gladiator_type']}) | "
                    f"LP: {g['lebenspunkte']}, A: {g['angriff']}, "
                    f"V: {g['verteidigung']}, E: {g['ausdauer']}", 
                    True, (255,255,255)
                )
                screen.blit(text, (50, y_pos + 10))  # +10 für vertikale Zentrierung mit Button
                button.draw(screen)
        
        # Zurück-Button
        back_button_rect = pygame.Rect(50, screen.get_height() - 50, 100, 30)
        draw_button_wrapper("Zurück", back_button_rect)
        
        # Event-Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Prüfe Fight-Buttons mit handle_event
            for button, gladiator in fight_buttons:
                if button.handle_event(event):  # Verwende handle_event statt rect.collidepoint
                    join_fight(user_id, gladiator['id'])
                    return
                    
            # Prüfe Zurück-Button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button_rect.collidepoint(event.pos):
                    return
        
        pygame.display.flip()
        clock.tick(30)

def main_menu(user_id, username, currency):
    clock = pygame.time.Clock()
    music_button = MusicButton(pos=(690,10))
    fight_button = FightButton(pos=(400,320))
    gladiator_button = GladiatorButton(pos=(200,320))
    
    # Initialisiere animierten Hintergrund
    background = AnimatedBackground(
        'assets/LoginBackground',
        'ezgif-frame-{:03d}.png',
        28,
        target_size=(800, 600),
        frame_delay=100
    )
    
    # Lade die Titelbilder für das Hauptmenü
    title_frames = []
    for i in range(8):  # sprite_0 bis sprite_7
        frame = pygame.image.load(os.path.join('assets/titel_Hauptmenu', f'sprite_{i}.png')).convert_alpha()
        title_frames.append(frame)
    current_title_frame = 0
    title_frame_delay = 150  # milliseconds
    last_title_update = pygame.time.get_ticks()
    
    while True:
        # Update und zeichne den Hintergrund
        background.update()
        background.draw(screen)
        
        # Animiere den Titel
        now = pygame.time.get_ticks()
        if now - last_title_update > title_frame_delay:
            current_title_frame = (current_title_frame + 1) % len(title_frames)
            last_title_update = now
        
        # Zentriere den Titel
        title_frame = title_frames[current_title_frame]
        title_rect = title_frame.get_rect(center=(400, 100))  # Zentriert bei y=100
        screen.blit(title_frame, title_rect)
        
        info = font.render(f"User: {username} | Guthaben: {currency}", True, (255,255,255))
        screen.blit(info, (250,270))
        gladiator_button.draw(screen)
        fight_button.draw(screen)
        music_button.draw(screen, font)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if gladiator_button.handle_event(event):
                gladiator_screen(user_id)
            elif fight_button.handle_event(event):
                fight_setup_screen(user_id)
            elif music_button.handle_event(event):
                toggle_music()
        pygame.display.flip()
        clock.tick(30)

def join_fight(user_id, gladiator_id):
    """
    Tritt einem Kampf bei oder erstellt einen neuen
    Args:
        user_id: ID des eingeloggten Benutzers
        gladiator_id: ID des ausgewählten Gladiators
    """
    print(f"Versuche Kampf beizutreten mit Gladiator ID: {gladiator_id}")  # Debug-Ausgabe
    
    response = send_request({
        'command': 'join_fight',
        'user_id': user_id,
        'gladiator_id': gladiator_id
    })
    
    print("Server Antwort:", response)  # Debug-Ausgabe
    
    if response:
        if response.get('status') == 'waiting':
            # Starte Wartebildschirm
            gladiator_info = response.get('gladiator', {})
            if gladiator_info:
                show_waiting_screen(gladiator_info)
            else:
                print("Fehler: Keine Gladiator-Informationen erhalten")
        elif response.get('status') == 'success':
            # Zeige sofortiges Kampfergebnis
            show_fight_result(response)
        else:
            print(f"Unerwarteter Status: {response.get('status')}")
            print(f"Fehlermeldung: {response.get('message', 'Keine Fehlermeldung')}")
    else:
        print("Keine Antwort vom Server erhalten")

def show_waiting_screen(gladiator):
    """
    Zeigt den Wartebildschirm während der Suche nach einem Gegner
    Args:
        gladiator: Dictionary mit den Informationen des wartenden Gladiators
    """
    clock = pygame.time.Clock()
    
    # Initialisiere animierten Kampf-Hintergrund
    background = AnimatedBackground(
        'assets/Kampf_Background',
        'ezgif-frame-{:03d}.png',
        17,
        target_size=(800, 600),
        frame_delay=100
    )
    
    # Timer für die Kampfabfrage
    last_check = pygame.time.get_ticks()
    check_interval = 1000  # Prüfe jede Sekunde
    animation_dots = 0  # Für animierte Punkte
    dot_update = pygame.time.get_ticks()
    
    while True:
        # Update und zeichne den animierten Hintergrund
        background.update()
        background.draw(screen)
        
        # Erstelle eine halbtransparente Oberfläche für den Text
        text_surface = pygame.Surface((700, 200))
        text_surface.set_alpha(128)
        text_surface.fill((0, 0, 0))
        screen.blit(text_surface, (50, 30))
        
        # Animierte Wartepunkte
        now = pygame.time.get_ticks()
        if now - dot_update > 500:  # Alle 500ms aktualisieren
            animation_dots = (animation_dots + 1) % 4
            dot_update = now
        
        # Zeige Gladiator-Info mit Schatten
        title_text = f"Warte auf Gegner{'.' * animation_dots}"
        title_shadow = font.render(title_text, True, (0, 0, 0))
        title = font.render(title_text, True, (255, 215, 0))  # Gold-Farbe
        screen.blit(title_shadow, (52, 52))
        screen.blit(title, (50, 50))
        
        # Zeige Gladiator-Name und Typ
        glad_info = f"{gladiator['gladiator_name']} ({gladiator['gladiator_type']})"
        info_text = font.render(glad_info, True, (255, 255, 255))
        screen.blit(info_text, (50, 100))
        
        # Zeige Stats mit Symbolen
        stats_text = font.render(
            f"❤️ LP: {gladiator['lebenspunkte']}  ⚔️ A: {gladiator['angriff']}  "
            f"🛡️ V: {gladiator['verteidigung']}  💪 E: {gladiator['ausdauer']}",
            True, (255, 255, 255)
        )
        screen.blit(stats_text, (50, 150))
        
        # Abbrechen-Button mit Kampf-Stil
        cancel_button_rect = pygame.Rect(50, screen.get_height() - 50, 150, 40)
        # Zeichne Button-Schatten
        shadow_rect = cancel_button_rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        pygame.draw.rect(screen, (0, 0, 0), shadow_rect, border_radius=5)
        # Zeichne eigentlichen Button
        pygame.draw.rect(screen, (139, 0, 0), cancel_button_rect, border_radius=5)  # Dunkelrot
        # Button-Text
        text_surf = font.render("Abbrechen", True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=cancel_button_rect.center)
        screen.blit(text_surf, text_rect)
        
        current_time = pygame.time.get_ticks()
        
        # Prüfe regelmäßig, ob ein Kampf begonnen hat
        if current_time - last_check >= check_interval:
            try:
                response = send_request({
                    'command': 'check_fight_status',
                    'gladiator_id': gladiator['gladiator_id']
                })
                
                if response:
                    if response.get('status') == 'success':
                        show_fight_result(response)
                        return
                    elif response.get('status') == 'error':
                        error_text = font.render(response.get('message', 'Fehler aufgetreten'), True, (255, 0, 0))
                        screen.blit(error_text, (50, 200))
                        pygame.display.flip()
                        pygame.time.wait(2000)
                        return
            except Exception as e:
                print("Fehler beim Prüfen des Kampfstatus:", e)
                error_text = font.render("Verbindungsfehler, versuche erneut...", True, (255, 0, 0))
                screen.blit(error_text, (50, 200))
                pygame.display.flip()
                pygame.time.wait(1000)
                    
            last_check = current_time
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if cancel_button_rect.collidepoint(event.pos):
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
    """
    Zeigt das Ergebnis eines Kampfes an
    Args:
        result: Dictionary mit den Kampfergebnissen und dem Kampflog
    """
    print("Zeige Kampfergebnis:", result)
    
    clock = pygame.time.Clock()
    scroll_offset = 0
    max_scroll = 0
    
    # Initialisiere animierten Kampf-Hintergrund
    background = AnimatedBackground(
        'assets/Kampf_Background',
        'ezgif-frame-{:03d}.png',
         17,
        target_size=(800, 600),
        frame_delay=100
    )
    
    # Erstelle ein detailliertes Kampflog
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
        # Update und zeichne den animierten Hintergrund
        background.update()
        background.draw(screen)
        
        # Erstelle eine halbtransparente Oberfläche für den Text
        text_surface = pygame.Surface((700, 450))
        text_surface.set_alpha(128)
        text_surface.fill((0, 0, 0))
        screen.blit(text_surface, (50, 30))
        
        # Zeige Kampfergebnis mit Schatten für bessere Lesbarkeit
        title_shadow = font.render(result.get('message', 'Kampf beendet!'), True, (0, 0, 0))
        title = font.render(result.get('message', 'Kampf beendet!'), True, (255, 215, 0))  # Gold-Farbe
        screen.blit(title_shadow, (52, 52))  # Schatten-Offset
        screen.blit(title, (50, 50))
        
        # Zeige Kampfprotokoll
        y_pos = 100 - scroll_offset
        if result.get('fight_log'):
            for log_entry in result['fight_log']:
                if y_pos >= 100 and y_pos < screen.get_height() - 100:
                    text = font.render(str(log_entry), True, (255, 255, 255))
                    screen.blit(text, (60, y_pos))  # Leicht eingerückt
                y_pos += 30
            
            max_scroll = max(0, len(result['fight_log']) * 30 - (screen.get_height() - 200))
        else:
            text = font.render("Kein Kampfprotokoll verfügbar", True, (255, 255, 255))
            screen.blit(text, (60, y_pos))
        
        # Zurück-Button mit Kampf-Stil
        back_button_rect = pygame.Rect(50, screen.get_height() - 50, 150, 40)
        # Zeichne Button-Schatten
        shadow_rect = back_button_rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        pygame.draw.rect(screen, (0, 0, 0), shadow_rect, border_radius=5)
        # Zeichne eigentlichen Button
        pygame.draw.rect(screen, (139, 0, 0), back_button_rect, border_radius=5)  # Dunkelrot
        # Button-Text
        text_surf = font.render("Zurück", True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=back_button_rect.center)
        screen.blit(text_surf, text_rect)
        
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
    """Hauptfunktion des Spiels"""
    user_id, username, currency = login_screen()  # Starte mit dem Login-Bildschirm
    main_menu(user_id, username, currency)  # Nach erfolgreichem Login zeige das Hauptmenü

# Starte das Spiel, wenn die Datei direkt ausgeführt wird
if __name__ == '__main__':
    main()
