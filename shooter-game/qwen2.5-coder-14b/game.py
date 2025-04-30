import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Game settings
PLAYER_SPEED = 5
ENEMY_SPEED = 3
BULLET_SPEED = 10

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Side-Scrolling Shooter")

# Load images
player_img = pygame.image.load('player.png')
enemy_img = pygame.image.load('enemy.png')
bullet_img = pygame.image.load('bullet.png')

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED
        if keys[pygame.K_SPACE]:
            self.shoot()

        # Keep player on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedx = ENEMY_SPEED

    def update(self):
        self.rect.y += self.speedx
        if self.rect.top > SCREEN_HEIGHT + 10:
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -BULLET_SPEED

    def update(self):
        self.rect.y += self.speedy
        # Kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

# Create sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Add player to all sprites group
player = Player()
all_sprites.add(player)

# Add enemies to all sprites and enemies group
for i in range(8):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Game loop
running = True
clock = pygame.time.Clock()
score = 0

while running:
    clock.tick(60)  # Limit frames per second

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update all sprites
    all_sprites.update()

    # Check for bullet collisions with enemies
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        score += 10  # Give points when enemy is hit
        enemy = Enemy()  # Replace the enemy that was destroyed
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Check for player collisions with enemies
    hits = pygame.sprite.spritecollide(player, enemies, False)
    if hits:
        running = False

    # Draw everything
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # Display score
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, GREEN)
    screen.blit(text, (10, 10))

    pygame.display.flip()

pygame.quit()
