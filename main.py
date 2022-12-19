import math
import random

import pygame

# Initialise the pygame
pygame.init()

# create screen
screen = pygame.display.set_mode((900, 750))

# background
background = pygame.image.load("space.png")

# Caption and icon
pygame.display.set_caption("THE INVADERS")
icon = pygame.image.load("alienn.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("arcade.png")
playerX = 420
playerY = 670
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 10

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("alienn.png"))
    enemyX.append(random.randint(0, 836))
    enemyY.append(random.randint(0, 50))
    enemyX_change.append(3)
    enemyY_change.append(40)

# Bullets
# Ready - can't see the bullets on the screen
# Fire - the bullets are currently moving
bulletImg = pygame.image.load("bullets.png")
bulletX = 0
bulletY = 670
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Font
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 20)

textX = 5
textY = 5

# Game Over Text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x,y):
    score = font.render("Score : " +str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (250, 330))

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 20))

def isCollision(enemyX,enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False

# game loop
running = True
while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
               playerX_change = -5
            if event.key == pygame.K_RIGHT:
               playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            playerX_change = 0

    # Checking for boundries of spaceship

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 836:
        playerX = 836

    # movement 0f enemy
    for i in range(num_of_enemies):

        # Game over
        if enemyY[i] > 620:
            for j in range(num_of_enemies):
                enemyY[j] = 3000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 836:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 670
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 836)
            enemyY[i] = random.randint(0, 50)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 670
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change


    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()