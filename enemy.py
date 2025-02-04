import pygame
import random
import math
from projectile import Projectile  # Importamos la clase Projectile
from constantes import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.color = RED
        self.create_triangle(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = random.randint(1, 3)  # Enemigos más lentos
        self.shoot_timer = 0  # Temporizador para los disparos

    def create_triangle(self, color):
        self.image.fill((0, 0, 0, 0))  # Limpiar la imagen
        points = [(0, 50), (25, 0), (50, 50)]  # Triángulo equilátero
        pygame.draw.polygon(self.image, color, points)

    def update(self, player, all_sprites, enemy_projectiles):
        # Movimiento hacia el jugador (más lento)
        if self.rect.centerx < player.rect.centerx:
            self.rect.x += self.speed
        elif self.rect.centerx > player.rect.centerx:
            self.rect.x -= self.speed
        if self.rect.centery < player.rect.centery:
            self.rect.y += self.speed
        elif self.rect.centery > player.rect.centery:
            self.rect.y -= self.speed

        # Disparar cada 1 segundo
        self.shoot_timer += 1
        if self.shoot_timer >= FPS:  # 1 segundo
            self.shoot(player, all_sprites, enemy_projectiles)
            self.shoot_timer = 0

    def shoot(self, player, all_sprites, enemy_projectiles):
        # Disparar hacia la posición del jugador
        angle = math.atan2(player.rect.centery - self.rect.centery, player.rect.centerx - self.rect.centerx)
        projectile = Projectile(self.rect.centerx, self.rect.centery, angle, is_enemy=True)
        all_sprites.add(projectile)
        enemy_projectiles.add(projectile)
