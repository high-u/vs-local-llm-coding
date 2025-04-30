import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gradius-like Shooter")

# Clock to control the frame rate of our game
clock = pygame.time.Clock()

# Load images for player and bullets
player_image = pygame.Surface((50, 40))  # Placeholder for actual image
player_image.fill(WHITE)
player_rect = player_image.get_rect()
player_rect.centerx, player_rect.centery = SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100

bullet_image = pygame.Surface((5, 10))
bullet_image.fill(WHITE)
bullets = []

# Player movement variables
player_speed = 300  # pixels per second

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Fire bullet on spacebar press
                bullet_rect = bullet_image.get_rect(center=player_rect.center)
                bullets.append(bullet_rect)

    # Get keys pressed and update player position
    keys = pygame.key.get_pressed()
    dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
    dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]

    # Move the player
    player_rect.x += dx * player_speed * clock.get_time() / 1000.0
    player_rect.y += dy * player_speed * clock.get_time() / 1000.0

    # Keep player on screen
    player_rect.clamp_ip(screen.get_rect())

    # Update bullet positions
    for bullet in bullets[:]:
        bullet.y -= 500 * clock.get_time() / 1000.0  # Move bullets upwards
        if bullet.top < 0:  # If a bullet goes off the top of the screen, remove it
            bullets.remove(bullet)

    # Fill the screen with black color
    screen.fill(BLACK)

    # Draw player and bullets on screen
    screen.blit(player_image, player_rect)
    for bullet in bullets:
        screen.blit(bullet_image, bullet)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate at 60 frames per second
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
