#setup
'START BLOCK'
import pygame
import keyboard
import math

from sprites import *
from map import *

pygame.init()

screen = pygame.display.set_mode((1200,600))

running = True

clock = pygame.time.Clock()

font = pygame.font.Font(None,32)
'END BLOCK'

#environment
'START BLOCK'
groundshift = 0

#should only be used for rendering, not collisions or anything else
#IMPORTANT - THIS IS LITERALLY USED TO RENDER EVERYTHING IN THE ENTIRE GAME
camX = 600
#literally used for nothing
camY = 0

time = 0
day = 1
daycolor = (200,200,250)
'END BLOCK'

#players
'START BLOCK'
class player1:
    X = 0
    Y = 455

    direction = 'left'
    move = 'none'

    class sword:
        sprite = sword #not actually used
        
        sword = 0
        length = 0
        state = 'none'

        rect = sprite.get_rect()

    sprite = p1
    rect = sprite.get_rect()
    rect.topleft = (X,Y)

class player2:
    X = 0
    Y = 455

    direction = 'left'
    move = 'none'

    class sword:
        sprite = sword
        
        sword = 0
        length = 0
        state = 'none'

        rect = sprite.get_rect()
        
    sprite = p2
    rect = sprite.get_rect()
    rect.topleft = (X,Y)

screenX = 0

bothmoving = False

speed = 3

health = 100
'END BLOCK'

#enemies
'START BLOCK'
enemies = []

enemytimer = 500
'END BLOCK'

