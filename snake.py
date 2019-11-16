import sys, pygame
from pygame.locals import *
import time
import random

SCORE = 0

TILE_SIZE = 32
pygame.init()

SIZE = WIDTH, HEIGHT = 768, 768

ARROW_KEYS = [pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT]

COLORS = {
    "black": (0,0,0),
    "white": (255,255,255),
    "red": (255,0,0),
}

POSITIONS = [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5)]
FOOD = []
DISPLAY = pygame.display.set_mode(SIZE)

CURR_PresedKey = None
LST_PressedKey = None

def drawFood(x,y):
    pygame.draw.rect(DISPLAY,COLORS['red'],(x,y,TILE_SIZE,TILE_SIZE))

def drawSnake(x,y):
    pygame.draw.rect(DISPLAY,COLORS['white'],(x,y,TILE_SIZE,TILE_SIZE))

def createFood():
    FOOD.append((random.randint(1,WIDTH//TILE_SIZE),random.randint(1,HEIGHT//TILE_SIZE)))

def moveSnake():
    newPos = None

    if CURR_PresedKey == pygame.K_LEFT:
        newPos = (POSITIONS[-1][0] - 1,POSITIONS[-1][1])
    if CURR_PresedKey == pygame.K_RIGHT:
        newPos = (POSITIONS[-1][0] + 1,POSITIONS[-1][1])
    if CURR_PresedKey == pygame.K_UP:
        newPos = (POSITIONS[-1][0],POSITIONS[-1][1] - 1)
    if CURR_PresedKey == pygame.K_DOWN:
        newPos = (POSITIONS[-1][0],POSITIONS[-1][1] + 1)

    if newPos:
        if newPos[0] < 0 or newPos[1] < 0 or newPos[0] >= WIDTH // TILE_SIZE or newPos[1] >= HEIGHT // TILE_SIZE or newPos in POSITIONS:
            print("Final Score:",SCORE)
            sys.exit(0)
            #Game Over
        if len(POSITIONS) > SCORE + 5:
            del POSITIONS[0]            
        POSITIONS.append(newPos)

pygame.time.set_timer(USEREVENT + 1, 150) # move snake
pygame.time.set_timer(USEREVENT + 2, 1500) # Create Food

while True:    
    DISPLAY.fill(COLORS['black'])

    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key in ARROW_KEYS:
            a = CURR_PresedKey == pygame.K_RIGHT and event.key == K_LEFT
            b = CURR_PresedKey == pygame.K_LEFT and event.key == K_RIGHT
            c = CURR_PresedKey == pygame.K_UP and event.key == K_DOWN
            d = CURR_PresedKey == pygame.K_DOWN and event.key == K_UP
            
            if not a and not b and not c and not d:
                CURR_PresedKey = event.key
        if event.type == USEREVENT + 1:
            moveSnake()
        if event.type == USEREVENT + 2:
            createFood()
    
    for pos in POSITIONS:
        drawSnake(pos[0] * TILE_SIZE, pos[1] * TILE_SIZE) 

    if POSITIONS[-1] in FOOD:
        del FOOD[FOOD.index(POSITIONS[-1])]
        SCORE += 1

    for pos in FOOD:
        drawFood(pos[0] * TILE_SIZE, pos[1] * TILE_SIZE)

    pygame.display.flip()