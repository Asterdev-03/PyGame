import pygame
import random

# Initialize Pygame
pygame.init()

# Define constants
ROWS = 15
COLUMN = 30
GRID_SIZE = 40
BULLET_SIZE = 40
BULLET_RANGE = 12
NO_OF_ENEMIES = 15
PLAYER_HEALTH = 300

# Define sprites
PLAYER_SPRITE = pygame.image.load("player.png")
ENEMY_SPRITE = pygame.image.load("enemy.png")
BULLET_SPRITE = pygame.image.load("bullet.png")
GRASS_SPRITE = pygame.image.load("grass.jpg")

# Set up the screen
screen_width = GRID_SIZE*COLUMN
screen_height = GRID_SIZE*ROWS
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tank Game")

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 127)
dark_green = (60, 179, 113)
red = (199, 21, 133)
blue = (0, 0, 255)
yellow = (255, 250, 205)

# Set up the clock
clock = pygame.time.Clock()

# Initaialize score
score = 0

font = pygame.font.SysFont(None, 48)

# Render welcome message
font = pygame.font.SysFont(None, 48)
text = font.render("Welcome to tank battle survival.", True, (255, 255, 255))
text_rect = text.get_rect(center=(screen_width/2, screen_height/2))
screen.blit(text, text_rect)

pygame.display.update()
pygame.time.delay(2000)

screen.fill((0, 0, 0))

# Define Tank


class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite):
        super().__init__()
        self.image = pygame.Surface([GRID_SIZE, GRID_SIZE])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.sprite = pygame.transform.scale(
            sprite, (GRID_SIZE, GRID_SIZE))
        self.rotate = 0

    def draw(self):
        screen.blit(self.sprite, (self.rect.x, self.rect.y))

    def move(self, direction):
        if direction == "up":
            self.rect.y -= GRID_SIZE
            if self.rotate == 90:
                self.sprite = pygame.transform.rotate(self.sprite, -90)
            elif self.rotate == -90:
                self.sprite = pygame.transform.rotate(self.sprite, 90)
            elif self.rotate == 180:
                self.sprite = pygame.transform.rotate(self.sprite, 180)
            self.rotate = 0
        elif direction == "down":
            self.rect.y += GRID_SIZE
            if self.rotate == 90:
                self.sprite = pygame.transform.rotate(self.sprite, 90)
            elif self.rotate == -90:
                self.sprite = pygame.transform.rotate(self.sprite, -90)
            elif self.rotate == 0:
                self.sprite = pygame.transform.rotate(self.sprite, 180)
            self.rotate = 180
        elif direction == "left":
            self.rect.x -= GRID_SIZE
            if self.rotate == 0:
                self.sprite = pygame.transform.rotate(self.sprite, 90)
            elif self.rotate == -90:
                self.sprite = pygame.transform.rotate(self.sprite, 180)
            elif self.rotate == 180:
                self.sprite = pygame.transform.rotate(self.sprite, -90)
            self.rotate = 90
        elif direction == "right":
            self.rect.x += GRID_SIZE
            if self.rotate == 90:
                self.sprite = pygame.transform.rotate(self.sprite, 180)
            elif self.rotate == 0:
                self.sprite = pygame.transform.rotate(self.sprite, -90)
            elif self.rotate == 180:
                self.sprite = pygame.transform.rotate(self.sprite, 90)
            self.rotate = -90

        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > (screen_width - self.image.get_width()):
            self.rect.x = screen_width - self.image.get_width()
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > (screen_height - self.image.get_height()):
            self.rect.y = screen_height - self.image.get_height()

