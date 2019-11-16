import pygame as pg
from pygame.locals import *
from settings import *
from snake import Snake
import random
import sys
import train

FPS = 150
fpsClock = pg.time.Clock()

class Game:
    def __init__(self, game_over):
        pg.init()
        self.game_over = game_over
        self.FOOD = []
        self.DISPLAY = pg.display.set_mode(SIZE)
        self.FONT = pg.font.Font("fonts/RobotoMono-Medium.ttf", 20)

        pg.time.set_timer(USEREVENT + 1, 1000) # move snake
        pg.time.set_timer(USEREVENT + 2, 1500) # Create Food

        self.Player1 = Snake(color = COLORS["white"], up = pg.K_UP, down = pg.K_DOWN, right = pg.K_RIGHT, left = K_LEFT, display = self.DISPLAY, game_over = self.game_over)
        self.createFood()

        while True:
            self.DISPLAY.fill(COLORS['black'])
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    self.Player1.newEvent(event)
                if event.type == USEREVENT + 1:
                    action = train.chooseAction(self.Player1, self.FOOD)
                    self.Player1.act(action)
                    print("Direction: ", self.Player1.getSnakeDirection(), " Food: ", self.Player1.getFoodDirection(self.FOOD))
                    self.Player1.moveSnake()
                if event.type == USEREVENT + 2:
                    self.createFood()

            self.Player1.update(self.FOOD)

            for pos in self.FOOD:
                self.drawFood(pos[0] * TILE_SIZE, pos[1] * TILE_SIZE)

            score = self.FONT.render('Score: ' + str(self.Player1.SCORE), True, COLORS["text"])
            self.DISPLAY.blit(score, (10, 5))  # render score

            pg.display.update()
            fpsClock.tick(FPS)

    def drawFood(self, x,y):
        pg.draw.rect(self.DISPLAY,COLORS['red'],(x,y,TILE_SIZE,TILE_SIZE))

    def createFood(self):
        if len(self.FOOD) == 0:
            self.FOOD.append((random.randint(1,WIDTH//TILE_SIZE),random.randint(1,HEIGHT//TILE_SIZE)))

    def getScore(self):
        return self.Player1.SCORE


def gameOver():
    print("HAS PERDUT")
    exit()

if __name__== "__main__":
    game = Game(gameOver)
