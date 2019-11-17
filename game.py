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
import pygame_textinput
import requests

API_ENDPOINT = "http://localhost"
bg = pg.image.load("background.png")
textinput = pygame_textinput.TextInput()
train_ = False
if not train_:
    with open('stats.json', 'r') as fp:
        stats = json.load(fp)
        if "generation" in stats and "max_score" in stats:
            generation = stats["generation"]
            max_score = stats["max_score"]
        else:
            generation = 0
            max_score = 0
else:
    generation = 0
    max_score = 0

class Game:
    def __init__(self):

        self.money = pg.image.load("images/money.png")
        self.swiss = pg.image.load("images/swiss.png")
        self.swiss2 = pg.image.load("images/swiss2.png")
        self.moneyrect = self.money.get_rect()
        self.swissrect = self.swiss.get_rect()
        self.swiss2rect = self.swiss2.get_rect()

        pg.init()
        pg.mixer.music.load('background.mp3')
        pg.mixer.music.play(-1)
        self.FOOD = []
        self.DISPLAY = pg.display.set_mode(SIZE)
        self.FONT = pg.font.Font("fonts/RobotoMono-Medium.ttf", 20)

        self.start = False
        while not self.start:
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.start = True

            self.DISPLAY.fill(COLORS['black'])
            start = self.FONT.render('Press SPACE to Start', True, COLORS["swiss"])
            self.DISPLAY.blit(start, (WIDTH/2 - 125, HEIGHT/2))

            pg.display.update()

        pg.time.set_timer(USEREVENT + 1, 100) # move snake
        pg.time.set_timer(USEREVENT + 2, 15) # Create Food
        pg.time.set_timer(USEREVENT + 3, 20000) # Save weigths

        self.Player1 = Snake(color = COLORS["white"], up = pg.K_UP, down = pg.K_DOWN, right = pg.K_RIGHT, left = K_LEFT, display = self.DISPLAY, game_over = None)

        self.Player2 = Snake(color = COLORS["snake"], up = pg.K_w, down = pg.K_s, right = pg.K_d, left = K_a, display = self.DISPLAY, game_over = self.go)

        self.createFood()

        global max_score, generation
        while True:
            self.DISPLAY.blit(bg, (0, 0))

            # self.DISPLAY.fill(COLORS['black'])
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    self.Player1.newEvent(event)

                    self.Player2.newEvent(event)
                if event.type == USEREVENT + 1:
                    action = train.chooseAction(self.Player1, self.FOOD)
                    self.Player1.act(action)
                    self.Player1.moveSnake()

                    self.Player2.moveSnake()
                if event.type == USEREVENT + 2:
                    self.createFood()
                if event.type == USEREVENT + 3:
                    if not train_:
                        with open('storage.json', 'w') as fp:
                            json.dump(train.storage, fp)
                        with open('stats.json', 'w') as fp:
                            json.dump({'max_score': max_score, 'generation': generation}, fp)
                        np.savetxt("Q.txt", train.Q)

            self.Player1.update(self.FOOD, self.DISPLAY, self.swiss, self.swissrect)
            
            self.Player2.update(self.FOOD, self.DISPLAY, self.swiss2, self.swiss2rect)

            if not self.FOOD:
                self.createFood()

            for pos in self.FOOD:
                self.moneyrect.x = pos[0] * TILE_SIZE
                self.moneyrect.y = pos[1] * TILE_SIZE
                self.DISPLAY.blit(self.money, self.moneyrect)
                #self.drawFood(pos[0] * TILE_SIZE, pos[1] * TILE_SIZE)

            if not train_:
                score = self.FONT.render('Score AI: ' + str(self.Player1.SCORE), True, COLORS["white"])
                self.DISPLAY.blit(score, (10, 5))

                score2 = self.FONT.render('Score 2: ' + str(self.Player2.SCORE), True, COLORS["white"])
                self.DISPLAY.blit(score2, (WIDTH - 150, 5))

                # global max_score, generation
                # maxScore = self.FONT.render('Max score: ' + str(max_score), True, COLORS["text"])
                # self.DISPLAY.blit(maxScore, (10, 30))

                # epoch = self.FONT.render('Generation: ' + str(generation), True, COLORS["text"])
                # self.DISPLAY.blit(epoch, (10, 55))

            pg.display.update()

    def drawFood(self, x,y):
        pg.draw.rect(self.DISPLAY,COLORS['red'],(x,y,TILE_SIZE,TILE_SIZE))

    def createFood(self):
        if len(self.FOOD) == 0:
            newPos = self.Player1.POSITIONS[0]
            while newPos in self.Player1.POSITIONS or newPos in self.Player2.POSITIONS:
                newPos = (random.randint(1,(WIDTH//TILE_SIZE) -1),random.randint(1,(HEIGHT//TILE_SIZE) -1))
            
            self.FOOD.append(newPos)

    def getScore(self):
        return self.Player1.SCORE

    def go(self):
        AI_score_txt = self.Player1.SCORE
        score_txt = self.Player2.SCORE
        self.restart_bool = False

        while not self.restart_bool:
            events = pg.event.get()
            for event in events:
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.restart_bool = True
                        self.restart()

            self.DISPLAY.fill(COLORS['swiss'])
            AI_score = self.FONT.render('Score of the AI: ' + str(AI_score_txt), True, COLORS["black"])
            score = self.FONT.render('Your score: ' + str(score_txt), True, COLORS["black"])
            start = self.FONT.render('Enter your username and hit RETURN', True, COLORS["black"])
            self.DISPLAY.blit(score, (WIDTH/2 - 75, 5))
            self.DISPLAY.blit(AI_score, (WIDTH/2 - 100, 30))
            self.DISPLAY.blit(start, (WIDTH/2 - 200, 60))

            self.DISPLAY.blit(textinput.get_surface(), (25, 100))
            if textinput.update(events):
                self.enterRanking(textinput.get_text(), score)

            lines = self.FONT.render("-------------------", True, COLORS["black"])
            self.DISPLAY.blit(lines, (25, 120))

            lines = self.FONT.render("RANKING", True, COLORS["white"])
            self.DISPLAY.blit(lines, (WIDTH/2-30, 160))

            names = ["bernatixer", "dasix", "lacasa"]
            for i in range(0,len(names)):
                lines = self.FONT.render(" -> " + names[i], True, COLORS["white"])
                self.DISPLAY.blit(lines, (WIDTH/2-30, 180+25*i))
            
            pg.display.update()

    def enterRanking(self, name, score):
        data = {
            'name': name,
            'score': score
        }
        r = requests.post(url=API_ENDPOINT, data=data)
        print(r)

    def restart(self):
        global max_score
        if self.Player1.SCORE > max_score:
            max_score = self.Player1.SCORE
        global generation
        generation += 1

        self.Player1 = Snake(color = COLORS["white"], up = pg.K_UP, down = pg.K_DOWN, right = pg.K_RIGHT, left = K_LEFT, display = self.DISPLAY, game_over = None)

        self.Player2 = Snake(color = COLORS["snake"], up = pg.K_w, down = pg.K_s, right = pg.K_d, left = K_a, display = self.DISPLAY, game_over = self.go)


if __name__== "__main__":
    GAME = Game()
