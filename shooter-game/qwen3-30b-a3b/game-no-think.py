import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gradius Clone")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Clock and FPS
clock = pygame.time.Clock()
FPS = 60

# Fonts
font = pygame.font.SysFont("Arial", 24)

# Player settings
player_width = 40
player_height = 20
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 50
player_speed = 5

# Bullet settings
bullet_width = 4
bullet_height = 10
bullet_speed = 7
bullets = []

# Enemy settings
enemy_width = 30
enemy_height = 20
enemy_speed = 2
enemies = []
enemy_spawn_timer = 0
ENEMY_SPAWN_INTERVAL = 60

# Score
score = 0

def draw_player(x, y):
    pygame.draw.rect(screen, WHITE, (x, y, player_width, player_height))

def draw_bullets(bullets):
    for bullet in bullets:
        pygame.draw.rect(screen, RED, (*bullet, bullet_width, bullet_height))

def draw_enemies(enemies):
    for enemy in enemies:
        pygame.draw.rect(screen, RED, (*enemy, enemy_width, enemy_height))

def draw_score(score):
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

# Main game loop
running = True
while running:
    clock.tick(FPS)
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_speed
    if keys[pygame.K_SPACE]:
        bullets.append(pygame.Rect(player_x + player_width // 2 - bullet_width // 2, player_y, bullet_width, bullet_height))

    # Spawn enemies
    enemy_spawn_timer += 1
    if enemy_spawn_timer > ENEMY_SPAWN_INTERVAL:
        x = WIDTH
        y = random.randint(0, HEIGHT - enemy_height)
        enemies.append(pygame.Rect(x, y, enemy_width, enemy_height))
        enemy_spawn_timer = 0

    # Move bullets
    for bullet in bullets[:]:
        bullet.y -= bullet_speed
        if bullet.top < 0:
            bullets.remove(bullet)

    # Move enemies
    for enemy in enemies[:]:
        enemy.x -= enemy_speed
        if enemy.right < 0:
            enemies.remove(enemy)
        else:
            # Check collision with player
            if enemy.colliderect(pygame.Rect(player_x, player_y, player_width, player_height)):
                print("Game Over!")
                running = False

    # Check bullet vs enemy collisions
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.colliderect(enemy):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 10
                break

    # Draw everything
    draw_player(player_x, player_y)
    draw_bullets(bullets)
    draw_enemies(enemies)
    draw_score(score)

    pygame.display.flip()

pygame.quit()
sys.exit()
