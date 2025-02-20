import pygame
import utils

class ImageButton:
    def __init__(self, image_path, pos, frame_size=(96, 96), pressed_offset=(0, 96)):
        """
        image_path: Pfad zum Bild (z. B. "assets/buttons/login.png")
        pos: Tuple (x, y) – Position des Buttons im Fenster
        frame_size: Tuple (width, height) – Größe eines Frames im Sprite-Sheet
        pressed_offset: Tuple (x_offset, y_offset) – Offset für den gedrückten Zustand.
                        Wird z. B. verwendet, wenn der gedrückte Zustand unter dem Normalzustand liegt.
        """
        self.image_full = pygame.image.load(utils.resource_path(image_path)).convert_alpha()
        self.frame_size = frame_size
        self.pressed_offset = pressed_offset
        self.normal_frame = pygame.Surface(frame_size, pygame.SRCALPHA)
        self.pressed_frame = pygame.Surface(frame_size, pygame.SRCALPHA)
        self.normal_frame.blit(self.image_full, (0, 0), (0, 0, *frame_size))
        self.pressed_frame.blit(self.image_full, (0, 0), (pressed_offset[0], pressed_offset[1], *frame_size))
        self.rect = pygame.Rect(pos[0], pos[1], frame_size[0], frame_size[1])
        self.is_pressed = False

    def draw(self, surface):
        if self.is_pressed:
            surface.blit(self.pressed_frame, self.rect.topleft)
        else:
            surface.blit(self.normal_frame, self.rect.topleft)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.is_pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.is_pressed and self.rect.collidepoint(event.pos):
                self.is_pressed = False
                return True  # Button wurde geklickt
            self.is_pressed = False
        return False

class MusicButton:
    def __init__(self, pos, size=(100, 30)):
        self.rect = pygame.Rect(pos, size)

    def draw(self, surface, font):
        from utils import music_on
        if music_on:
            pygame.draw.rect(surface, (80, 180, 80), self.rect)  # Grün wenn Musik an
            text_surf = font.render("Musik aus", True, (255, 255, 255))
        else:
            pygame.draw.rect(surface, (180, 80, 80), self.rect)  # Rot wenn Musik aus
            text_surf = font.render("Musik an", True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            from utils import toggle_music
            toggle_music()
            return True
        return False

class RegisterButton(ImageButton):
    def __init__(self, pos):
        super().__init__("assets/buttons/RegButton.png", pos, frame_size=(96, 96), pressed_offset=(0, 96))

class FightButton(ImageButton):
    def __init__(self, pos):
        super().__init__("assets/buttons/KampfButton.png", pos, frame_size=(171, 118), pressed_offset=(0, 193))

class GladiatorButton(ImageButton):
    def __init__(self, pos):
        super().__init__("assets/buttons/PickGlad.png", pos, frame_size=(171, 118), pressed_offset=(0, 193))

class Fight_s_Button(ImageButton):
    def __init__(self, pos):
        super().__init__("assets/buttons/fight_button.png", pos, frame_size=(96, 96), pressed_offset=(0, 96))
