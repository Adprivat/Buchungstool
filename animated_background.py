import pygame
import os
from utils import resource_path

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
            frame_pattern: Muster für die Dateinamen (z.B. 'frame_{:03d}.png')
            frame_count: Anzahl der Frames
            target_size: Optional, Tuple (width, height) für die Zielgröße
            frame_delay: Verzögerung zwischen den Frames in Millisekunden
        """
        self.frames = []
        for i in range(frame_count):
            frame = pygame.image.load(os.path.join(folder_path, frame_pattern.format(i+1))).convert()
            if target_size:
                frame = pygame.transform.scale(frame, target_size)
            self.frames.append(frame)
        
        self.current_frame = 0
        self.frame_count = frame_count
        self.frame_delay = frame_delay
        self.last_update = pygame.time.get_ticks()

    def update(self):
        """
        Aktualisiert den aktuellen Frame basierend auf der verstrichenen Zeit.
        """
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_delay:
            self.current_frame = (self.current_frame + 1) % self.frame_count
            self.last_update = now

    def draw(self, surface):
        """
        Zeichnet den aktuellen Frame auf die angegebene Oberfläche.
        
        Args:
            surface: Die Pygame-Oberfläche, auf die gezeichnet werden soll
        """
        surface.blit(self.frames[self.current_frame], (0, 0))