# Define Bullet


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite, direction, speed):
        super().__init__()
        self.image = pygame.Surface([BULLET_SIZE, BULLET_SIZE])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction
        self.speed = speed
        self.sprite = pygame.transform.scale(
            sprite, (BULLET_SIZE, BULLET_SIZE))
        self.rotate = 0

    def draw(self):
        screen.blit(self.sprite, (self.rect.x, self.rect.y))

    def update(self):
        if self.direction == "up":
            self.rect.y -= self.speed
            if self.rotate == 90:
                self.sprite = pygame.transform.rotate(self.sprite, -90)
            elif self.rotate == -90:
                self.sprite = pygame.transform.rotate(self.sprite, 90)
            elif self.rotate == 180:
                self.sprite = pygame.transform.rotate(self.sprite, 180)
            self.rotate = 0
        elif self.direction == "down":
            self.rect.y += self.speed
            if self.rotate == 90:
                self.sprite = pygame.transform.rotate(self.sprite, 90)
            elif self.rotate == -90:
                self.sprite = pygame.transform.rotate(self.sprite, -90)
            elif self.rotate == 0:
                self.sprite = pygame.transform.rotate(self.sprite, 180)
            self.rotate = 180
        elif self.direction == "left":
            self.rect.x -= self.speed
            if self.rotate == 0:
                self.sprite = pygame.transform.rotate(self.sprite, 90)
            elif self.rotate == -90:
                self.sprite = pygame.transform.rotate(self.sprite, 180)
            elif self.rotate == 180:
                self.sprite = pygame.transform.rotate(self.sprite, -90)
            self.rotate = 90
        elif self.direction == "right":
            self.rect.x += self.speed
            if self.rotate == 90:
                self.sprite = pygame.transform.rotate(self.sprite, 180)
            elif self.rotate == 0:
                self.sprite = pygame.transform.rotate(self.sprite, -90)
            elif self.rotate == 180:
                self.sprite = pygame.transform.rotate(self.sprite, 90)
            self.rotate = -90


