import pygame
import math
from constantes import WHITE
from projectile import Projectile  # Importamos la clase Projectile desde su archivo
from constantes import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.color = WHITE
        self.create_triangle(self.color)
        self.image = self.original_image  # Usar la imagen original
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)  # Posición inicial
        self.speed = 5

    def create_triangle(self, color):
        self.original_image.fill((0, 0, 0, 0))  # Limpiar la imagen
        points = [(50, 25), (0, 0), (0, 50)]  # Triángulo orientado hacia la derecha
        pygame.draw.polygon(self.original_image, color, points)

    def update(self, keys):
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed

            # Evitar que el jugador se salga de la pantalla
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

            # Rotar hacia el mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()
        angle = math.degrees(math.atan2(mouse_y - self.rect.centery, mouse_x - self.rect.centerx))
        self.image = pygame.transform.rotate(self.original_image, -angle)  # Rotar y ajustar el ángulo
        self.rect = self.image.get_rect(center=self.rect.center)  # Mantener el centro del rectángulo

    def shoot(self, all_sprites, player_projectiles):
        # Obtener la posición del mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()
        angle = math.atan2(mouse_y - self.rect.centery, mouse_x - self.rect.centerx)

        # Calcular la posición de disparo desde la punta del triángulo
        projectile_x = self.rect.centerx + 50 * math.cos(angle)  # Ajustado a la longitud del triángulo
        projectile_y = self.rect.centery + 50 * math.sin(angle)

        projectile = Projectile(projectile_x, projectile_y, angle)
        all_sprites.add(projectile)
        player_projectiles.add(projectile)
