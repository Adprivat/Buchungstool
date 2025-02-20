#!/usr/bin/env python3
import pygame
import socket
import json
import sys
import os
from buttons import ImageButton, MusicButton, RegisterButton, FightButton, GladiatorButton, Fight_s_Button
from LoginScreen import LoginScreen
from utils import toggle_music, send_request, draw_button, resource_path, init_music
from registration_screen import show_registration_screen
from animated_background import AnimatedBackground

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Gladiator")
font = pygame.font.SysFont(None, 36)

# Musik initialisieren – Musik wird geladen, aber nicht automatisch abgespielt (Startzustand "aus")
pygame.mixer.init()
init_music()

def draw_button_wrapper(text, rect, color=(70, 130, 180)):
    draw_button(screen, font, text, rect, color)

def login_screen():
    login_scr = LoginScreen(screen, font)
    while True:
        login_scr.draw()
        for event in pygame.event.get():
            result = login_scr.handle_event(event)
            if result:
                return result  # (user_id, username, currency)
        pygame.display.flip()
        login_scr.clock.tick(30)

def get_currency(user_id):
    response = send_request({'command': 'get_currency', 'user_id': user_id})
    if response and response.get('status') == 'success':
        return response.get('currency')
    return None

def gladiator_screen(user_id, currency):
    """
    Gladiator-Verwaltung: Beim Aufrufen wird die aktuelle Liste der Gladiatoren
    einmalig vom Server abgerufen. Bei Aktionen (z. B. Rekrutieren) wird die Liste
    bei Bedarf aktualisiert.
    """
    clock = pygame.time.Clock()
    new_name = ""
    active_field = "new_name"
    input_rect_newname = pygame.Rect(400, 490, 260, 40)
    
    background = AnimatedBackground(
        resource_path('assets/LoginBackground'),
        'ezgif-frame-{:03d}.png',
        28,
        target_size=(800, 600),
        frame_delay=100
    )
    
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

    button_rect_recruit = pygame.Rect(50, y + button_height + 20, 200, 50)
    button_rect_back = pygame.Rect(50, y + button_height + 80, 200, 50)
    selected_type = None

    def fetch_gladiators():
        req = {'command': 'get_gladiators', 'user_id': user_id}
        response = send_request(req)
        if response and response.get('status') == 'success':
            return response.get('gladiators', [])
        return []
    
    gladiators = fetch_gladiators()

    while True:
        background.update()
        background.draw(screen)
        
        title = font.render("Deine Gladiatoren", True, (255, 255, 255))
        screen.blit(title, (300, 20))
        
        cost_text = font.render("Kosten für einen neuen Gladiator: 100 Gold", True, (255, 215, 0))
        screen.blit(cost_text, (50, 300))
        
        y_offset = 60
        if not gladiators:
            no_text = font.render("Keine Gladiatoren gefunden.", True, (200, 200, 200))
            screen.blit(no_text, (300, y_offset))
        else:
            for g in gladiators:
                text = font.render(f"ID: {g['id']} | {g['name']} ({g['gladiator_type']})", True, (255, 255, 255))
                screen.blit(text, (50, y_offset))
                y_offset += 30
        
        prompt = font.render("Wähle Gladiator-Typ:", True, (255, 255, 255))
        screen.blit(prompt, (50, 250))
        for rect, typ in type_buttons:
            color = (0, 255, 0) if selected_type == typ else (100, 100, 100)
            pygame.draw.rect(screen, color, rect)
            typ_text = font.render(typ, True, (255, 255, 255))
            text_rect = typ_text.get_rect(center=(rect.x + rect.width // 2, rect.y + rect.height // 2))
            screen.blit(typ_text, text_rect)
        
        prompt_name = font.render("Neuer Gladiator Name:", True, (255, 255, 255))
        screen.blit(prompt_name, (400, 445))
        
        # Zeichne das Eingabefeld mit unterschiedlichen Farben für aktiv/inaktiv
        name_color = (255, 255, 0) if active_field == "new_name" else (255, 255, 255)
        pygame.draw.rect(screen, name_color, input_rect_newname, 2)
        new_text = font.render(new_name, True, (255, 255, 255))
        screen.blit(new_text, (input_rect_newname.x + 5, input_rect_newname.y + 5))
        
        # Zeichne den blinkenden Cursor im aktiven Feld
        if active_field == "new_name":
            cursor_x = input_rect_newname.x + 5 + new_text.get_width()
            cursor_y = input_rect_newname.y + 5
            if (pygame.time.get_ticks() // 500) % 2:  # Blinken alle 500ms
                pygame.draw.line(screen, (255, 255, 255),
                               (cursor_x, cursor_y),
                               (cursor_x, cursor_y + new_text.get_height()))
        
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
                        req = {
                            'command': 'recruit_gladiator',
                            'user_id': user_id,
                            'name': new_name,
                            'type': selected_type
                        }
                        response = send_request(req)
                        if response and response.get('status') == 'success':
                            currency = response.get('currency', currency)
                            gladiators = fetch_gladiators()
                            new_name = ""
                        else:
                            print("Fehler beim Rekrutieren:", response.get('message') if response else "Keine Antwort vom Server")
                elif button_rect_back.collidepoint(mouse_pos):
                    currency = get_currency(user_id)
                    return currency
            if event.type == pygame.KEYDOWN:
                if active_field == "new_name":
                    if event.key == pygame.K_BACKSPACE:
                        new_name = new_name[:-1]
                    elif event.key == pygame.K_RETURN:
                        if new_name.strip() != "":
                            req = {
                                'command': 'recruit_gladiator',
                                'user_id': user_id,
                                'name': new_name,
                                'type': selected_type
                            }
                            response = send_request(req)
                            if response and response.get('status') == 'success':
                                currency = response.get('currency', currency)
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
    Kampfvorbereitung: Beim Betreten wird die Gladiatorenliste einmalig abgerufen.
    Zusätzlich gibt es ein Eingabefeld für den Wetteinsatz (nur ganze Zahlen).
    Wenn ein Fight-Button gedrückt wird, wird join_fight mit Gladiator-ID und Wetteinsatz aufgerufen.
    """
    clock = pygame.time.Clock()
    background = AnimatedBackground(
        resource_path('assets/LoginBackground'),
        'ezgif-frame-{:03d}.png',
        28,
        target_size=(800, 600),
        frame_delay=100
    )
    
    response = send_request({'command': 'get_gladiators', 'user_id': user_id})
    if response and response.get('status') == 'success':
        gladiators = response['gladiators']
        fight_buttons = []
        for i, g in enumerate(gladiators):
            y_pos = 50 + (i * 70)
            fight_button = Fight_s_Button(pos=(600, y_pos))
            fight_buttons.append((fight_button, g))
    else:
        gladiators = []
        fight_buttons = []
    
    # Eingabefeld für den Wetteinsatz (unten mittig)
    input_rect_bet = pygame.Rect(300, screen.get_height()-100, 200, 40)
    bet_value = ""
    active_field = None
    back_button_rect = pygame.Rect(50, screen.get_height()-50, 100, 30)
    
    while True:
        background.update()
        background.draw(screen)
        
        if response and response.get('status') == 'success':
            for button, g in fight_buttons:
                y_pos = 50 + (fight_buttons.index((button, g)) * 70)
                text = font.render(
                    f"{g['name']} ({g['gladiator_type']}) | LP: {g['lebenspunkte']}, A: {g['angriff']}, V: {g['verteidigung']}, E: {g['ausdauer']}",
                    True, (255,255,255)
                )
                screen.blit(text, (50, y_pos+10))
                button.draw(screen)
        
        # Zeichne das Wetteinsatz-Eingabefeld mit unterschiedlichen Farben für aktiv/inaktiv
        bet_color = (255, 255, 0) if active_field == "bet" else (255, 255, 255)
        pygame.draw.rect(screen, bet_color, input_rect_bet, 2)
        bet_text = font.render("Wette: " + (bet_value if bet_value != "" else "0"), True, (255,215,0))
        bet_rect = bet_text.get_rect(center=(input_rect_bet.centerx, input_rect_bet.centery))
        screen.blit(bet_text, bet_rect)
        
        # Zeichne den blinkenden Cursor im aktiven Feld
        if active_field == "bet":
            cursor_x = bet_rect.right + 5
            cursor_y = bet_rect.y
            if (pygame.time.get_ticks() // 500) % 2:  # Blinken alle 500ms
                pygame.draw.line(screen, (255, 255, 255),
                               (cursor_x, cursor_y),
                               (cursor_x, cursor_y + bet_text.get_height()))
        
        draw_button_wrapper("Zurück", back_button_rect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if input_rect_bet.collidepoint(mouse_pos):
                    active_field = "bet"
                else:
                    active_field = None
                for button, g in fight_buttons:
                    if button.rect.collidepoint(mouse_pos):
                        try:
                            bet_int = int(bet_value) if bet_value != "" else 0
                        except:
                            bet_int = 0
                        join_fight(user_id, g['id'], bet_int)
                        return
                if back_button_rect.collidepoint(mouse_pos):
                    return
            if event.type == pygame.KEYDOWN:
                if active_field == "bet":
                    if event.key == pygame.K_BACKSPACE:
                        bet_value = bet_value[:-1]
                    elif event.key == pygame.K_RETURN:
                        pass
                    else:
                        if event.unicode.isdigit():
                            bet_value += event.unicode
        pygame.display.flip()
        clock.tick(30)

def join_fight(user_id, gladiator_id, bet=0):
    request = {
        'command': 'join_fight',
        'user_id': user_id,
        'gladiator_id': gladiator_id,
        'bet': bet
    }
    response = send_request(request)
    if response:
        if response.get('status') == 'waiting':
            gladiator_info = response.get('gladiator', {})
            if gladiator_info:
                show_waiting_screen(gladiator_info)
            else:
                print("Fehler: Keine Gladiator-Informationen erhalten")
        elif response.get('status') == 'success':
            show_fight_result(response)
        else:
            print(f"Unerwarteter Status: {response.get('status')}")
            print(f"Fehlermeldung: {response.get('message', 'Keine Fehlermeldung')}")
    else:
        print("Keine Antwort vom Server erhalten")

def show_waiting_screen(gladiator):
    clock = pygame.time.Clock()
    background = AnimatedBackground(
        resource_path('assets/Kampf_Background'),
        'ezgif-frame-{:03d}.png',
        17,
        target_size=(800, 600),
        frame_delay=100
    )
    last_check = pygame.time.get_ticks()
    check_interval = 1000
    animation_dots = 0
    dot_update = pygame.time.get_ticks()
    message = ""
    message_timer = 0
    
    while True:
        background.update()
        background.draw(screen)
        
        text_surface = pygame.Surface((700,200))
        text_surface.set_alpha(128)
        text_surface.fill((0,0,0))
        screen.blit(text_surface,(50,30))
        
        now = pygame.time.get_ticks()
        if now - dot_update > 500:
            animation_dots = (animation_dots + 1) % 4
            dot_update = now
        
        title_text = f"Warte auf Gegner{'.' * animation_dots}"
        title_shadow = font.render(title_text, True, (0,0,0))
        title = font.render(title_text, True, (255,215,0))
        screen.blit(title_shadow, (52,52))
        screen.blit(title, (50,50))
        
        glad_info = f"{gladiator['gladiator_name']} ({gladiator['gladiator_type']})"
        info_text = font.render(glad_info, True, (255,255,255))
        screen.blit(info_text, (50,100))
        
        stats_text = font.render(
            f"❤️ LP: {gladiator['lebenspunkte']}  ⚔️ A: {gladiator['angriff']}  🛡️ V: {gladiator['verteidigung']}  💪 E: {gladiator['ausdauer']}",
            True, (255,255,255)
        )
        screen.blit(stats_text, (50,150))
        
        # Zeige Nachricht an
        if message:
            msg_surf = font.render(message, True, (255,215,0))
            screen.blit(msg_surf, (50,200))
            if pygame.time.get_ticks() - message_timer > 2000:  # Nachricht für 2 Sekunden anzeigen
                return
        
        cancel_button_rect = pygame.Rect(50, screen.get_height()-50, 150, 40)
        shadow_rect = cancel_button_rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        pygame.draw.rect(screen, (0,0,0), shadow_rect, border_radius=5)
        pygame.draw.rect(screen, (139,0,0), cancel_button_rect, border_radius=5)
        text_surf = font.render("Abbrechen", True, (255,255,255))
        text_rect = text_surf.get_rect(center=cancel_button_rect.center)
        screen.blit(text_surf, text_rect)
        
        current_time = pygame.time.get_ticks()
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
                        error_text = font.render(response.get('message', 'Fehler aufgetreten'), True, (255,0,0))
                        screen.blit(error_text, (50,200))
                        pygame.display.flip()
                        pygame.time.wait(2000)
                        return
            except Exception as e:
                print("Fehler beim Prüfen des Kampfstatus:", e)
                error_text = font.render("Verbindungsfehler, versuche erneut...", True, (255,0,0))
                screen.blit(error_text, (50,200))
                pygame.display.flip()
                pygame.time.wait(1000)
            last_check = current_time
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if cancel_button_rect.collidepoint(event.pos):
                    try:
                        response = send_request({'command': 'cancel_fight', 'gladiator_id': gladiator['gladiator_id']})
                        if response and response.get('status') == 'success':
                            message = response.get('message', 'Kampf abgebrochen')
                            message_timer = pygame.time.get_ticks()
                        else:
                            message = "Fehler beim Abbrechen des Kampfes"
                            message_timer = pygame.time.get_ticks()
                    except Exception as e:
                        print("Fehler beim Abbrechen des Kampfes:", e)
                        return
        
        pygame.display.flip()
        clock.tick(30)

def show_fight_result(result):
    print("Zeige Kampfergebnis:", result)
    clock = pygame.time.Clock()
    scroll_offset = 0
    max_scroll = 0
    background = AnimatedBackground(
        resource_path('assets/Kampf_Background'),
        'ezgif-frame-{:03d}.png',
        17,
        target_size=(800,600),
        frame_delay=100
    )
    
    if not result.get('fight_log'):
        winner = result.get('winner',{})
        loser = result.get('loser',{})
        result['fight_log'] = [
            f"Kampf zwischen {winner.get('gladiator_name')} und {loser.get('gladiator_name')}",
            "",
            f"{winner.get('gladiator_name')} ({winner.get('gladiator_type')})",
            f"LP: {winner.get('lebenspunkte')}, A: {winner.get('angriff')}, V: {winner.get('verteidigung')}, E: {winner.get('ausdauer')}",
            "",
            f"{loser.get('gladiator_name')} ({loser.get('gladiator_type')})",
            f"LP: {loser.get('lebenspunkte')}, A: {loser.get('angriff')}, V: {loser.get('verteidigung')}, E: {loser.get('ausdauer')}",
            "",
            result.get('message','Kampf beendet!')
        ]
    
    while True:
        background.update()
        background.draw(screen)
        
        text_surface = pygame.Surface((700,450))
        text_surface.set_alpha(128)
        text_surface.fill((0,0,0))
        screen.blit(text_surface,(50,30))
        
        title_shadow = font.render(result.get('message','Kampf beendet!'), True, (0,0,0))
        title = font.render(result.get('message','Kampf beendet!'), True, (255,215,0))
        screen.blit(title_shadow,(52,52))
        screen.blit(title,(50,50))
        
        y_pos = 100 - scroll_offset
        if result.get('fight_log'):
            for log_entry in result['fight_log']:
                if y_pos >= 100 and y_pos < screen.get_height()-100:
                    text = font.render(str(log_entry), True, (255,255,255))
                    screen.blit(text,(60,y_pos))
                y_pos += 30
            max_scroll = max(0, len(result['fight_log'])*30 - (screen.get_height()-200))
        else:
            text = font.render("Kein Kampfprotokoll verfügbar", True, (255,255,255))
            screen.blit(text,(60,y_pos))
        
        back_button_rect = pygame.Rect(50, screen.get_height()-50, 150, 40)
        shadow_rect = back_button_rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        pygame.draw.rect(screen, (0,0,0), shadow_rect, border_radius=5)
        pygame.draw.rect(screen, (139,0,0), back_button_rect, border_radius=5)
        text_surf = font.render("Zurück", True, (255,255,255))
        text_rect = text_surf.get_rect(center=back_button_rect.center)
        screen.blit(text_surf, text_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    scroll_offset = max(0, scroll_offset-30)
                elif event.button == 5:
                    scroll_offset = min(max_scroll, scroll_offset+30)
                elif back_button_rect.collidepoint(event.pos):
                    return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    scroll_offset = max(0, scroll_offset-30)
                elif event.key == pygame.K_DOWN:
                    scroll_offset = min(max_scroll, scroll_offset+30)
        clock.tick(30)

def main():
    user_id, username, currency = login_screen()
    main_menu(user_id, username, currency)

def main_menu(user_id, username, currency):
    """
    Hauptmenü: Beim Aufrufen wird der aktuelle Guthabenstand aus der DB einmalig abgefragt.
    Danach werden keine kontinuierlichen Updates durchgeführt.
    """
    currency = get_currency(user_id)
    
    clock = pygame.time.Clock()
    music_button = MusicButton(pos=(690, 10))
    fight_button = FightButton(pos=(400, 320))
    gladiator_button = GladiatorButton(pos=(200, 320))
    
    background = AnimatedBackground(
        resource_path('assets/LoginBackground'),
        'ezgif-frame-{:03d}.png',
        28,
        target_size=(800,600),
        frame_delay=100
    )
    
    title_frames = []
    for i in range(8):
        frame = pygame.image.load(resource_path(os.path.join('assets/titel_Hauptmenu', f'sprite_{i}.png'))).convert_alpha()
        title_frames.append(frame)
    current_title_frame = 0
    title_frame_delay = 150
    last_title_update = pygame.time.get_ticks()
    
    while True:
        background.update()
        background.draw(screen)
        
        now = pygame.time.get_ticks()
        if now - last_title_update > title_frame_delay:
            current_title_frame = (current_title_frame + 1) % len(title_frames)
            last_title_update = now
        
        title_frame = title_frames[current_title_frame]
        title_rect = title_frame.get_rect(center=(400,100))
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
                currency = gladiator_screen(user_id, currency)
                currency = get_currency(user_id)
            elif fight_button.handle_event(event):
                fight_setup_screen(user_id)
                currency = get_currency(user_id)
            elif music_button.handle_event(event):
                # Kein zusätzliches toggle_music() hier, da es bereits im Button-Handler aufgerufen wird.
                pass
        
        pygame.display.flip()
        clock.tick(30)

if __name__ == '__main__':
    main()
