import pygame
import random
import sys
import os # Needed for reliable path handling

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

# Player properties
PLAYER_SPEED = 5
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 30

# Bullet properties
BULLET_SPEED = 10
BULLET_WIDTH = 15
BULLET_HEIGHT = 5

# Enemy properties
ENEMY_SPEED_MIN = 2
ENEMY_SPEED_MAX = 5
ENEMY_WIDTH = 40
ENEMY_HEIGHT = 40
ENEMY_SPAWN_RATE = 60 # Lower number means more frequent spawns (every X frames)

# --- Asset Loading Helper ---
# (Optional but good practice if using images/sounds later)
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- Game Classes ---

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Use a simple colored block for now
        self.image = pygame.Surface([PLAYER_WIDTH, PLAYER_HEIGHT])
        self.image.fill(CYAN)
        self.rect = self.image.get_rect()
        self.rect.centery = SCREEN_HEIGHT // 2
        self.rect.left = 10
        self.speed_x = 0
        self.speed_y = 0
        self.shoot_delay = 250 # milliseconds
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        # Reset speed then check keys
        self.speed_x = 0
        self.speed_y = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -PLAYER_SPEED
        if keystate[pygame.K_RIGHT]:
            self.speed_x = PLAYER_SPEED
        if keystate[pygame.K_UP]:
            self.speed_y = -PLAYER_SPEED
        if keystate[pygame.K_DOWN]:
            self.speed_y = PLAYER_SPEED

        # Move the player
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Keep player on screen
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

        # Shooting
        if keystate[pygame.K_SPACE]:
            self.shoot()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            # Spawn bullet slightly in front of the player's nose
            bullet = Bullet(self.rect.right, self.rect.centery)
            all_sprites.add(bullet)
            bullets.add(bullet)
            # Optional: Add a shooting sound here
            # shoot_sound.play()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([ENEMY_WIDTH, ENEMY_HEIGHT])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.left = SCREEN_WIDTH + random.randrange(50, 200) # Start off-screen right
        self.rect.y = random.randrange(0, SCREEN_HEIGHT - ENEMY_HEIGHT)
        self.speed_x = random.randrange(ENEMY_SPEED_MIN, ENEMY_SPEED_MAX)
        # Optional: Add vertical movement
        self.speed_y = random.randrange(-1, 2) # -1, 0, or 1

    def update(self):
        self.rect.x -= self.speed_x
        self.rect.y += self.speed_y

        # Keep enemy roughly within vertical bounds or reverse direction
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.speed_y *= -1

        # Remove enemy if it goes off the left side
        if self.rect.right < 0:
            self.kill() # Removes sprite from all groups it belongs to

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([BULLET_WIDTH, BULLET_HEIGHT])
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.centery = y
        self.speed_x = BULLET_SPEED

    def update(self):
        self.rect.x += self.speed_x
        # Remove bullet if it goes off the right side
        if self.rect.left > SCREEN_WIDTH:
            self.kill()

# --- Initialization ---
pygame.init()
# Optional: Initialize sound mixer early if using sounds
# pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gradius Clone")
clock = pygame.time.Clock()

# Font for scoring
font_name = pygame.font.match_font('arial') # Find a default system font
def draw_text(surf, text, size, x, y, color=WHITE):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color) # True for anti-aliasing
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

# --- Load Assets ---
# Example - Replace with actual image loading if desired
# player_img = pygame.image.load(resource_path("playerShip.png")).convert_alpha()
# background_img = pygame.image.load(resource_path("background.png")).convert()
# background_rect = background_img.get_rect()

# Create a simple starry background effect
stars = []
for i in range(100):
    star_x = random.randrange(0, SCREEN_WIDTH)
    star_y = random.randrange(0, SCREEN_HEIGHT)
    star_speed = random.randrange(1, 4) # Different speeds for parallax
    star_color = random.choice([WHITE, (200, 200, 200), (150, 150, 150)])
    stars.append([star_x, star_y, star_speed, star_color])

# --- Sprite Groups ---
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
# player_group = pygame.sprite.GroupSingle() # Alternative for single player

player = Player()
all_sprites.add(player)
# player_group.add(player)

# --- Game Variables ---
score = 0
enemy_timer = 0 # Used with ENEMY_SPAWN_RATE

# Optional: Load sounds
# shoot_sound = pygame.mixer.Sound(resource_path("laserShoot.wav"))
# explosion_sound = pygame.mixer.Sound(resource_path("explosion.wav"))
# pygame.mixer.music.load(resource_path("background_music.ogg"))
# pygame.mixer.music.play(loops=-1) # Loop background music


# --- Game Loop ---
running = True
game_over = False
while running:
    # Keep loop running at the right speed
    dt = clock.tick(FPS) / 1000.0 # Delta time in seconds (optional, can use frame counts)

    # --- Process Input (Events) ---
    for event in pygame.event.get():
        # Check for closing window
        if event.type == pygame.QUIT:
            running = False
        # Example: Add restart functionality on game over screen
        if game_over and event.type == pygame.KEYDOWN:
             if event.key == pygame.K_r:
                 # Reset the game (Need a more robust reset function for a full game)
                 game_over = False
                 all_sprites.empty()
                 enemies.empty()
                 bullets.empty()
                 player = Player()
                 all_sprites.add(player)
                 score = 0
                 enemy_timer = 0
             elif event.key == pygame.K_q:
                 running = False


    # --- Update ---
    if not game_over:
        all_sprites.update() # Calls the update() method of all sprites in the group

        # Spawn enemies based on timer/rate
        enemy_timer += 1
        if enemy_timer >= ENEMY_SPAWN_RATE:
            enemy_timer = 0
            new_enemy = Enemy()
            all_sprites.add(new_enemy)
            enemies.add(new_enemy)

        # Check for collisions: bullets hitting enemies
        # groupcollide checks collisions between two groups.
        # The two booleans determine if the sprites in the first and second group should be killed on collision.
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            score += 10 # Increase score for each enemy hit
            # Optional: Add explosion effect or sound here
            # explosion_sound.play()

        # Check for collisions: player hitting enemies
        # spritecollide checks collisions between a single sprite and a group.
        # The boolean determines if the sprites in the group should be killed on collision.
        hits = pygame.sprite.spritecollide(player, enemies, True) # Kill enemy on collision
        if hits:
            # Player hit an enemy!
            # Optional: Player explosion effect/sound
            # player.kill() # Remove player if implementing lives
            game_over = True # End the game for this simple version

    # --- Draw / Render ---
    # Background first
    screen.fill(BLACK)

    # Draw scrolling stars
    for star in stars:
        star[0] -= star[2] # Move star left based on its speed
        if star[0] < 0: # If star goes off screen left...
            star[0] = SCREEN_WIDTH # ...reset to the right side
            star[1] = random.randrange(0, SCREEN_HEIGHT) # New vertical position
        pygame.draw.circle(screen, star[3], (star[0], star[1]), 1) # Draw the star

    # If using a background image:
    # screen.blit(background_img, background_rect) # Add scrolling logic here

    # Draw all sprites
    all_sprites.draw(screen)

    # Draw the score
    draw_text(screen, f"Score: {score}", 24, SCREEN_WIDTH // 2, 10)

    # If Game Over, show message
    if game_over:
        draw_text(screen, "GAME OVER", 64, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4, RED)
        draw_text(screen, "Press 'R' to Restart or 'Q' to Quit", 22, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    # *After* drawing everything, flip the display
    pygame.display.flip()

# --- Quit Pygame ---
pygame.quit()
sys.exit()
