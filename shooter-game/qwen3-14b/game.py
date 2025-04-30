import pygame
import random

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gradius Clone")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Load assets (placeholder shapes used for simplicity)
PLAYER_COLOR = (0, 255, 0)     # Green
ENEMY_COLOR = (255, 0, 0)      # Red
BULLET_COLOR = (255, 255, 255)  # White

# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))
        self.speed = 5
        self.shoot_cooldown = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        # Keep player within screen bounds
        self.rect.clamp_ip(screen.get_rect())

        # Shooting logic
        if keys[pygame.K_SPACE] and self.shoot_cooldown <= 0:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            self.shoot_cooldown = 30

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(ENEMY_COLOR)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed_y = 2
        self.direction_x = random.choice([-1, 1])

    def update(self):
        # Move downward and side-to-side
        self.rect.y += self.speed_y
        self.rect.x += self.direction_x

        # Reverse direction if hitting screen edges
        if self.rect.right > SCREEN_WIDTH or self.rect.left < 0:
            self.direction_x *= -1

        # Remove enemy if it goes off-bottom of the screen
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(BULLET_COLOR)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -7  # Move upward

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()


# Sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

# Initialize score and game timer
score = 0
enemy_spawn_timer = 0

# Main Game Loop
running = True
while running:
    clock.tick(60)  # Cap frame rate to 60 FPS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update all sprites
    all_sprites.update()

    # Spawn enemies every second (60 frames)
    enemy_spawn_timer += 1
    if enemy_spawn_timer > 60:
        x = random.randint(0, SCREEN_WIDTH - 30)
        y = 0
        enemy = Enemy(x, y)
        all_sprites.add(enemy)
        enemies.add(enemy)
        enemy_spawn_timer = 0

    # Collision detection between bullets and enemies
    collisions = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for _ in collisions:
        score += 10

    # Game Over condition: player collides with any enemy
    if pygame.sprite.spritecollideany(player, enemies):
        print("Game Over!")
        running = False

    # Drawing everything
    screen.fill((0, 0, 0))  # Clear the screen (black background)
    all_sprites.draw(screen)

    # Display score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()
