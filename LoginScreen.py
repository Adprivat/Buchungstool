import pygame
import os
import sys
from buttons import ImageButton, MusicButton, RegisterButton
from utils import toggle_music, send_request, draw_button
from registration_screen import show_registration_screen

class LoginScreen:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.username = ""
        self.password = ""
        self.active_field = "username"
        self.input_rect_username = pygame.Rect(300, 250, 200, 40)
        self.input_rect_password = pygame.Rect(300, 320, 200, 40)
        self.login_button = ImageButton("assets/buttons/login.png", pos=(290, 400), frame_size=(96, 96), pressed_offset=(0, 96))
        self.register_button = RegisterButton(pos=(410, 400))
        self.music_button = MusicButton(pos=(690, 10))
        self.clock = pygame.time.Clock()
        
        # Lade die Hintergrundbilder und skaliere sie
        self.frames = []
        for i in range(1, 29):
            frame = pygame.image.load(os.path.join('assets/LoginBackground', f'ezgif-frame-{i:03d}.png')).convert()
            self.frames.append(pygame.transform.scale(frame, (800, 600)))
        self.current_frame = 0
        self.frame_delay = 100  # milliseconds
        self.last_update = pygame.time.get_ticks()
        
        # Lade die Titelbilder
        self.title_frames = []
        for i in range(8):  # sprite_0 bis sprite_7
            frame = pygame.image.load(os.path.join('assets/titel', f'sprite_{i}.png')).convert_alpha()
            self.title_frames.append(frame)
        self.current_title_frame = 0
        self.title_frame_delay = 150  # milliseconds
        self.last_title_update = pygame.time.get_ticks()

    def draw(self):
        now = pygame.time.get_ticks()
        
        # Animiere den Hintergrund
        if now - self.last_update > self.frame_delay:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_update = now
        self.screen.blit(self.frames[self.current_frame], (0, 0))
        
        # Animiere den Titel
        if now - self.last_title_update > self.title_frame_delay:
            self.current_title_frame = (self.current_title_frame + 1) % len(self.title_frames)
            self.last_title_update = now
        
        # Zentriere den Titel
        title_frame = self.title_frames[self.current_title_frame]
        title_rect = title_frame.get_rect(center=(400, 100))
        self.screen.blit(title_frame, title_rect)

        # Beschriftungen für die Eingabefelder
        username_label = self.font.render("Benutzername:", True, (255, 255, 255))
        password_label = self.font.render("Passwort:", True, (255, 255, 255))
        self.screen.blit(username_label, (self.input_rect_username.x, self.input_rect_username.y - 30))
        self.screen.blit(password_label, (self.input_rect_password.x, self.input_rect_password.y - 30))

        # Zeichne die Eingabefelder
        pygame.draw.rect(self.screen, (255, 255, 255), self.input_rect_username, 2)
        pygame.draw.rect(self.screen, (255, 255, 255), self.input_rect_password, 2)
        user_text = self.font.render(self.username, True, (255, 255, 255))
        pass_text = self.font.render("*" * len(self.password), True, (255, 255, 255))
        self.screen.blit(user_text, (self.input_rect_username.x + 5, self.input_rect_username.y + 5))
        self.screen.blit(pass_text, (self.input_rect_password.x + 5, self.input_rect_password.y + 5))
        self.login_button.draw(self.screen)
        self.register_button.draw(self.screen)
        self.music_button.draw(self.screen, self.font)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if self.login_button.handle_event(event):
            req = {'command': 'login', 'username': self.username, 'password': self.password}
            response = send_request(req)
            if response and response.get('status') == 'success':
                return response['user_id'], self.username, response['currency']
            else:
                print("Login fehlgeschlagen:", response.get('message') if response else "Keine Antwort")
                self.username = ""
                self.password = ""
                self.active_field = "username"
        if self.register_button.handle_event(event):
            show_registration_screen(self.screen, self.font)
            self.username = ""
            self.password = ""
            self.active_field = "username"
        if self.music_button.handle_event(event):
            toggle_music()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if self.input_rect_username.collidepoint(mouse_pos):
                self.active_field = "username"
            elif self.input_rect_password.collidepoint(mouse_pos):
                self.active_field = "password"
        if event.type == pygame.KEYDOWN:
            if self.active_field == "username":
                if event.key == pygame.K_BACKSPACE:
                    self.username = self.username[:-1]
                elif event.key == pygame.K_TAB:
                    self.active_field = "password"
                else:
                    self.username += event.unicode
            elif self.active_field == "password":
                if event.key == pygame.K_BACKSPACE:
                    self.password = self.password[:-1]
                elif event.key == pygame.K_TAB:
                    self.active_field = "username"
                else:
                    self.password += event.unicode
        return None
