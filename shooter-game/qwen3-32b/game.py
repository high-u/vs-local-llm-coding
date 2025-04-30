import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gradius-like Shooter")

# Clock and fonts
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Game constants
ENEMY_SPAWN_RATE = 1000  # milliseconds between enemy spawns

# Define game classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 255, 0))  # Green square
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill((255, 255, 255))  # White rectangle
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))  # Red square
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(SCREEN_WIDTH + 10, SCREEN_WIDTH + 60)
        self.rect.y = random.randint(50, SCREEN_HEIGHT - 50)
        self.speed = random.choice([2, 3])

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()


# Initialize game objects and groups
player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()

pygame.time.set_timer(pygame.USEREVENT + 1, ENEMY_SPAWN_RATE)

score = 0
last_shot_time = 0

# Game loop
running = True
while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.USEREVENT + 1:
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

    # Shooting logic with cooldown (200 ms)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        if current_time - last_shot_time > 200:
            bullet = Bullet(player.rect.centerx, player.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            last_shot_time = current_time

    # Update
    all_sprites.update()

    # Collision between bullets and enemies
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    score += len(hits) * 10

    # Check if player is hit by enemy
    if pygame.sprite.spritecollide(player, enemies, False):
        running = False

    # Render game
    screen.fill((0, 0, 0))  # Black background
    all_sprites.draw(screen)

    # Draw score
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(60)  # Cap the frame rate at 60 FPS

pygame.quit()
