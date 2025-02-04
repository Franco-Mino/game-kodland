import pygame

# Inicializar pygame
pygame.init()

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Dimensiones de la pantalla
WIDTH = 900
HEIGHT = 800
FPS = 60

# Estados del juego
MENU = "menu"
PLAYING = "playing"
INSTRUCTIONS = "instructions"
GAME_OVER = "game_over"

# Fuentes
font = pygame.font.SysFont("Arial", 30)
