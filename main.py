import pygame
import random
import math

from pygame import mixer

pygame.init()

#screen
width = 750
height = 750
screen = pygame.display.set_mode((width, height))

#sprites load
playerShip = pygame.image.load("Game Assets/PlayerShip.png")
playerShip = pygame.transform.scale(playerShip, (180, 120))
playerBullet = pygame.image.load("Game Assets/PlayerBullet.png")
playerBullet = pygame.transform.scale(playerBullet, (20,20))
bg = pygame.image.load("Game Assets/Background.jpg")
bg = pygame.transform.scale(bg, (width, height))

#background music
mixer.music.load("Game Assets/background.wav")
mixer.music.play(-1)
mixer.music.set_volume(2)

#player coordinates
playerX = (width/2)-90
playerY = 600
playerX_change = 0
playerY_change = 0

#enemy coordinates
enemyShip = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num = 5
for i in range(num):
    enemyShip.append(pygame.image.load("Game Assets/EnemyShip.png"))
    enemyShip[i] = pygame.transform.scale(enemyShip[i], (150, 100))
    enemyX.append(random.randint(-20, width-130))
    enemyY.append(random.randint(0, 100))
    enemyX_change.append(2.3)
    enemyY_change.append(0.5)

#player bullet coordinates
pBulletX = 0
pBulletY = 600
pBulletY_change = 6
pBulletState = "ready"

#score
score = 0;
font = pygame.font.Font('freesansbold.ttf', 34)
textX = 10
textY = 10

#game over
gameOverFont = pygame.font.Font('freesansbold.ttf', 50)
gTextX = width/2 - 100
gTextY = height/2

def player(x, y):
    screen.blit(playerShip, (x, y))

def enemy(x, y, i):
    screen.blit(enemyShip[i], (x, y))

def firePBullet(x, y):
    global pBulletState
    pBulletState = "fire"
    screen.blit(playerBullet,(x + 80, y + 25))

def showScore(x, y):
    sc = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(sc, (x, y))

def isCollision(bulletX, bulletY, enemyX, enemyY):
    distance = math.sqrt(pow(bulletX - enemyX, 2) + pow(bulletY - enemyY, 2))
    if distance <= 50:
        return True
    else:
        return False

def gameOver(x, y):
    gmov = font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(gmov, (x, y))

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
                bulletSound = mixer.Sound("Game Assets\laser.mp3")
                bulletSound.play()
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
    for i in range(num):
        enemyX[i] += enemyX_change[i]
        enemyY[i] += enemyY_change[i]
        if enemyX[i] <= -20:
            enemyX_change[i] = 2.3
            enemyX[i] += enemyX_change[i]

        if enemyX[i] >= width - 130:
            enemyX_change[i] = -2.3
            enemyX[i] += enemyX_change[i]

        enemy(enemyX[i], enemyY[i], i)

        if enemyY[i] > 600:
            for j in range(num):
                enemyY[j] = 1000
            gameOver(gTextX, gTextY)
            break


    #bullet movement
    if pBulletY <= -30:
        pBulletY = 600
        pBulletState = "ready"
    if pBulletState == "fire":
        firePBullet(pBulletX, pBulletY)
        pBulletY -= pBulletY_change

    #collision
    for i in range(num):
        collision = isCollision(pBulletX, pBulletY, enemyX[i], enemyY[i])
        if collision:
            collisionSound = mixer.Sound("Game Assets/explosion.wav")
            collisionSound.play()
            pBulletY = 600
            pBulletState = "ready"
            score += 1
            #print(score)
            enemyX[i] = random.randint(-20, width - 130)
            enemyY[i] = random.randint(0, 100)

    player(playerX, playerY)
    showScore(textX, textY)
    pygame.display.update()
