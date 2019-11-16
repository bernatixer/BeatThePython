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
    print("Actions: ", Q[convert(s), :])
    return np.argmax(Q[convert(s), :])

def afteraction(s, action):
    head = s.head
    if action == 2:
        newHead = (head[0] - 1, head[1])
    if action == 3:
        newHead = (head[0] + 1, head[1])
    if action == 0:
        newHead = (head[0], head[1] - 1)
    if action == 1:
        newHead = (head[0], head[1] + 1)
    return State(newHead, s.food)

def chooseAction(player,food):
    s = State(player.POSITIONS[-1],food)
    act = action(s)
    r0 = player.calculateScore(food, act)
    global SCORE
    SCORE += r0
    print("Score: ", SCORE)
    s1 = afteraction(s, act)
    print("=======")
    print(Q[convert(s), act], "-", r0, "-", np.max(Q[convert(s1), :]))
    print("=======")
    Q[convert(s), act] = Q[convert(s), act] + LR*(r0 + Y * np.max(Q[convert(s1), :]) - Q[convert(s), act])
    
    return act
