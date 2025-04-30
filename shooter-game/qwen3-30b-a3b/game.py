import pygame
import sys
import random

pygame.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gradius Clone")
clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 20))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed = 5
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 200

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        # Keep within screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

# Bullet class (player)
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(WHITE)
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
        self.image = pygame.Surface((30, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2

    def update(self):
        self.rect.x += self.speed
        if self.rect.right > WIDTH or self.rect.left < 0:
            self.speed *= -1
            self.rect.y += 10

    def shoot(self):
        bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
        all_sprites.add(bullet)
        enemy_bullets.add(bullet)

# Enemy Bullet class
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

# Power-Up class
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

# Initialize groups
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
powerups = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

# Create enemies
for i in range(5):
    enemy = Enemy(i * 100 + 100, 50)
    all_sprites.add(enemy)
    enemies.add(enemy)

# Main game loop
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle shooting
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        now = pygame.time.get_ticks()
        if now - player.last_shot > player.shoot_delay:
            player.shoot()
            player.last_shot = now

    # Update all sprites
    all_sprites.update()

    # Handle enemy shooting
    for enemy in enemies:
        if random.random() < 0.01:  # 1% chance to shoot each frame
            enemy.shoot()

    # Check collisions between bullets and enemies
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        powerup = PowerUp(hit.rect.centerx, hit.rect.centery)
        all_sprites.add(powerup)
        powerups.add(powerup)

    # Check collisions between player and power-ups
    powerup_hits = pygame.sprite.spritecollide(player, powerups, True)
    for powerup in powerup_hits:
        player.speed += 1  # Increase speed temporarily

    # Check collisions between player and enemy bullets
    player_hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
    for hit in player_hits:
        print("Player hit!")

    # Update enemy bullets
    enemy_bullets.update()

    # Draw everything
    screen.fill(BLACK)
    all_sprites.draw(screen)
    enemy_bullets.draw(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()
