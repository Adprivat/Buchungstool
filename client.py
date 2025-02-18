#!/usr/bin/env python3
import pygame
import socket
import json
import sys
from buttons import ImageButton  # Importiere die Button-Klasse aus buttons.py

SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Gladiatoren Spiel")
font = pygame.font.SysFont(None, 36)

pygame.mixer.init()
music_on = True
try:
    pygame.mixer.music.load("music/mygladiator.mp3")  # Hier ggf. anpassen – falls andere Musikdatei genutzt wird
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

def draw_button(text, rect, color=(70,130,180)):
    pygame.draw.rect(screen, color, rect)
    text_surf = font.render(text, True, (255,255,255))
    text_rect = text_surf.get_rect(center=(rect[0]+rect[2]//2, rect[1]+rect[3]//2))
    screen.blit(text_surf, text_rect)

def login_screen():
    username = ""
    password = ""
    active_field = "username"
    input_rect_username = pygame.Rect(300, 200, 200, 40)
    input_rect_password = pygame.Rect(300, 260, 200, 40)
    # Verwende den ImageButton für den Login-Button – Bild muss ein Sprite-Sheet sein mit Normal- und gedrücktem Zustand.
    # Hier nehmen wir an, dass "assets/buttons/login.png" 96x96 Pixel pro Frame hat,
    # Normalzustand oben, gedrückt unten.
    login_button = ImageButton("assets/buttons/login.png", pos=(300, 320), frame_size=(96, 96), pressed_offset=(0, 96))
    button_rect_register = pygame.Rect(300, 420, 200, 50)
    clock = pygame.time.Clock()
    music_button_rect = pygame.Rect(690, 10, 100, 30)
    
    while True:
        screen.fill((30,30,30))
        title = font.render("Gladiatoren Spiel - Login", True, (255,255,255))
        screen.blit(title, (220,100))
        pygame.draw.rect(screen, (255,255,255), input_rect_username, 2)
        pygame.draw.rect(screen, (255,255,255), input_rect_password, 2)
        user_text = font.render(username, True, (255,255,255))
        pass_text = font.render("*"*len(password), True, (255,255,255))
        screen.blit(user_text, (input_rect_username.x+5, input_rect_username.y+5))
        screen.blit(pass_text, (input_rect_password.x+5, input_rect_password.y+5))
        login_button.draw(screen)
        draw_button("Registrieren", button_rect_register)
        if music_on:
            draw_button("Musik aus", music_button_rect, color=(180,80,80))
        else:
            draw_button("Musik an", music_button_rect, color=(80,180,80))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if login_button.handle_event(event):
                req = {'command': 'login', 'username': username, 'password': password}
                response = send_request(req)
                if response and response.get('status') == 'success':
                    return response['user_id'], username, response['currency']
                else:
                    print("Login fehlgeschlagen:", response.get('message') if response else "Keine Antwort")
                    username = ""
                    password = ""
                    active_field = "username"
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if music_button_rect.collidepoint(mouse_pos):
                    toggle_music()
                elif input_rect_username.collidepoint(mouse_pos):
                    active_field = "username"
                elif input_rect_password.collidepoint(mouse_pos):
                    active_field = "password"
                elif button_rect_register.collidepoint(mouse_pos):
                    registration_screen()
                    username = ""
                    password = ""
                    active_field = "username"
            if event.type == pygame.KEYDOWN:
                if active_field == "username":
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    elif event.key == pygame.K_TAB:
                        active_field = "password"
                    else:
                        username += event.unicode
                elif active_field == "password":
                    if event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    elif event.key == pygame.K_TAB:
                        active_field = "username"
                    else:
                        password += event.unicode
        pygame.display.flip()
        clock.tick(30)

def registration_screen():
    username = ""
    password = ""
    active_field = "username"
    input_rect_username = pygame.Rect(300,200,200,40)
    input_rect_password = pygame.Rect(300,260,200,40)
    button_rect_register = pygame.Rect(300,320,200,50)
    button_rect_back = pygame.Rect(300,380,200,50)
    clock = pygame.time.Clock()
    registration_success = False
    message = ""
    music_button_rect = pygame.Rect(690,10,100,30)
    while True:
        screen.fill((30,30,30))
        title = font.render("Registrierung", True, (255,255,255))
        screen.blit(title, (320,100))
        pygame.draw.rect(screen, (255,255,255), input_rect_username, 2)
        pygame.draw.rect(screen, (255,255,255), input_rect_password, 2)
        user_text = font.render(username, True, (255,255,255))
        pass_text = font.render("*"*len(password), True, (255,255,255))
        screen.blit(user_text, (input_rect_username.x+5, input_rect_username.y+5))
        screen.blit(pass_text, (input_rect_password.x+5, input_rect_password.y+5))
        draw_button("Registrieren", button_rect_register)
        draw_button("Zurück", button_rect_back)
        if music_on:
            draw_button("Musik aus", music_button_rect, color=(180,80,80))
        else:
            draw_button("Musik an", music_button_rect, color=(80,180,80))
        if message:
            msg_surf = font.render(message, True, (255,215,0))
            screen.blit(msg_surf, (300,150))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if music_button_rect.collidepoint(mouse_pos):
                    toggle_music()
                elif input_rect_username.collidepoint(mouse_pos):
                    active_field = "username"
                elif input_rect_password.collidepoint(mouse_pos):
                    active_field = "password"
                elif button_rect_register.collidepoint(mouse_pos):
                    req = {'command': 'register', 'username': username, 'password': password}
                    response = send_request(req)
                    if response is None:
                        message = "Verbindungsfehler: Keine Antwort vom Server"
                    elif response.get('status') == 'success':
                        message = "Registrierung erfolgreich!"
                        registration_success = True
                    else:
                        message = "Fehler: " + str(response.get('message'))
                elif button_rect_back.collidepoint(mouse_pos):
                    return
            if event.type == pygame.KEYDOWN:
                if active_field == "username":
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    elif event.key == pygame.K_TAB:
                        active_field = "password"
                    else:
                        username += event.unicode
                elif active_field == "password":
                    if event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    elif event.key == pygame.K_TAB:
                        active_field = "username"
                    else:
                        password += event.unicode
        pygame.display.flip()
        clock.tick(30)
        if registration_success:
            pygame.time.delay(1500)
            return

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
        draw_button("Rekrutieren", button_rect_recruit)
        draw_button("Zurück", button_rect_back)
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
    selected_gladiator_id = None
    bet_amount_str = ""
    active_field = "bet"
    input_rect_bet = pygame.Rect(300,450,200,40)
    button_rect_start = pygame.Rect(300,500,200,50)
    button_rect_back = pygame.Rect(300,560,200,50)
    def fetch_gladiators():
        req = {'command': 'get_gladiators', 'user_id': user_id}
        response = send_request(req)
        if response and response.get('status') == 'success':
            return response.get('gladiators', [])
        else:
            return []
    gladiators = fetch_gladiators()
    gladiator_rects = []
    start_y = 60
    for i, g in enumerate(gladiators):
        rect = pygame.Rect(50, start_y + i*40, 700, 30)
        gladiator_rects.append((rect, g))
    while True:
        screen.fill((50,50,80))
        title = font.render("Kampf vorbereiten", True, (255,255,255))
        screen.blit(title, (300,20))
        for rect, g in gladiator_rects:
            if selected_gladiator_id == g['id']:
                pygame.draw.rect(screen, (0,255,0), rect)
            else:
                pygame.draw.rect(screen, (100,100,100), rect)
            text = font.render(f"ID: {g['id']} - {g['name']} (Str: {g['staerke']}, Agil: {g['agilitaet']})", True, (255,255,255))
            screen.blit(text, (rect.x+5, rect.y+5))
        prompt = font.render("Wetteinsatz:", True, (255,255,255))
        screen.blit(prompt, (300,420))
        pygame.draw.rect(screen, (255,255,255), input_rect_bet, 2)
        bet_text = font.render(bet_amount_str, True, (255,255,255))
        screen.blit(bet_text, (input_rect_bet.x+5, input_rect_bet.y+5))
        draw_button("Kampf starten", button_rect_start)
        draw_button("Zurück", button_rect_back)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for rect, g in gladiator_rects:
                    if rect.collidepoint(mouse_pos):
                        selected_gladiator_id = g['id']
                if input_rect_bet.collidepoint(mouse_pos):
                    active_field = "bet"
                elif button_rect_start.collidepoint(mouse_pos):
                    if selected_gladiator_id is None:
                        print("Kein Gladiator ausgewählt!")
                    else:
                        try:
                            bet_amount = int(bet_amount_str)
                        except ValueError:
                            print("Ungültiger Wetteinsatz!")
                            continue
                        req = {
                            'command': 'join_fight',
                            'user_id': user_id,
                            'gladiator_id': selected_gladiator_id,
                            'bet_amount': bet_amount
                        }
                        response = send_request(req)
                        if response:
                            if response.get('status') == 'waiting':
                                print("Warte auf einen Gegner...")
                            elif response.get('status') == 'success':
                                print("Kampf beendet. Gewinner User ID:", response.get('winner'), "Pot:", response.get('pot'))
                            else:
                                print("Fehler:", response.get('message'))
                        else:
                            print("Keine Antwort vom Server")
                elif button_rect_back.collidepoint(mouse_pos):
                    return
            if event.type == pygame.KEYDOWN:
                if active_field == "bet":
                    if event.key == pygame.K_BACKSPACE:
                        bet_amount_str = bet_amount_str[:-1]
                    elif event.key == pygame.K_RETURN:
                        pass
                    else:
                        bet_amount_str += event.unicode
        pygame.display.flip()
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
        draw_button("Gladiatoren verwalten", button_rect_manage)
        draw_button("Kampf beitreten", button_rect_fight)
        if music_on:
            draw_button("Musik aus", music_button_rect, color=(180,80,80))
        else:
            draw_button("Musik an", music_button_rect, color=(80,180,80))
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

def main():
    user_id, username, currency = login_screen()
    main_menu(user_id, username, currency)

if __name__ == '__main__':
    main()
