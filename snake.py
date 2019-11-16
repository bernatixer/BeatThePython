import sys
import pygame as pg
from pygame.locals import *
import time
import random
from settings import *
import math

class Snake:
    def __init__(self, up, down, right, left, color, display, game_over):
        self.up = up
        self.down = down
        self.right = right
        self.left = left
        self.color = color
        self.CURR_PresedKey = self.down
        self.gameOver = False
        self.POSITIONS = [(4,0),(4,1),(4,2),(4,3),(4,4),(4,5)]
        self.SCORE = 0
        self.DISPLAY = display
        self.ALLOWED_KEYS = [up,down,left,right]
        self.GAME_OVER = game_over
    
    def drawSnake(self,x,y):
        pg.draw.rect(self.DISPLAY,self.color,(x,y,TILE_SIZE,TILE_SIZE))

    def act(self, action):
        print("Action:", action)
        if action == 0:
            self.moveUp()
        elif action == 1:
            self.moveDown()
        elif action == 2:
            self.moveLeft()
        elif action == 3:
            self.moveRight()

    def moveLeft(self):
        self.CURR_PresedKey = self.left

    def moveRight(self):
        self.CURR_PresedKey = self.right

    def moveUp(self):
        self.CURR_PresedKey = self.up

    def moveDown(self):
        self.CURR_PresedKey = self.down

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
            # if newPos[0] < 0 or newPos[1] < 0 or newPos[0] >= WIDTH // TILE_SIZE or newPos[1] >= HEIGHT // TILE_SIZE or newPos in self.POSITIONS:
            #     print("Final Score:", self.SCORE)
            #     self.gameOver = True
            #     self.GAME_OVER()
            if len(self.POSITIONS) > self.SCORE + 5:
                del self.POSITIONS[0]            
            self.POSITIONS.append(newPos)

    def update(self, FOOD):
        if not self.gameOver:
            for pos in self.POSITIONS:
                self.drawSnake(pos[0] * TILE_SIZE, pos[1] * TILE_SIZE)
            if self.POSITIONS[-1] in FOOD:
                del FOOD[FOOD.index(self.POSITIONS[-1])]
                self.SCORE += 1
    
    def newEvent(self,event):
        if event.key in self.ALLOWED_KEYS:
            a = self.CURR_PresedKey == self.right and event.key == self.left
            b = self.CURR_PresedKey == self.left and event.key == self.right
            c = self.CURR_PresedKey == self.up and event.key == self.down
            d = self.CURR_PresedKey == self.down and event.key == self.up
            
            if not a and not b and not c and not d:
                self.CURR_PresedKey = event.key
    
    def calculateScore(self, FOOD, action):
        distA = self.calculateDistance(self.POSITIONS[-1], FOOD[0], action = action)
        distB = self.calculateDistance(self.POSITIONS[-1], FOOD[0])

        print("Distancia: ", distA, " Distancia: ",distB)
        if distA < distB:
            return 1
        else:
            return -1

    def calculateDistance(self, head, food, action = None):
        if action or action == 0:
            if action == 2:
                (a,b) = (head[0] - 1, head[1])
            if action == 3:
                (a,b) = (head[0] + 1, head[1])
            if action == 0:
                (a,b) = (head[0], head[1] - 1)
            if action == 1:
                (a,b) = (head[0], head[1] + 1)
        else:
            (a,b) = head

        (c,d) = food
        return math.sqrt((a-c)**2 + (b-d)**2)
            
