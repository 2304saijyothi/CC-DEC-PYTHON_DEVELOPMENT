import sys 
import random
from pygame.locals import *
import pygame

fps = 32
bird = 'resources/images_res/bird.png'
bg = 'resources/images_res/background.png'
pipe = 'resources/images_res/pipe.png'
swidth = 289
IMAGES = {}
AUDIO = {}
sheigth = 511
game_screen = pygame.display.set_mode((swidth, sheigth))
gy = sheigth * 0.8

def Home():

    playerx = int(swidth/5)
    playery = int((sheigth - IMAGES['player'].get_height())/2)
    messagex = int((swidth - IMAGES['message'].get_width())/1.5)
    messagey = int(sheigth*0.003)
    basex = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                return
            else:
                game_screen.blit(IMAGES['background'], (0, 0))    
                game_screen.blit(IMAGES['player'], (playerx, playery))    
                game_screen.blit(IMAGES['message'], (messagex,messagey ))    
                game_screen.blit(IMAGES['base'], (basex, gy))    
                pygame.display.update()
                FPSCLOCK.tick(fps)

def mainGame():
    score = 0
    newPipe1 = getranpipe()
    newPipe2 = getranpipe()
    playerx = int(swidth/5)
    playery = int(swidth/2)
    basex = 0

    upperPipes = [
        {'x': swidth+200+(swidth/2), 'y':newPipe2[0]['y']},
        {'x': swidth+200, 'y':newPipe1[0]['y']},

    ]

    lowerPipes = [
        {'x': swidth+200+(swidth/2), 'y':newPipe2[1]['y']},
        {'x': swidth+200, 'y':newPipe1[1]['y']},

    ]

    pipeVelX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8
    playerFlapped = False 


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    AUDIO['wing'].play()


        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)
        if crashTest:
            return     

        playerMidPos = playerx + IMAGES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + IMAGES['pipe'][0].get_width()/2
            if pipeMidPos<= playerMidPos < pipeMidPos +4:
                score +=1
                print(f"Your score is {score}") 
                AUDIO['point'].play()


        if playerVelY <playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False            
        playerHeight = IMAGES['player'].get_height()
        playery = playery + min(playerVelY, gy - playery - playerHeight)

        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        
        if 0<upperPipes[0]['x']<5:
            newpipe = getranpipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])


        if upperPipes[0]['x'] < -IMAGES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        game_screen.blit(IMAGES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            game_screen.blit(IMAGES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            game_screen.blit(IMAGES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        game_screen.blit(IMAGES['base'], (basex, gy))
        game_screen.blit(IMAGES['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += IMAGES['numbers'][digit].get_width()
        Xoffset = (swidth - width)/2

        for digit in myDigits:
            game_screen.blit(IMAGES['numbers'][digit], (Xoffset, sheigth*0.12))
            Xoffset += IMAGES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(fps)

def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery> gy - 25  or playery<0:
        AUDIO['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = IMAGES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < IMAGES['pipe'][0].get_width()):
            AUDIO['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + IMAGES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < IMAGES['pipe'][0].get_width():
            AUDIO['hit'].play()
            return True

    return False

def getranpipe():

    pipeHeight = IMAGES['pipe'][0].get_height()
    offset = sheigth/3
    y2 = offset + random.randrange(0, int(sheigth - IMAGES['base'].get_height()  - 1.2 *offset))
    pipeX = swidth + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1}, 
        {'x': pipeX, 'y': y2}
    ]
    return pipe


if __name__ == "__main__":

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird')
    IMAGES['numbers'] = ( 
        pygame.image.load('resources/images_res/0.png').convert_alpha(),
        pygame.image.load('resources/images_res/1.png').convert_alpha(),
        pygame.image.load('resources/images_res/2.png').convert_alpha(),
        pygame.image.load('resources/images_res/3.png').convert_alpha(),
        pygame.image.load('resources/images_res/4.png').convert_alpha(),
        pygame.image.load('resources/images_res/5.png').convert_alpha(),
        pygame.image.load('resources/images_res/6.png').convert_alpha(),
        pygame.image.load('resources/images_res/7.png').convert_alpha(),
        pygame.image.load('resources/images_res/8.png').convert_alpha(),
        pygame.image.load('resources/images_res/9.png').convert_alpha(),
    )

    IMAGES['message'] =pygame.image.load('resources/images_res/message.png').convert_alpha()
    IMAGES['base'] =pygame.image.load('resources/images_res/down-bg.png').convert_alpha()
    IMAGES['pipe'] =(pygame.transform.rotate(pygame.image.load( pipe).convert_alpha(), 180), 
    pygame.image.load(pipe).convert_alpha()
    )

    AUDIO['die'] = pygame.mixer.Sound('resources/audio_res/die.wav')
    AUDIO['hit'] = pygame.mixer.Sound('resources/audio_res/hit_pipe.wav')
    AUDIO['point'] = pygame.mixer.Sound('resources/audio_res/score-a-point.wav')
    AUDIO['swoosh'] = pygame.mixer.Sound('resources/audio_res/fly.wav')
    AUDIO['wing'] = pygame.mixer.Sound('resources/audio_res/wings.wav')

    IMAGES['background'] = pygame.image.load(bg).convert()
    IMAGES['player'] = pygame.image.load(bird).convert_alpha()

    while True:
        Home()
        mainGame()