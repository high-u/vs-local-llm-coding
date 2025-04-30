import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Side-Scrolling Shooter")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Load images
player_image = pygame.image.load("player.png").convert_alpha()
enemy_image = pygame.image.load("enemy.png").convert_alpha()
bullet_image = pygame.image.load("bullet.png").convert_alpha()

# Scale images if necessary
player_image = pygame.transform.scale(player_image, (50, 50))
enemy_image = pygame.transform.scale(enemy_image, (30, 30))
bullet_image = pygame.transform.scale(bullet_image, (10, 10))

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed_x = 5

    def update(self):
        # Move the player based on key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed_x
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed_x
        if keys[pygame.K_SPACE]:
            self.shoot()

        # Keep the player within the screen bounds
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed_y = -10

    def update(self):
        # Move the bullet upwards
        self.rect.y += self.speed_y
        # Kill the bullet if it goes off-screen
        if self.rect.bottom < 0:
            self.kill()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed_y = random.randrange(1, 8)

    def update(self):
        # Move the enemy downwards
        self.rect.y += self.speed_y
        # If the enemy goes off-screen, reset its position
        if self.rect.top > SCREEN_HEIGHT + 10:
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speed_y = random.randrange(1, 8)

# Create sprite groups
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Create the player and add it to the sprite group
player = Player()
all_sprites.add(player)

# Spawn enemies
for _ in range(8):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Game loop
running = True
while running:
    # Keep the frame rate consistent
    clock.tick(60)

    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update all sprites
    all_sprites.update()

    # Check for collisions between bullets and enemies
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Draw everything on the screen
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Update the display
    pygame.display.flip()

# Clean up
pygame.quit()
