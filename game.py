import pygame as pg
from pygame.locals import *
from settings import *
from snake import Snake
import random
import sys
import train
import json

class Game:
    def __init__(self):
        pg.init()
        self.FOOD = []
        self.DISPLAY = pg.display.set_mode(SIZE)
        self.FONT = pg.font.Font("fonts/RobotoMono-Medium.ttf", 20)

        pg.time.set_timer(USEREVENT + 1, 1) # move snake
        pg.time.set_timer(USEREVENT + 2, 15) # Create Food
        pg.time.set_timer(USEREVENT + 3, 100000) # Save weigths

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
                    self.Player1.moveSnake()
                if event.type == USEREVENT + 2:
                    self.createFood()
                if event.type == USEREVENT + 3:
                    with open('storage.json', 'w') as fp:
                        json.dump(train.storage, fp)

                    with open('Q.json', 'w') as fp:
                        json.dump(train.Q, fp)
                        
                    # with open('storage.json', 'r') as fp:
                    #     data = json.load(fp)

            self.Player1.update(self.FOOD)
            if not self.FOOD:
                self.createFood()

            for pos in self.FOOD:
                self.drawFood(pos[0] * TILE_SIZE, pos[1] * TILE_SIZE)

            score = self.FONT.render('Score: ' + str(self.Player1.SCORE), True, COLORS["text"])
            self.DISPLAY.blit(score, (10, 5))  # render score

            pg.display.update()

    def drawFood(self, x,y):
        pg.draw.rect(self.DISPLAY,COLORS['red'],(x,y,TILE_SIZE,TILE_SIZE))

    def createFood(self):
        if len(self.FOOD) == 0:
            newPos = self.Player1.POSITIONS[0]
            while newPos in self.Player1.POSITIONS:
                newPos = (random.randint(1,(WIDTH//TILE_SIZE) -1),random.randint(1,(HEIGHT//TILE_SIZE) -1))
            
            self.FOOD.append(newPos)

    def getScore(self):
        return self.Player1.SCORE

    def game_over(self):
        self.Player1 = Snake(color = COLORS["white"], up = pg.K_UP, down = pg.K_DOWN, right = pg.K_RIGHT, left = K_LEFT, display = self.DISPLAY, game_over = self.game_over)


if __name__== "__main__":
    global GAME
    GAME = Game()
