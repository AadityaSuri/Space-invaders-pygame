import pygame
import time
import random
import os

#screen
width = 750
height = 750
screen = pygame.display.set_mode((width, height))

#sprites load
playerShip = pygame.image.load("Game Assets/PlayerShip.png")
playerShip = pygame.transform.scale(playerShip, (180, 120))
enemyShip = pygame.image.load("Game Assets/EnemyShip.png")
enemyShip = pygame.transform.scale(enemyShip, (150, 100))
playerBullet = pygame.image.load("Game Assets/PlayerBullet.png")
playerBullet = pygame.transform.scale(playerBullet, (20,20))
enemyBullet = pygame.image.load("Game Assets/EnemyBullet.png")
bg = pygame.image.load("Game Assets/Background.jpg")
bg = pygame.transform.scale(bg, (width, height))

#player coordinates
playerX = (width/2)-90
playerY = 600
playerX_change = 0
playerY_change = 0

#enemy coordinates
enemyX = random.randint(-20, width-130)
enemyY = random.randint(0, 100)
enemyX_change = 2.3
enemyY_change = 0.3

#player bullet coordinates
pBulletX = 0
pBulletY = 600
pBulletY_change = 6
pBulletState = "ready"

def player(x, y):
    screen.blit(playerShip, (x, y))

def enemy(x, y):
    screen.blit(enemyShip, (x, y))

def firePBullet(x, y):
    global pBulletState
    pBulletState = "fire"
    screen.blit(playerBullet,(x + 80, y + 25))

#event loop

running = True
while running:
    screen.blit(bg, (0, 0))

    #player control mechanics
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -2
            if event.key == pygame.K_RIGHT:
                playerX_change = 2
            if event.key == pygame.K_SPACE:
                if pBulletState == "ready":
                    pBulletX = playerX
                    firePBullet(playerX, pBulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    #boundary check for player and player movement
    if playerX <= -50:
        playerX = -50
    if playerX >= width-130:
        playerX = width-130
    playerX += playerX_change

    #enemy movement
    enemyX += enemyX_change
    enemyY += enemyY_change
    if enemyX <= -20:
        enemyX_change = 2.2
    if enemyX >= width - 130:
        enemyX_change = -2.3

    #bullet movement
    if pBulletY <= -30:
        pBulletY = 600
        pBulletState = "ready"
    if pBulletState == "fire":
        firePBullet(pBulletX, pBulletY)
        pBulletY -= pBulletY_change

    player(playerX, playerY)
    enemy(enemyX, enemyY)
    pygame.display.update()
