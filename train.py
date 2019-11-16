from settings import *
import numpy as np
import game

storage = {}
Q = np.zeros([25000, 4])

SCORE = 0

class State:
    def __init__(self,head,food):
        self.head = head
        self.food = food

    def getStringState(self):
        return str(self.head)+str(self.food)

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

def afteraction(s, action):
    return State(action, s.fooddirection)

def chooseAction(player,food):
    direction = player.getSnakeDirection()
    fooddirection = player.getFoodDirection(food)
    s = State(player.POSITIONS[-1],food)
    act = action(s)
    r0 = player.calculateScore(food, act)
    global SCORE
    SCORE += r0
    print("Score: ", SCORE)
    s1 = afteraction(s, act)
    Q[convert(s), act] += LR*(r0 + Y * np.max(Q[convert(s1), :]) - Q[convert(s), act])
    
    return act
