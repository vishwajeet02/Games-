import math

import pygame
import random
from pygame import mixer
# intialize the pygame /permanent line 1
pygame.init()  
# create a screen
screen=pygame.display.set_mode((800,600))
# Background
background = pygame.image.load('background.png')
#background music
mixer.music.load('background.wav')#music as baar baar play karna h
mixer.music.play(-1)  #-1 for loop playing
#Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)
 
#player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0
#playerY_change = 0

#enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = [] 
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,735)) #for spawing at different places
    enemyY.append(random.randint(50,150))
    enemyX_change.append(1)
    enemyY_change.append(70)

#bullet
# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving
bulletImg=pygame.image.load('bullet.png')
bulletX = 0 #for spawing at different places
bulletY = 480
bulletX_change = 0
bulletY_change = 1.5
bullet_state = "ready"

#Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10
#game over
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x,y):
    score = font.render("Score :"+ str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))
    
def player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))
 
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))   
    
def fire_bullet(x,y):
    global bullet_state #global so that we can call state
    bullet_state = "fire" # creating that bullet
    screen.blit(bulletImg, (x + 16 , y + 10)) #+16 and +10 k mtlb ye peak se niklega
    
def isCollison(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX,2)+math.pow(enemyY-bulletY,2))
    if distance < 27:
        return True
    else:
        return False
    
    
    
running=True
while running:
    #RGB=red,green,blue     
    screen.fill((0,0,0)) 
    #background image
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        #if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1
            if event.key == pygame.K_RIGHT:
                playerX_change = 1
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    bulletX = playerX # to jo bullet k x value h ussi pe rahega so 
                    fire_bullet(bulletX,bulletY)# after calling wo x k value pe hein shoot karega  
                
            #if event.key == pygame.K_UP:
                #playerY_change = -0.1
           # if event.key == pygame.K_DOWN:
                #playerY_change = 0.1 
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT: #or event.key == pygame.K_UP or event.key == pygame.K_DOWN :
                playerX_change = 0
                
                
                
                
    #playerY += playerY_change  
    playerX += playerX_change #it changes the player location
    if playerX <= 0: #Boundaries
        playerX = 0
    elif playerX >= 736:
        playerX = 736
        
    #enemy movement
    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000 #agar hua to rest of the enemies goes beyond the pixel
            game_over_text()
            break
        
        enemyX[i] += enemyX_change[i]  
        if enemyX[i] <= 0: 
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]
        #collision
        collision = isCollison(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value+=1
            enemyX[i] = random.randint(0,735) 
            enemyY[i] = random.randint(50,150)
        
        enemy(enemyX[i],enemyY[i],i)
        
     
    #bullet movement
    if bulletY<=0:   #basically jaise hein ek bullet y axis m -ve jata h we are making the state of bullet to ready again
        bulletY = 480 #so that we can shoot multiple bullet
        bullet_state = "ready"
    if bullet_state == "fire":  
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change
    
     
        
    player(playerX,playerY)#always after screen bcoz screen is drawn first then on top is the player
    show_score(textX,textY)
    pygame.display.update()   #permanent line 2