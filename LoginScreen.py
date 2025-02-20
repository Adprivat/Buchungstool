import pygame
import os
import sys
from buttons import ImageButton, MusicButton, RegisterButton
from utils import toggle_music, send_request, draw_button, resource_path
from registration_screen import show_registration_screen
from animated_background import AnimatedBackground

class LoginScreen:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.username = ""
        self.password = ""
        self.active_field = "username"
        self.input_rect_username = pygame.Rect(300, 250, 200, 40)
        self.input_rect_password = pygame.Rect(300, 320, 200, 40)
        self.login_button = ImageButton(resource_path("assets/buttons/login.png"), pos=(290, 400), frame_size=(96, 96), pressed_offset=(0, 96))
        self.register_button = RegisterButton(pos=(420, 400))
        self.music_button = MusicButton(pos=(690, 10))
        self.clock = pygame.time.Clock()
        
        # Initialisiere animierten Hintergrund
        self.background = AnimatedBackground(
            resource_path('assets/LoginBackground'),
            'ezgif-frame-{:03d}.png',
            28,
            target_size=(800, 600),
            frame_delay=100
        )
        
        # Lade die Titelbilder
        self.title_frames = []
        for i in range(8):
            frame = pygame.image.load(resource_path(os.path.join('assets/titel_Hauptmenu', f'sprite_{i}.png'))).convert_alpha()
            self.title_frames.append(frame)
        self.current_title_frame = 0
        self.title_frame_delay = 150
        self.last_title_update = pygame.time.get_ticks()

    def draw(self):
        now = pygame.time.get_ticks()
        
        # Update und zeichne den Hintergrund
        self.background.update()
        self.background.draw(self.screen)
        
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

        # Zeichne die Eingabefelder mit unterschiedlichen Farben für aktiv/inaktiv
        username_color = (255, 255, 0) if self.active_field == "username" else (255, 255, 255)
        password_color = (255, 255, 0) if self.active_field == "password" else (255, 255, 255)
        pygame.draw.rect(self.screen, username_color, self.input_rect_username, 2)
        pygame.draw.rect(self.screen, password_color, self.input_rect_password, 2)

        # Rendere Benutzereingaben
        user_text = self.font.render(self.username, True, (255, 255, 255))
        pass_text = self.font.render("*" * len(self.password), True, (255, 255, 255))
        self.screen.blit(user_text, (self.input_rect_username.x + 5, self.input_rect_username.y + 5))
        self.screen.blit(pass_text, (self.input_rect_password.x + 5, self.input_rect_password.y + 5))

        # Zeichne den Cursor im aktiven Feld
        if self.active_field == "username":
            cursor_x = self.input_rect_username.x + 5 + user_text.get_width()
            cursor_y = self.input_rect_username.y + 5
            if (now // 500) % 2:  # Blinken alle 500ms
                pygame.draw.line(self.screen, (255, 255, 255),
                               (cursor_x, cursor_y),
                               (cursor_x, cursor_y + user_text.get_height()))
        elif self.active_field == "password":
            cursor_x = self.input_rect_password.x + 5 + pass_text.get_width()
            cursor_y = self.input_rect_password.y + 5
            if (now // 500) % 2:  # Blinken alle 500ms
                pygame.draw.line(self.screen, (255, 255, 255),
                               (cursor_x, cursor_y),
                               (cursor_x, cursor_y + pass_text.get_height()))

        self.login_button.draw(self.screen)
        self.register_button.draw(self.screen)
        self.music_button.draw(self.screen, self.font)

    def try_login(self):
        """Versucht den Login mit den aktuellen Eingaben"""
        req = {'command': 'login', 'username': self.username, 'password': self.password}
        response = send_request(req)
        if response and response.get('status') == 'success':
            return response['user_id'], self.username, response['currency']
        else:
            print("Login fehlgeschlagen:", response.get('message') if response else "Keine Antwort")
            self.username = ""
            self.password = ""
            self.active_field = "username"
        return None

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if self.input_rect_username.collidepoint(mouse_pos):
                self.active_field = "username"
            elif self.input_rect_password.collidepoint(mouse_pos):
                self.active_field = "password"
            elif self.music_button.rect.collidepoint(mouse_pos):
                toggle_music()
                return None
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Enter-Taste
                return self.try_login()
            elif event.key == pygame.K_TAB:  # Tab-Taste
                self.active_field = "password" if self.active_field == "username" else "username"
            elif event.key == pygame.K_BACKSPACE:
                if self.active_field == "username":
                    self.username = self.username[:-1]
                elif self.active_field == "password":
                    self.password = self.password[:-1]
            elif event.unicode.isprintable():  # Nur druckbare Zeichen
                if self.active_field == "username":
                    self.username += event.unicode
                elif self.active_field == "password":
                    self.password += event.unicode
        
        # Handle die anderen Buttons
        if self.login_button.handle_event(event):
            return self.try_login()
        elif self.register_button.handle_event(event):
            show_registration_screen(self.screen, self.font)
            self.username = ""
            self.password = ""
            self.active_field = "username"
        
        return None
