import pygame
#test
class ImageButton:
    def __init__(self, image_path, pos, frame_size, pressed_offset=None):
        """
        image_path: Pfad zum Bild (z. B. "assets/buttons/login.png")
        pos: Tuple (x, y) – Position des Buttons im Fenster
        frame_size: Tuple (width, height) – Größe eines Frames im Sprite-Sheet
        pressed_offset: Tuple (x_offset, y_offset) – Position des gedrückten Zustands im Bild.
                        Falls None, wird angenommen, dass der gedrückte Zustand direkt unter dem Normalzustand liegt.
        """
        self.image_full = pygame.image.load(image_path).convert_alpha()
        self.frame_width, self.frame_height = frame_size
        self.rect = pygame.Rect(pos, frame_size)
        if pressed_offset is None:
            pressed_offset = (0, frame_height)
        self.pressed_offset = pressed_offset
        self.image_normal = self.image_full.subsurface(pygame.Rect(0, 0, self.frame_width, self.frame_height))
        self.image_pressed = self.image_full.subsurface(pygame.Rect(0, self.pressed_offset[1], self.frame_width, self.frame_height))
        self.pressed = False

    def draw(self, surface):
        if self.pressed:
            surface.blit(self.image_pressed, self.rect.topleft)
        else:
            surface.blit(self.image_normal, self.rect.topleft)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.pressed and self.rect.collidepoint(event.pos):
                self.pressed = False
                return True  # Button wurde geklickt
            self.pressed = False
        return False
