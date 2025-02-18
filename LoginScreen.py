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
        self.input_rect_username = pygame.Rect(300, 200, 200, 40)
        self.input_rect_password = pygame.Rect(300, 260, 200, 40)
        self.login_button = ImageButton("assets/buttons/login.png", pos=(350, 320), frame_size=(96, 96), pressed_offset=(0, 96))
        self.register_button = RegisterButton(pos=(350, 400))
        self.music_button = MusicButton(pos=(690, 10))
        self.clock = pygame.time.Clock()
        # Lade die Bilder und skaliere sie auf Fenstergröße
        self.frames = []
        for i in range(1, 29):
            frame = pygame.image.load(os.path.join('assets/LoginBackground', f'ezgif-frame-{i:03d}.png')).convert()
            self.frames.append(pygame.transform.scale(frame, (800, 600)))
        self.current_frame = 0
        self.frame_delay = 100  # milliseconds
        self.last_update = pygame.time.get_ticks()

    def draw(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_delay:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_update = now
        self.screen.blit(self.frames[self.current_frame], (0, 0))
        title = self.font.render("Gladiatoren Spiel - Login", True, (255, 255, 255))
        self.screen.blit(title, (220, 100))
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
