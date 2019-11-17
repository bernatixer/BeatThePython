# GAME
TILE_SIZE = 32

SIZE = WIDTH, HEIGHT = 480, 480

COLORS = {
    "black": (0,0,0),
    "white": (255,255,255),
    "red": (244,67,54),
    "text": (76,175,80),
    "snake": (255,193,7),
    "swiss": (250,91,53),
}

# TRAIN
storage = {}
radius = 10
score = 0
missed = 0
reward = 0

LR = 0.2
Y = 0.8