#main loop
while running:

    #quit
    'START BLOCK'
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    'END BLOCK'

    #environment
    'START BLOCK'
    #sky
    screen.fill(daycolor)

    time = time + 0.1

    #sunrise
    if time > 0 and time < 200:
        daycolor = (0+time,0+time,50+time)
    #day
    if time > 200 and time < 1000:
        daycolor = (200,200,250)
    #sunset
    if time > 1000 and time < 1200:
        daycolor = (200-time+1000,200-time+1000,250-time+1000)
    #night
    if time > 1200 and time < 2000:
        daycolor = (0,0,50)
    if time > 2000:
        time = 0
        day = day + 1

    #ground
    for i in range (17):
        if bothmoving:
            groundshift = camX%80
        screen.blit(ground,(-80+i*80+groundshift,camY+500))

    #houses
    for houseX in houseXs:
        screen.blit(house,(camX+houseX,camY+400))
    for doorX in doorXs:
        screen.blit(doorsprite,(camX+doorX,camY+450))

    #grass
    for grass in grassdata:
        if camX+grass['X'] > -100 and camX+grass['X'] < 1300:
            if grass['type'] == 0:
                grasssprite = grass1
            if grass['type'] == 1:
                grasssprite = grass2
            screen.blit(grasssprite,(camX+grass['X'],camY+490))
    'END BLOCK'

    #die
    'START BLOCK'
    if health <= 0:
        running = False
    'END BLOCK'

    #movement
    'START BLOCK'
    #p1
    a = keyboard.is_pressed('a')
    d = keyboard.is_pressed('d')

    #p2
    left = keyboard.is_pressed('left')
    right = keyboard.is_pressed('right')

    #p1
    if a != d:
        if a:
            player1.X = player1.X - speed
            player1.move = 'left'
            player1.direction = 'left'
        if d:
            player1.X = player1.X + speed
            player1.move = 'right'
            player1.direction = 'right'

    else:
        player1.move = 'none'

    #p2
    if left != right:
        if left:
            player2.X = player2.X - speed
            player2.direction = 'left'
            player2.move = 'left'
        if right:
            player2.X = player2.X + speed
            player2.move = 'right'
            player2.direction = 'right'
            
    else:
        player2.move = 'none'

    #p1
    if camX+player1.X < 50:
        player1.X = 50 - camX
    if camX+player1.X > 1130:
        player1.X = 1130 - camX

    #p2
    if camX+player2.X < 50:
        player2.X = 50 - camX
    if camX+player2.X > 1130:
        player2.X = 1130 - camX

    #rect used for collisions
    player1.rect = player1.sprite.get_rect()
    player1.rect.topleft = (player1.X,player1.Y)

    player2.rect = player2.sprite.get_rect()
    player2.rect.topleft = (player2.X,player2.Y)

    #camera
    if player1.move == player2.move:
        if player1.move == 'left':
            camX = camX + 3
        if player1.move == 'right':
            camX = camX - 3

        if not player1.move == 'none':
            bothmoving = True

    if player1.direction == 'right':
        screen.blit(pygame.transform.scale(player1.sprite,(20,45)),(camX+player1.X,camY+player1.Y))
    if player1.direction == 'left':
        screen.blit(pygame.transform.flip(pygame.transform.scale(player1.sprite,(20,45)),True,False),(camX+player1.X,camY+player1.Y))
    if player2.direction == 'right':
        screen.blit(pygame.transform.scale(player2.sprite,(20,45)),(camX+player2.X,camY+player2.Y))
    if player2.direction == 'left':
        screen.blit(pygame.transform.flip(pygame.transform.scale(player2.sprite,(20,45)),True,False),(camX+player2.X,camY+player2.Y))
    'END BLOCK'
    
    #sword
    'START BLOCK'
    #p1
    if player1.sword.sword > 0:
        player1.sword.sword = player1.sword.sword - 1
        
    if player1.sword.sword < 0:
        player1.sword.sword = player1.sword.sword + 1
        if player1.sword.sword == 0:
            player1.sword.sword = 30
        
    if keyboard.is_pressed('w'):
        if player1.sword.sword == 0:
            player1.sword.sword = -30
            player1.sword.length = 0
            player1.sword.state = 'out'

    if player1.sword.sword < 0: 
        if player1.sword.state == 'out':
            player1.sword.length = player1.sword.length + 1
            if player1.sword.length == 15:
                player1.sword.state = 'in'

        if player1.sword.state == 'in':
            player1.sword.length = player1.sword.length - 1

        if player1.direction == 'left':
            screen.blit(sword,(camX+player1.X-20-player1.sword.length,camY+player1.Y+10))
            player1.sword.rect.topleft = (player1.X-20-player1.sword.length,player1.Y+10)
        if player1.direction == 'right':
            screen.blit(pygame.transform.flip(sword,True,False),(camX+player1.X+10+player1.sword.length,camY+player1.Y+10))
            player1.sword.rect.topleft = (player1.X+10+player1.sword.length,player1.Y+10)

    #p2
    if player2.sword.sword > 0:
        player2.sword.sword = player2.sword.sword - 1
        
    if player2.sword.sword < 0:
        player2.sword.sword = player2.sword.sword + 1
        if player2.sword.sword == 0:
            player2.sword.sword = 30
        
    if keyboard.is_pressed('up'):
        if player2.sword.sword == 0:
            player2.sword.sword = -30
            player2.sword.length = 0
            player2.sword.state = 'out'

    if player2.sword.sword < 0: 
        if player2.sword.state == 'out':
            player2.sword.length = player2.sword.length + 1
            if player2.sword.length == 15:
                player2.sword.state = 'in'

        if player2.sword.state == 'in':
            player2.sword.length = player2.sword.length - 1

        if player2.direction == 'left':
            screen.blit(sword,(camX+player2.X-20-player2.sword.length,camY+player2.Y+10))
            player2.sword.rect.topleft = (player2.X-20-player2.sword.length,camY+player2.Y+10)
        if player2.direction == 'right':
            screen.blit(pygame.transform.flip(sword,True,False),(camX+player2.X+10+player2.sword.length,camY+player2.Y+10))
            player2.sword.rect.topleft = (player2.X+10+player2.sword.length,camY+player2.Y+10)
    'END BLOCK'
    
    #enemy spawning
    'START BLOCK'
    enemytimer = enemytimer - 1

    #spawn enemies
    if enemytimer < 1:
        if random.randint(0,1) == 1:
            enemyX = -100
        else:
            enemyX = 1300
            
        enemies.append({'type':'normal',
                        'X':enemyX-camX,'Y':460+camY,'direction':'left','knockback':0,
                        'target':'none','targettimer':0,
                        'health':2,'hurttimer':0,
                        'attacktimer':0,'damage':1})
            
        enemytimer = random.randint(200,350)

    #clear dead enemies
    for enemy in enemies:
        if enemy['health'] < 1:
            enemies.remove(enemy)
    'END BLOCK'

    #enemy AI
    'START BLOCK'
    for enemy in enemies:

        if enemy['type'] == 'normal':
            enemyrect = zombie1.get_rect()
            enemyrect.topleft = (enemy['X'],enemy['Y'])

            #whether or not the zombie can take damage
            if enemy['hurttimer'] > 0:
                enemy['hurttimer'] = enemy['hurttimer'] - 1

            #targeting
            if enemy['targettimer'] > 0:
                enemy['targettimer'] = enemy['targettimer'] - 1

            if enemy['targettimer'] == 0:
                if math.dist(enemyrect.center,player1.rect.center) > math.dist(enemyrect.center,player2.rect.center):
                    enemy['target'] = '2'
                    enemy['targettimer'] = 120
                if math.dist(enemyrect.center,player2.rect.center) > math.dist(enemyrect.center,player1.rect.center):
                    enemy['target'] = '1'
                    enemy['targettimer'] = 120

            #chase            
            if enemy['target'] == '1' and not abs(enemyrect.centerx-player1.rect.centerx) < 1:
                if enemyrect.centerx > player1.rect.centerx:
                    enemy['X'] = enemy['X'] - 1
                    enemy['direction'] = 'left'
                if enemyrect.centerx < player1.rect.centerx:
                    enemy['X'] = enemy['X'] + 1
                    enemy['direction'] = 'right'
        
            if enemy['target'] == '2' and not abs(enemyrect.centerx-player2.rect.centerx) < 15:
                if enemyrect.centerx > player2.rect.centerx:
                    enemy['X'] = enemy['X'] - 1
                    enemy['direction'] = 'left'
                if enemyrect.centerx < player2.rect.centerx:
                    enemy['X'] = enemy['X'] + 1
                    enemy['direction'] = 'right'

            #when hit
            if (enemyrect.colliderect(player1.sword.rect) and player1.sword.sword < 0) or (enemyrect.colliderect(player2.sword.rect) and player2.sword.sword < 0):
                if enemy['hurttimer'] == 0:
                    enemy['health'] = enemy['health'] - 1
                    enemy['knockback'] = 7
                    enemy['hurttimer'] = 40

            #takes knockback
            if enemy['knockback'] > 0:
                if enemy['direction'] == 'left':
                    enemy['X'] = enemy['X'] + enemy['knockback']
                if enemy['direction'] == 'right':
                    enemy['X'] = enemy['X'] - enemy['knockback']

                enemy['knockback'] = enemy['knockback'] - 1

            #attack
            if enemy['target'] == '1':
                if abs(enemyrect.centerx-player1.rect.centerx) < 30:
                    if enemy['attacktimer'] == 0:
                        enemy['attacktimer'] = 40
                    else:
                        enemy['attacktimer'] = enemy['attacktimer'] - 1
                        if enemy['attacktimer'] == 0:
                            health = health - enemy['damage']

            if enemy['target'] == '2':
                if abs(enemyrect.centerx-player2.rect.centerx) < 30:
                    if enemy['attacktimer'] == 0:
                        enemy['attacktimer'] = 40
                    else:
                        enemy['attacktimer'] = enemy['attacktimer'] - 1
                        if enemy['attacktimer'] == 0:
                            health = health - enemy['damage']
                              

            #draws the sprite
            if enemy['direction'] == 'left':
                screen.blit(pygame.transform.flip(zombie1,True,False),(camX+enemy['X'],camY+enemy['Y']))
            if enemy['direction'] == 'right':
                screen.blit(zombie1,(camX+enemy['X'],camY+enemy['Y']))
    'END BLOCK'

    #displays
    'START BLOCK'
    healthdisplay = font.render(str(health),True,(0,0,0))
    screen.blit(heart,(30,30))
    screen.blit(healthdisplay,(60,30))
    'END BLOCK'
    
    #necessary stuff
    'START BLOCK'
    pygame.display.update()
    clock.tick(60)
    'END BLOCK'

#quit
pygame.quit()
