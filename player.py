# player.py

from base_object import BaseObject
from constants import PLAYER_IMAGE, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SPEED, INITIAL_LIVES, INITIAL_SCORE,INITIAL_PLAYER_X, INITIAL_PLAYER_Y
from utils import debug_log

class Player(BaseObject):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_IMAGE, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.lives = INITIAL_LIVES
        self.score = INITIAL_SCORE

    def move_up(self):
        self.move(0, -PLAYER_SPEED)
        debug_log("Player moved up")

    def move_down(self):
        self.move(0, PLAYER_SPEED)
        debug_log("Player moved dowm")

    def move_right(self):
        self.move(PLAYER_SPEED, 0)
        debug_log("Player moved right")

    def move_left(self):
        self.move(-PLAYER_SPEED, 0)
        debug_log("Player moved left")

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def reset(self, init = False):
        self.hit = False
        self.x = INITIAL_PLAYER_X
        self.y = INITIAL_PLAYER_Y
        if init:
            self.lives = INITIAL_LIVES
            self.score = INITIAL_SCORE

            
