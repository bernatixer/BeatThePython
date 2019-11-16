from settings import *
import numpy as np
import game

storage = {}
Q = np.zeros([25000, 4])

class State:
    def __init__(self,direction,fooddirection):
        self.direction = direction
        self.fooddirection = fooddirection

    def getStringState(self):
        return str(self.direction)+str(self.fooddirection)

def convert(s):
    n = s.getStringState()
    if n in storage:
        return storage[n]
    else:
        if len(storage):
            maximum = max(storage, key=storage.get) 
            storage[n] = storage[maximum] + 1
        else:
            storage[n] = 1
    return storage[n]

def action(s):
    return np.argmax(Q[convert(s), :])

def afteraction(game, action):
    pass

def chooseAction(player,food):
    direction = player.getSnakeDirection()
    fooddirection = player.getFoodDirection(food)
    s = State(direction,fooddirection)
    act = action(s)
    r0 = player.calculateScore()
    s1 = afteraction(s, act)
    Q[convert(s), act] += LR*(r0 + Y * np.max(Q[convert(s1), :]) - Q[convert(s), act])
    
    return act

if __name__== "__main__":
    game = Game(gameOver)
