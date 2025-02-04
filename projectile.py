# projectile.py
import pygame
import math
from constantes import *
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, is_enemy=False):
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, WHITE, (5, 5), 5)  # Forma de círculo
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 7
        self.angle = angle
        self.is_enemy = is_enemy

    def update(self):
        # Movimiento según el ángulo
        self.rect.x += self.speed * math.cos(self.angle)
        self.rect.y += self.speed * math.sin(self.angle)

        if self.rect.bottom < 0 or self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.kill()
