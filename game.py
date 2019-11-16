import pygame as pg
from pygame.locals import *
from settings import *
from snake import Snake
import random
import sys
import train
import numpy as np
import json
from tempfile import TemporaryFile

generation = 0
max_score = 0

class Game:
    def __init__(self):
        pg.init()
        self.FOOD = []
        self.DISPLAY = pg.display.set_mode(SIZE)
        self.FONT = pg.font.Font("fonts/RobotoMono-Medium.ttf", 20)

        pg.time.set_timer(USEREVENT + 1, 1) # move snake
        pg.time.set_timer(USEREVENT + 2, 15) # Create Food
        pg.time.set_timer(USEREVENT + 3, 60000) # Save weigths

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
                    if not train.train:
                        with open('storage.json', 'w') as fp:
                            json.dump(train.storage, fp)
                        np.savetxt("Q.txt", train.Q)

            self.Player1.update(self.FOOD)
            if not self.FOOD:
                self.createFood()

            for pos in self.FOOD:
                self.drawFood(pos[0] * TILE_SIZE, pos[1] * TILE_SIZE)

            if not train.train:
                score = self.FONT.render('Score: ' + str(self.Player1.SCORE), True, COLORS["text"])
                self.DISPLAY.blit(score, (10, 5))

                global max_score, generation
                maxScore = self.FONT.render('Max score: ' + str(max_score), True, COLORS["text"])
                self.DISPLAY.blit(maxScore, (10, 30))

                epoch = self.FONT.render('Generation: ' + str(generation), True, COLORS["text"])
                self.DISPLAY.blit(epoch, (10, 55))

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
        global max_score
        if self.Player1.SCORE > max_score:
            max_score = self.Player1.SCORE
        global generation
        generation += 1
        self.Player1 = Snake(color = COLORS["white"], up = pg.K_UP, down = pg.K_DOWN, right = pg.K_RIGHT, left = K_LEFT, display = self.DISPLAY, game_over = self.game_over)


if __name__== "__main__":
    global GAME
    GAME = Game()
