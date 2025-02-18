import pygame
import sys
import os
from utils import toggle_music, send_request, draw_button, music_on

class RegistrationScreen:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        # Lade die Bilder und skaliere sie auf Fenstergröße
        self.frames = []
        for i in range(1, 29):
            frame = pygame.image.load(os.path.join('assets/LoginBackground', f'ezgif-frame-{i:03d}.png')).convert()
            self.frames.append(pygame.transform.scale(frame, (800, 600)))
        self.current_frame = 0
        self.frame_delay = 100  # milliseconds
        self.last_update = pygame.time.get_ticks()

def show_registration_screen(screen, font):
    registration = RegistrationScreen(screen, font)
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
        now = pygame.time.get_ticks()
        if now - registration.last_update > registration.frame_delay:
            registration.current_frame = (registration.current_frame + 1) % len(registration.frames)
            registration.last_update = now
        
        screen.blit(registration.frames[registration.current_frame], (0, 0))
        title = font.render("Registrierung", True, (255,255,255))
        screen.blit(title, (320,100))
        pygame.draw.rect(screen, (255,255,255), input_rect_username, 2)
        pygame.draw.rect(screen, (255,255,255), input_rect_password, 2)
        user_text = font.render(username, True, (255,255,255))
        pass_text = font.render("*"*len(password), True, (255,255,255))
        screen.blit(user_text, (input_rect_username.x+5, input_rect_username.y+5))
        screen.blit(pass_text, (input_rect_password.x+5, input_rect_password.y+5))
        draw_button(screen, font, "Registrieren", button_rect_register)
        draw_button(screen, font, "Zurück", button_rect_back)
        if music_on:
            draw_button(screen, font, "Musik aus", music_button_rect, color=(180,80,80))
        else:
            draw_button(screen, font, "Musik an", music_button_rect, color=(80,180,80))
        if message:
            msg_surf = font.render(message, True, (255,215,0))
            screen.blit(msg_surf, (300,150))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
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