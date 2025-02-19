import pygame
import os

class AnimatedBackground:
    """
    Eine wiederverwendbare Klasse für animierte Hintergründe.
    Unterstützt das Laden und Animieren von Sprite-Sequenzen.
    """
    def __init__(self, folder_path, frame_pattern, frame_count, target_size=None, frame_delay=100):
        """
        Initialisiert einen animierten Hintergrund.
        
        Args:
            folder_path: Pfad zum Ordner mit den Frame-Bildern
            frame_pattern: Muster für die Dateinamen (z.B. 'ezgif-frame-{:03d}.png')
            frame_count: Anzahl der Frames
            target_size: Optional, Tuple (width, height) für die Zielgröße
            frame_delay: Verzögerung zwischen Frames in Millisekunden
        """
        self.frames = []
        for i in range(1, frame_count + 1):
            frame = pygame.image.load(os.path.join(folder_path, frame_pattern.format(i))).convert()
            if target_size:
                frame = pygame.transform.scale(frame, target_size)
            self.frames.append(frame)
        
        self.current_frame = 0
        self.frame_delay = frame_delay
        self.last_update = pygame.time.get_ticks()

    def update(self):
        """
        Aktualisiert den aktuellen Frame basierend auf der verstrichenen Zeit.
        """
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_delay:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_update = now

    def draw(self, surface, position=(0, 0)):
        """
        Zeichnet den aktuellen Frame auf die angegebene Oberfläche.
        
        Args:
            surface: Die Pygame-Oberfläche, auf die gezeichnet werden soll
            position: Optional, Tuple (x, y) für die Position
        """
        surface.blit(self.frames[self.current_frame], position)