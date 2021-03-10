import math
import random
import time

import pygame
from pygame import mixer

# Initalize the pygame
pygame.init()

# Created the screen
screen = pygame.display.set_mode((800, 600))

# Background Image
background = pygame.image.load('background.png')

# backgroun Music
mixer.music.load('background.wav')
mixer.music.play(-1)
# if we pass -1 then it will go to infinite loop.


# Title
pygame.display.set_caption("Space Invaders")
# Icon
icon = pygame.image.load('rocket.png')
pygame.display.set_icon(icon)

# scoreboard
score = 0
font = pygame.font.Font('freesansbold.ttf', 16)
fontX = 10
fontY = 10

# gamoveover text
over = pygame.font.Font('freesansbold.ttf', 72)


def showScore(x, y):
    # first we have to render the score and then we blit the score on screen
    s = font.render("Score : " + str(score), True, (255, 255, 255))
    screen.blit(s, (x, y))


def Game_over():
    # first we have to render the score and then we blit the score on screen
    s = over.render("GAME OVER", True, (255, 255, 255))
    screen.blit(s, (200, 250))
    time.sleep(2)


# Player
playerimg = pygame.image.load('space-invaders.png')
# X-axis and Y-axis
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = pygame.image.load('alien.png')
enemyX = random.randint(0, 736)
enemyY = random.randint(50, 150)
enemyX_Change = 4
enemyY_Change = 40

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_Change = 0
bulletY_Change = 10
bullet_state = "ready"


def player(x, y):
    # bilt means draw it take 3args first image, (cords)
    screen.blit(playerimg, (x, y))


def enemy(x, y):
    # bilt means draw it take 3args first image, (cords)
    screen.blit(enemyImg, (x, y))


def fire_bullet(x, y):
    # global bullet_state
    # bullet_state = "fire"
    # bilt means draw it take 3args first image, (cords)
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:
    # RGB Disaplay Color
    screen.fill((0, 0, 0))
    # background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if Keystroke is pressed check wheather it is right or left
        if event.type == pygame.KEYDOWN:  # KEYDOWN means Button Pressed
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = +5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletmusic = mixer.Sound("laser.wav")
                    bulletmusic.play()
                    bulletX = playerX
                    bullet_state = "fire"
                    # fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:  # KEYUP means Button Realsed
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Logical Part Of the Game

    playerX += playerX_change

    # Adding Boundaries for Player
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    enemyX += enemyX_Change

    # Adding Boundaries for Enemies
    if enemyX <= 0:
        enemyX_Change = 4
        enemyY += enemyY_Change
    elif enemyX >= 736:
        enemyX_Change = -4
        enemyY += enemyY_Change

    # Gamover logic
    if enemyY > 300:
        enemyY = 2000
        Game_over()
        break

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_Change

    # Collision it will get a bool value.
    collision = isCollision(enemyX, enemyY, bulletX, bulletY)

    # after the collision again gernating the enemy and fixing the bullet at his former place.
    if collision:
        bulletY = 480
        bullet_state = "ready"
        enemysound = mixer.Sound("explosion.wav")
        enemysound.play()
        score += 1
        enemyX = random.randint(0, 736)
        enemyY = random.randint(50, 150)

    player(playerX, playerY)
    enemy(enemyX, enemyY)
    showScore(fontX, fontY)
    pygame.display.update()  # this is must to upadte the changes.
