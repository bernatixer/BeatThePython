import sys, pygame
from pygame.locals import *
import time
import random

TILE_SIZE = 32
pygame.init()

SIZE = WIDTH, HEIGHT = 768, 768

COLORS = {
    "black": (0,0,0),
    "white": (255,255,255),
    "red": (255,0,0),
}

FOOD = []
DISPLAY = pygame.display.set_mode(SIZE)

class Snake:
    def __init__(self, up, down, right, left, color):
        self.up = up
        self.down = down
        self.right = right
        self.left = left
        self.color = color
        self.CURR_PresedKey = None
        self.gameOver = False
        self.POSITIONS = [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5)]
        self.SCORE = 0
    
    def drawSnake(self,x,y):
        pygame.draw.rect(DISPLAY,self.color,(x,y,TILE_SIZE,TILE_SIZE))

    def moveSnake(self):
        newPos = None
        if self.CURR_PresedKey == self.left:
            newPos = (self.POSITIONS[-1][0] - 1, self.POSITIONS[-1][1])
        if self.CURR_PresedKey == self.right:
            newPos = (self.POSITIONS[-1][0] + 1, self.POSITIONS[-1][1])
        if self.CURR_PresedKey == self.up:
            newPos = (self.POSITIONS[-1][0], self.POSITIONS[-1][1] - 1)
        if self.CURR_PresedKey == self.down:
            newPos = (self.POSITIONS[-1][0], self.POSITIONS[-1][1] + 1)

        if newPos:
            if newPos[0] < 0 or newPos[1] < 0 or newPos[0] >= WIDTH // TILE_SIZE or newPos[1] >= HEIGHT // TILE_SIZE or newPos in self.POSITIONS:
                print("Final Score:", self.SCORE)
                self.gameOver = True
            if len(self.POSITIONS) > self.SCORE + 5:
                del self.POSITIONS[0]            
            self.POSITIONS.append(newPos)

    def update(self):
        if not self.gameOver:
            for pos in self.POSITIONS:
                self.drawSnake(pos[0] * TILE_SIZE, pos[1] * TILE_SIZE)
            if self.POSITIONS[-1] in FOOD:
                del FOOD[FOOD.index(self.POSITIONS[-1])]
                self.SCORE += 1
    
    def newEvent(self,event):
        a = self.CURR_PresedKey == self.right and event.key == self.left
        b = self.CURR_PresedKey == self.left and event.key == self.right
        c = self.CURR_PresedKey == self.up and event.key == self.down
        d = self.CURR_PresedKey == self.down and event.key == self.up
        
        if not a and not b and not c and not d:
            self.CURR_PresedKey = event.key

def drawFood(x,y):
    pygame.draw.rect(DISPLAY,COLORS['red'],(x,y,TILE_SIZE,TILE_SIZE))

def createFood():
    FOOD.append((random.randint(1,WIDTH//TILE_SIZE),random.randint(1,HEIGHT//TILE_SIZE)))

pygame.time.set_timer(USEREVENT + 1, 150) # move snake
pygame.time.set_timer(USEREVENT + 2, 1500) # Create Food

Player1 = Snake(color = COLORS["white"], up = pygame.K_UP, down = pygame.K_DOWN, right = pygame.K_RIGHT, left = K_LEFT)

while True:    
    DISPLAY.fill(COLORS['black'])
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            Player1.newEvent(event)
        if event.type == USEREVENT + 1:
            Player1.moveSnake()
        if event.type == USEREVENT + 2:
            createFood()

    Player1.update()

    for pos in FOOD:
        drawFood(pos[0] * TILE_SIZE, pos[1] * TILE_SIZE)

    pygame.display.flip()