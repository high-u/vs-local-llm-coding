import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gradius Clone")

# Clock to control frame rate
clock = pygame.time.Clock()
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Load images
player_img = pygame.Surface((40, 40))
player_img.fill(WHITE)
enemy_img = pygame.Surface((30, 30))
enemy_img.fill(RED)

bullet_img = pygame.Surface((5, 10))
bullet_img.fill(WHITE)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed = 5

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speed = 2

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

# Sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

def spawn_enemies():
    for i in range(5):
        x = random.randint(0, WIDTH)
        y = random.randint(-100, -40)
        enemy = Enemy(x, y)
        all_sprites.add(enemy)
        enemies.add(enemy)

# Game loop
running = True
spawn_timer = 0
score = 0

while running:
    clock.tick(FPS)
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key input
    keys = pygame.key.get_pressed()
    player.update(keys)

    # Shooting bullets (spacebar)
    if keys[pygame.K_SPACE]:
        bullet = Bullet(player.rect.centerx, player.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

    # Spawn enemies every few seconds
    spawn_timer += 1
    if spawn_timer > 60:
        spawn_enemies()
        spawn_timer = 0

    # Update sprites
    all_sprites.update()

    # Collision detection: bullet and enemy
    for bullet in bullets:
        hits = pygame.sprite.spritecollide(bullet, enemies, True)
        for hit in hits:
            score += 10
            bullet.kill()

    # Draw everything
    all_sprites.draw(screen)

    # Score display
    font = pygame.font.SysFont(None, 36)
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

    # Update display
    pygame.display.flip()

pygame.quit()
