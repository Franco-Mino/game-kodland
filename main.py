import pygame
from constantes import *
from player import Player
from enemy import Enemy
from projectile import Projectile
import random

# Inicializar pygame
pygame.init()

# Configuración de la ventana
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Disparos")
clock = pygame.time.Clock()


def draw_text(text, x, y, color):
    font = pygame.font.Font(None, 36)  # Adjusta el tamaño de la fuente
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def draw_menu(screen):
    screen.fill(BLACK)
    menu_items = [
        ("Jugar", HEIGHT // 2),
        ("Instrucciones", HEIGHT // 2 + 40),
        ("Salir", HEIGHT // 2 + 80)
    ]
    draw_text("Menú Principal", WIDTH // 2 - 100, HEIGHT // 3, WHITE)
    for text, y in menu_items:
        draw_text(text, WIDTH // 2 - 100, y, WHITE)


def draw_instructions(screen):
    screen.fill(BLACK)
    left_margin = 50
    vertical_spacing = 40
    initial_y = 50
    instructions = [
        "Instrucciones",
        "",
        "Controles:",
        "W: Mover arriba",
        "A: Mover izquierda",
        "S: Mover abajo",
        "D: Mover derecha",
        "Espacio: Disparar",
        "",
        "Objetivo:",
        "Evita los enemigos y sus disparos",
        "Elimina 10 enemigos para ganar",
        "",
        "Presiona ESC para volver al menú"
    ]
    current_y = initial_y
    for line in instructions:
        text_surface = font.render(line, True, WHITE)
        screen.blit(text_surface, (left_margin, current_y))
        current_y += vertical_spacing


def draw_game_over(screen, enemies_killed):
    screen.fill(BLACK)

    # Mensaje y color según el resultado
    if enemies_killed >= 10:
        victory_text = "FELICITACIONES GANASTE!"
        enemies_text = f"Enemigos eliminados: {enemies_killed}"
        return_text = "Presiona ESC para volver al menú"
        text_color = GREEN  # Color para ganar
    else:
        victory_text = "BUEN INTENTO! NO TE RINDAS"
        enemies_text = f"Enemigos eliminados: {enemies_killed}"
        return_text = "Presiona ESC para volver al menú"
        text_color = RED    # Color para perder

    # Centrar el texto y dibujarlo
    draw_text(victory_text, (WIDTH // 2) - (text_width(victory_text) // 2), HEIGHT // 3, text_color)
    draw_text(enemies_text, (WIDTH // 2) - (text_width(enemies_text) // 2), HEIGHT // 2, WHITE)
    draw_text(return_text, (WIDTH // 2) - (text_width(return_text) // 2), HEIGHT - 50, WHITE)

def text_width(text):
    """ Devuelve el ancho del texto en píxeles.
        Asegúrate de que usas un objeto fuente de Pygame.
    """
    font = pygame.font.Font(None, 36)  # Asegúrate de que la fuente sea la misma que usas en draw_text
    return font.size(text)[0]



def main():
    global all_sprites, player_projectiles, enemy_projectiles

    # Inicializar sprites y variables del juego
    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    player_projectiles = pygame.sprite.Group()
    enemy_projectiles = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    game_state = MENU
    enemies_killed = 0
    spawn_timer = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if game_state in [INSTRUCTIONS, PLAYING, GAME_OVER]:
                        game_state = MENU
                if event.key == pygame.K_SPACE and game_state == PLAYING:
                    player.shoot(all_sprites, player_projectiles)
            if event.type == pygame.MOUSEBUTTONDOWN and game_state == MENU:
                mouse_pos = pygame.mouse.get_pos()
                if WIDTH // 2 - 100 <= mouse_pos[0] <= WIDTH // 2 + 100:
                    if HEIGHT // 2 <= mouse_pos[1] <= HEIGHT // 2 + 40:
                        # Reiniciar el juego
                        player = Player()
                        all_sprites = pygame.sprite.Group()
                        all_sprites.add(player)
                        player_projectiles = pygame.sprite.Group()
                        enemies = pygame.sprite.Group()
                        enemy_projectiles = pygame.sprite.Group()
                        enemies_killed = 0
                        game_state = PLAYING
                    elif HEIGHT // 2 + 40 <= mouse_pos[1] <= HEIGHT // 2 + 80:
                        game_state = INSTRUCTIONS
                    elif HEIGHT // 2 + 80 <= mouse_pos[1] <= HEIGHT // 2 + 120:
                        running = False

        if game_state == MENU:
            draw_menu(screen)

        elif game_state == INSTRUCTIONS:
            draw_instructions(screen)

        elif game_state == PLAYING:
            screen.fill(BLACK)

            # Spawnear enemigos
            spawn_timer += 1
            if spawn_timer > 60:
                spawn_timer = 0
                x, y = random.choice([
                    (random.randint(0, WIDTH), 0),
                    (random.randint(0, WIDTH), HEIGHT),
                    (0, random.randint(0, HEIGHT)),
                    (WIDTH, random.randint(0, HEIGHT))
                ])
                enemy = Enemy(x, y)
                all_sprites.add(enemy)
                enemies.add(enemy)

            # Actualizar
            keys = pygame.key.get_pressed()
            player.update(keys)

            for enemy in enemies:
                enemy.update(player, all_sprites, enemy_projectiles)

            player_projectiles.update()
            enemy_projectiles.update()

            # Colisiones de proyectiles con enemigos
            for enemy in enemies:
                if pygame.sprite.spritecollide(enemy, player_projectiles, True):
                    enemy.kill()
                    enemies_killed += 1

            # Colisión de proyectiles enemigos con el jugador
            if pygame.sprite.spritecollide(player, enemy_projectiles, True):
                game_state = GAME_OVER

            # Colisión del jugador con los enemigos
            if pygame.sprite.spritecollide(player, enemies, False):
                game_state = GAME_OVER

            # Victoria
            if enemies_killed >= 10:
                game_state = GAME_OVER

            all_sprites.draw(screen)
            draw_text(f"Enemigos eliminados: {enemies_killed}", 10, 10, WHITE)

        elif game_state == GAME_OVER:
            draw_game_over(screen, enemies_killed)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()