# Create player tank
player_tank = Tank(GRID_SIZE * (COLUMN//2), GRID_SIZE*(ROWS//2), PLAYER_SPRITE)

# Create enemy tanks
enemy_tank_group = pygame.sprite.Group()
for i in range(NO_OF_ENEMIES):
    enemy_tank = Tank(GRID_SIZE * random.randint(0, COLUMN),
                      GRID_SIZE * random.randint(0, ROWS), ENEMY_SPRITE)
    enemy_tank_group.add(enemy_tank)

# create the bullet groups
player_bullet_group = pygame.sprite.Group()
enemy_bullet_group = pygame.sprite.Group()

# Initialize variables
player_score = 0
game_running = True
enemy_direction = ""
shooting_direction = ""
player_direction = ""

while game_running:
    clock.tick(60)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_direction = "left"
                player_tank.move(player_direction)
            elif event.key == pygame.K_RIGHT:
                player_direction = "right"
                player_tank.move(player_direction)
            elif event.key == pygame.K_UP:
                player_direction = "up"
                player_tank.move(player_direction)
            elif event.key == pygame.K_DOWN:
                player_direction = "down"
                player_tank.move(player_direction)
            elif event.key == pygame.K_SPACE:
                bullet = Bullet(player_tank.rect.x,
                                player_tank.rect.y, BULLET_SPRITE, player_direction, 7)
                player_bullet_group.add(bullet)

    # update player bullets
    player_bullet_group.update()

    # update enemy bullets
    enemy_bullet_group.update()

    # Spawn new enemies
    x_enemy = GRID_SIZE * random.randint(0, COLUMN)
    y_enemy = GRID_SIZE * random.randint(0, ROWS)
    if random.randint(1, 70) == 1 and x_enemy != player_tank.rect.x and y_enemy != player_tank.rect.y:
        enemy_tank = Tank(x_enemy, y_enemy, ENEMY_SPRITE)
        enemy_tank_group.add(enemy_tank)

    # Move enemy tanks
    for enemy_tank in enemy_tank_group:
        if random.randint(1, 50) == 1:
            if (enemy_tank.rect.x < player_tank.rect.x) and (enemy_tank.rect.y > player_tank.rect.y):
                enemy_direction = random.choice(["right", "up"])
            elif (enemy_tank.rect.x < player_tank.rect.x) and (enemy_tank.rect.y < player_tank.rect.y):
                enemy_direction = random.choice(["right", "down"])
            elif (enemy_tank.rect.x > player_tank.rect.x) and (enemy_tank.rect.y > player_tank.rect.y):
                enemy_direction = random.choice(["left", "up"])
            elif (enemy_tank.rect.x > player_tank.rect.x) and (enemy_tank.rect.y < player_tank.rect.y):
                enemy_direction = random.choice(["left", "down"])

        enemy_tank.move(enemy_direction)

        # check if the enemy tank is facing the player tank
        if ((enemy_tank.rect.y - player_tank.rect.y) <= GRID_SIZE*BULLET_RANGE and (enemy_tank.rect.y - player_tank.rect.y) >= 0) and ((enemy_tank.rect.x - player_tank.rect.x) == 0):
            shooting_direction = "up"
        elif ((enemy_tank.rect.y - player_tank.rect.y) >= -GRID_SIZE*BULLET_RANGE and (enemy_tank.rect.y - player_tank.rect.y) <= 0) and ((enemy_tank.rect.x - player_tank.rect.x) == 0):
            shooting_direction = "down"
        elif ((enemy_tank.rect.x - player_tank.rect.x) <= GRID_SIZE*BULLET_RANGE and (enemy_tank.rect.x - player_tank.rect.x) >= 0) and ((enemy_tank.rect.y - player_tank.rect.y) == 0):
            shooting_direction = "left"
        elif ((enemy_tank.rect.x - player_tank.rect.x) >= -GRID_SIZE*BULLET_RANGE and (enemy_tank.rect.x - player_tank.rect.x) <= 0) and ((enemy_tank.rect.y - player_tank.rect.y) == 0):
            shooting_direction = "right"

        # create a bullet object in the direction of the player tank
        if random.randint(1, 40) == 1 and shooting_direction in ["up", "down", "left", "right"]:
            bullet = Bullet(enemy_tank.rect.x,
                            enemy_tank.rect.y, BULLET_SPRITE, shooting_direction, 3)
            enemy_bullet_group.add(bullet)

        enemy_direction = ""
        shooting_direction = ""

    # check for collisions between player bullets and enemy tanks
    for bullet in player_bullet_group:
        enemy_tank_hit_list = pygame.sprite.spritecollide(
            bullet, enemy_tank_group, True)
        for enemy_tank in enemy_tank_hit_list:
            player_bullet_group.remove(bullet)
            score += 100

    # check for collisions between enemy bullets and player tank
    for bullet in enemy_bullet_group:
        if pygame.sprite.collide_rect(bullet, player_tank):
            enemy_bullet_group.remove(bullet)
            PLAYER_HEALTH -= 30

    # check for collisions between player and enemy tanks
    enemy_tank_hit_list = pygame.sprite.spritecollide(
        player_tank, enemy_tank_group, True)
    if len(enemy_tank_hit_list) != 0:
        PLAYER_HEALTH -= 60

    # Regenerate some health
    if PLAYER_HEALTH <= 300:
        PLAYER_HEALTH += 0.05

    # draw the grids
    for i in range(ROWS):
        for j in range(COLUMN):
            rect = pygame.Rect(j*GRID_SIZE, i*GRID_SIZE, GRID_SIZE, GRID_SIZE)
            screen.blit(pygame.transform.scale(
                GRASS_SPRITE, (GRID_SIZE, GRID_SIZE)), rect)
            pygame.draw.rect(screen, dark_green, rect, 1)

    # draw the player tank
    player_tank.draw()

    # draw the enemy tanks
    for enemy_tank in enemy_tank_group:
        enemy_tank.draw()

    # draw the player bullets
    for bullet in player_bullet_group:
        bullet.draw()

    # draw the enemy bullets
    for bullet in enemy_bullet_group:
        bullet.draw()

    # draw the player health bar
    pygame.draw.rect(screen, (255, 0, 0), (screen_width -
                                           PLAYER_HEALTH, 0, PLAYER_HEALTH, GRID_SIZE))

    # check if the player is dead
    if PLAYER_HEALTH <= 0:
        game_running = False
        print("Game Over - You Lose!")

    # Update display
    pygame.display.update()

text = font.render("Highscore: " + str(score), True, (255, 255, 255))
text_rect = text.get_rect(center=(screen_width/2, screen_height/2 - GRID_SIZE))
screen.blit(text, text_rect)

text = font.render("Game Over!", True, (255, 255, 255))
text_rect = text.get_rect(center=(screen_width/2, screen_height/2))
screen.blit(text, text_rect)


pygame.display.update()
pygame.time.delay(2000)
pygame.quit()
