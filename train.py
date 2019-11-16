from settings import *
import numpy as np
import game
import json

train = False

if not train:
    with open('storage.json', 'r') as fp:
        storage = json.load(fp)

    Q = np.loadtxt("Q.txt", dtype=float)
else:
    storage = {}
    Q = np.zeros([50000, 4])

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
    global LR
    global reward
    global missed
    s = State(player.POSITIONS[-1],food)
    act = action(s)
    r0 = player.calculateScore(food, act)

    if r0 > 0:
        reward += r0
    else:
        missed += r0 
    s1 = afteraction(s, act)
    Q[convert(s), act] = Q[convert(s), act] + LR*(r0 + Y * np.max(Q[convert(s1), :]) - Q[convert(s), act])
    
    return act
