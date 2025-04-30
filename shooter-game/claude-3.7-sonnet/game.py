import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Set title and icon
pygame.display.set_caption("Space Shooter")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Background
background = pygame.image.load('background.png')
background_scroll = 0
background_width = background.get_width()

# Player
player_img = pygame.image.load('player.png')
player_x = 100
player_y = 300
player_y_change = 0
player_speed = 5
player_lives = 3

# Bullets
bullet_img = pygame.image.load('bullet.png')
bullets = []
bullet_speed = 10
bullet_state = "ready"  # ready - can't see bullet, fire - bullet is moving
bullet_cooldown = 0
bullet_cooldown_max = 10

# Enemies
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load('enemy.png'))
    enemy_x.append(random.randint(800, 1600))
    enemy_y.append(random.randint(50, 550))
    enemy_x_change.append(-4)
    enemy_y_change.append(0)

# Power-ups
power_up_img = pygame.image.load('powerup.png')
power_up_x = -100  # Off-screen initially
power_up_y = -100
power_up_active = False
power_up_type = None
power_up_timer = 0
power_up_speed = 3
power_up_spawn_timer = 0
power_up_spawn_cooldown = 600  # 10 seconds at 60 FPS

# Score
score_value = 0
font = pygame.font.SysFont(None, 24)  # デフォルトのシステムフォントを使用
score_x = 10
score_y = 10

# Game Over text
game_over_font = pygame.font.SysFont(None, 64)  # デフォルトのシステムフォントを使用

# Functions
def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    lives = font.render("Lives: " + str(player_lives), True, (255, 255, 255))
    screen.blit(score, (x, y))
    screen.blit(lives, (x, y + 30))

def player(x, y):
    screen.blit(player_img, (x, y))

def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    bullets.append([x + 50, y + 16])  # Position the bullet at the player's position

def draw_bullets():
    for bullet in bullets:
        screen.blit(bullet_img, (bullet[0], bullet[1]))

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((enemy_x - bullet_x) ** 2 + (enemy_y - bullet_y) ** 2)
    if distance < 35:  # Adjust collision threshold as needed
        return True
    return False

def spawn_power_up():
    global power_up_x, power_up_y, power_up_active, power_up_type
    power_up_types = ["double_shot", "speed_up", "shield"]
    power_up_type = random.choice(power_up_types)
    power_up_x = screen_width
    power_up_y = random.randint(50, 550)
    power_up_active = True

def draw_power_up():
    if power_up_active:
        screen.blit(power_up_img, (power_up_x, power_up_y))

def game_over_text():
    over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    restart_text = font.render("Press R to restart", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
    screen.blit(restart_text, (300, 350))

def reset_game():
    global player_x, player_y, player_lives, score_value, power_up_active, power_up_type, power_up_timer, bullets

    player_x = 100
    player_y = 300
    player_lives = 3
    score_value = 0
    power_up_active = False
    power_up_type = None
    power_up_timer = 0
    bullets = []

    for i in range(num_of_enemies):
        enemy_x[i] = random.randint(800, 1600)
        enemy_y[i] = random.randint(50, 550)

# Game loop
running = True
game_over = False
clock = pygame.time.Clock()

while running:
    # RGB background
    screen.fill((0, 0, 0))

    # Draw scrolling background
    rel_x = background_scroll % background_width
    screen.blit(background, (rel_x - background_width, 0))
    if rel_x < screen_width:
        screen.blit(background, (rel_x, 0))
    background_scroll += 2  # Scroll speed

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keystroke events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_y_change = -player_speed
            if event.key == pygame.K_DOWN:
                player_y_change = player_speed
            if event.key == pygame.K_SPACE and bullet_cooldown <= 0:
                fire_bullet(player_x, player_y)
                bullet_cooldown = bullet_cooldown_max
            if event.key == pygame.K_r and game_over:
                reset_game()
                game_over = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player_y_change = 0

    if not game_over:
        # Player movement
        player_y += player_y_change

        # Player boundaries
        if player_y <= 0:
            player_y = 0
        elif player_y >= 536:
            player_y = 536

        # Bullet movement
        for bullet in bullets[:]:
            bullet[0] += bullet_speed
            if bullet[0] >= 800:
                bullets.remove(bullet)

        # Bullet cooldown
        if bullet_cooldown > 0:
            bullet_cooldown -= 1

        # Enemy movement
        for i in range(num_of_enemies):
            # Enemy movement
            enemy_x[i] += enemy_x_change[i]

            # If enemy reaches the left edge, respawn it
            if enemy_x[i] <= -64:
                enemy_x[i] = random.randint(800, 1600)
                enemy_y[i] = random.randint(50, 550)

            # Collision detection with bullets
            for bullet in bullets[:]:
                collision = is_collision(enemy_x[i], enemy_y[i], bullet[0], bullet[1])
                if collision:
                    bullets.remove(bullet)
                    score_value += 1
                    enemy_x[i] = random.randint(800, 1600)
                    enemy_y[i] = random.randint(50, 550)

            # Collision detection with player
            player_collision = is_collision(enemy_x[i], enemy_y[i], player_x, player_y)
            if player_collision:
                player_lives -= 1
                enemy_x[i] = random.randint(800, 1600)
                enemy_y[i] = random.randint(50, 550)

                if player_lives <= 0:
                    game_over = True

            # Draw enemy
            enemy(enemy_x[i], enemy_y[i], i)

        # Power-up handling
        power_up_spawn_timer += 1
        if power_up_spawn_timer >= power_up_spawn_cooldown and not power_up_active:
            spawn_power_up()
            power_up_spawn_timer = 0

        if power_up_active:
            power_up_x -= power_up_speed

            # Check if player collects power-up
            power_up_collision = math.sqrt((power_up_x - player_x) ** 2 + (power_up_y - player_y) ** 2) < 35
            if power_up_collision:
                power_up_active = False
                power_up_timer = 600  # 10 seconds of power-up

                if power_up_type == "double_shot":
                    bullet_cooldown_max = 5
                elif power_up_type == "speed_up":
                    player_speed = 8
                elif power_up_type == "shield":
                    # Implement shield logic
                    pass

            # If power-up goes off-screen
            if power_up_x < -32:
                power_up_active = False

            draw_power_up()

        # If power-up is active, count down timer
        if power_up_timer > 0:
            power_up_timer -= 1

            # When power-up expires
            if power_up_timer <= 0:
                bullet_cooldown_max = 10
                player_speed = 5

        # Draw player and bullets
        player(player_x, player_y)
        draw_bullets()

    else:
        game_over_text()

    # Show score
    show_score(score_x, score_y)

    # Update display
    pygame.display.update()
    clock.tick(60)

pygame.quit()
