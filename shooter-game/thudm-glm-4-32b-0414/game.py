import pygame
import random
import math
from pygame import mixer

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Player settings
class Player:
    def __init__(self):
        self.width = 50
        self.height = 40
        self.x = 100
        self.y = HEIGHT // 2
        self.speed = 5
        self.bullets = []
        self.bullet_speed = 10
        self.bullet_cooldown = 10
        self.bullet_timer = 0
        self.lives = 3
        self.power_level = 1
        self.shield = False
        self.shield_radius = 30

    def draw(self):
        # Draw the ship
        pygame.draw.polygon(screen, GREEN, [
            (self.x + self.width, self.y + self.height // 2),
            (self.x, self.y),
            (self.x, self.y + self.height)
        ])

        # Draw shield if active
        if self.shield:
            pygame.draw.circle(screen, BLUE, (self.x + self.width // 2, self.y + self.height // 2),
                              self.shield_radius, 2)

    def move(self, direction):
        if direction == "up" and self.y > 0:
            self.y -= self.speed
        if direction == "down" and self.y < HEIGHT - self.height:
            self.y += self.speed
        if direction == "left" and self.x > 0:
            self.x -= self.speed
        if direction == "right" and self.x < WIDTH - self.width:
            self.x += self.speed

    def shoot(self):
        if self.bullet_timer <= 0:
            if self.power_level == 1:
                self.bullets.append([self.x + self.width, self.y + self.height // 2])
            elif self.power_level >= 2:
                self.bullets.append([self.x + self.width, self.y + self.height // 3])
                self.bullets.append([self.x + self.width, self.y + 2 * self.height // 3])

            self.bullet_timer = self.bullet_cooldown

    def update_bullets(self):
        if self.bullet_timer > 0:
            self.bullet_timer -= 1

        # Move bullets
        for bullet in self.bullets[:]:
            bullet[0] += self.bullet_speed
            if bullet[0] > WIDTH:
                self.bullets.remove(bullet)

    def draw_bullets(self):
        for bullet in self.bullets:
            pygame.draw.circle(screen, YELLOW, (bullet[0], bullet[1]), 3)

# Enemy class
class Enemy:
    def __init__(self, x, y, enemy_type):
        self.x = x
        self.y = y
        self.type = enemy_type
        self.health = enemy_type + 1
        self.width = 40
        self.height = 30
        self.speed = random.uniform(2, 4)

    def draw(self):
        if self.type == 0:  # Small enemy
            pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))
        else:  # Larger enemy
            pygame.draw.rect(screen, RED, (self.x, self.y, self.width + 10, self.height + 10))
            pygame.draw.rect(screen, YELLOW, (self.x + 5, self.y + 5, self.width - 10, self.height - 10))

    def move(self):
        self.x -= self.speed

    def is_off_screen(self):
        return self.x < -100

# Powerup class
class Powerup:
    def __init__(self, x, y, power_type):
        self.x = x
        self.y = y
        self.type = power_type  # 0 for weapon upgrade, 1 for shield, 2 for life
        self.width = 20
        self.height = 20
        self.speed = 3

    def draw(self):
        if self.type == 0:  # Weapon upgrade
            pygame.draw.rect(screen, YELLOW, (self.x, self.y, self.width, self.height))
        elif self.type == 1:  # Shield
            pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))
        else:  # Life
            pygame.draw.rect(screen, GREEN, (self.x, self.y, self.width, self.height))

    def move(self):
        self.x -= self.speed

    def is_off_screen(self):
        return self.x < -50

# Explosion effect
class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 5
        self.max_radius = 20
        self.growth_rate = 2

    def update(self):
        self.radius += self.growth_rate
        return self.radius > self.max_radius

    def draw(self):
        pygame.draw.circle(screen, RED, (self.x, self.y), self.radius)
        pygame.draw.circle(screen, YELLOW, (self.x, self.y), self.radius - 5)

# Game variables
player = Player()
enemies = []
powerups = []
explosions = []
score = 0
enemy_spawn_rate = 60  # Frames between enemy spawns
enemy_timer = 0
game_over = False
level = 1

# Background stars
stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(100)]
star_speeds = [random.uniform(1, 3) for _ in range(100)]

# Main game loop
clock = pygame.time.Clock()
running = True

def reset_game():
    global player, enemies, powerups, explosions, score, enemy_timer, game_over, level
    player = Player()
    enemies = []
    powerups = []
    explosions = []
    score = 0
    enemy_timer = 0
    game_over = False
    level = 1

def draw_text(text, size, x, y):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, (x, y))

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()

    if not game_over:
        # Get keyboard input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player.move("up")
        if keys[pygame.K_DOWN]:
            player.move("down")
        if keys[pygame.K_LEFT]:
            player.move("left")
        if keys[pygame.K_RIGHT]:
            player.move("right")
        if keys[pygame.K_SPACE]:
            player.shoot()

        # Update game objects
        player.update_bullets()

        # Spawn enemies
        enemy_timer += 1
        if enemy_timer >= enemy_spawn_rate:
            enemy_type = random.randint(0, min(level - 1, 2))
            y_pos = random.randint(20, HEIGHT - 50)
            enemies.append(Enemy(WIDTH + 50, y_pos, enemy_type))
            enemy_timer = 0
            if level > 3 and random.random() < 0.2:
                enemy_spawn_rate = max(30, enemy_spawn_rate - 1)  # Speed up spawning

        # Move enemies and check collisions
        for enemy in enemies[:]:
            enemy.move()

            # Check if enemy is off screen
            if enemy.is_off_screen():
                enemies.remove(enemy)
                continue

            # Check collision with player bullets
            for bullet in player.bullets[:]:
                if (enemy.x < bullet[0] < enemy.x + enemy.width and
                    enemy.y < bullet[1] < enemy.y + enemy.height):

                    enemy.health -= 1
                    if enemy.health <= 0:
                        explosions.append(Explosion(enemy.x + enemy.width//2, enemy.y + enemy.height//2))

                        # Chance to drop powerup
                        if random.random() < 0.2:  # 20% chance
                            power_type = random.randint(0, 2)
                            powerups.append(Powerup(enemy.x, enemy.y, power_type))

                        enemies.remove(enemy)
                        score += (enemy.type + 1) * 10
                        break

                    if bullet in player.bullets:
                        player.bullets.remove(bullet)

            # Check collision with player
            if (player.x < enemy.x + enemy.width and
                player.x + player.width > enemy.x and
                player.y < enemy.y + enemy.height and
                player.y + player.height > enemy.y):

                if player.shield:
                    explosions.append(Explosion(enemy.x + enemy.width//2, enemy.y + enemy.height//2))
                    enemies.remove(enemy)
                    score += (enemy.type + 1) * 10
                    player.shield = False
                else:
                    explosions.append(Explosion(player.x + player.width//2, player.y + player.height//2))
                    if enemy in enemies:  # Make sure enemy still exists
                        enemies.remove(enemy)
                    player.lives -= 1
                    if player.lives <= 0:
                        game_over = True

        # Move powerups and check collisions
        for powerup in powerups[:]:
            powerup.move()

            if powerup.is_off_screen():
                powerups.remove(powerup)
                continue

            # Check collision with player
            if (player.x < powerup.x + powerup.width and
                player.x + player.width > powerup.x and
                player.y < powerup.y + powerup.height and
                player.y + player.height > powerup.y):

                if powerup.type == 0:  # Weapon upgrade
                    player.power_level = min(player.power_level + 1, 3)
                elif powerup.type == 1:  # Shield
                    player.shield = True
                else:  # Life
                    player.lives += 1

                powerups.remove(powerup)

        # Update explosions
        for explosion in explosions[:]:
            if explosion.update():
                explosions.remove(explosion)

        # Level progression
        if score >= level * 500:
            level += 1

        # Move stars (background effect)
        for i in range(len(stars)):
            stars[i] = ((stars[i][0] - star_speeds[i]) % WIDTH, stars[i][1])

    # Drawing
    screen.fill(BLACK)

    # Draw stars
    for i, star in enumerate(stars):
        brightness = random.randint(150, 255)
        pygame.draw.circle(screen, (brightness, brightness, brightness),
                          (int(star[0]), int(star[1])), 1)

    if not game_over:
        player.draw()
        player.draw_bullets()

        for enemy in enemies:
            enemy.draw()

        for powerup in powerups:
            powerup.draw()

        for explosion in explosions:
            explosion.draw()

        # Draw HUD
        draw_text(f"Score: {score}", 30, 10, 10)
        draw_text(f"Lives: {player.lives}", 30, 10, 40)
        draw_text(f"Power Level: {player.power_level}", 30, 10, 70)
        draw_text(f"Level: {level}", 30, 10, 100)
    else:
        draw_text("GAME OVER", 60, WIDTH//2 - 150, HEIGHT//2 - 50)
        draw_text(f"Final Score: {score}", 40, WIDTH//2 - 120, HEIGHT//2 + 20)
        draw_text("Press R to Restart", 30, WIDTH//2 - 100, HEIGHT//2 + 70)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
