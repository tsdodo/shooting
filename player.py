# player.py

import pygame
from base_object import BaseObject
from beam import PlayerBeam
from explosion import PlayerExplosion
from constants import PLAYER_IMAGE, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SPEED, \
    INITIAL_LIVES, INITIAL_SCORE,INITIAL_PLAYER_X, INITIAL_PLAYER_Y,SCREEN_WIDTH,SCREEN_HEIGHT,SCORE_PER_HIT
from utils import debug_log

class Player(BaseObject):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_IMAGE, PLAYER_WIDTH, PLAYER_HEIGHT ,lives=INITIAL_LIVES)

        self.score = INITIAL_SCORE

    def key_handler(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.x > 0:
            self.move(-PLAYER_SPEED, 0)
        if keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - PLAYER_WIDTH:
            self.move(PLAYER_SPEED, 0)
        if keys[pygame.K_UP] and self.y > 0:
            self.move(0, -PLAYER_SPEED)
        if keys[pygame.K_DOWN] and self.y < SCREEN_HEIGHT - PLAYER_HEIGHT:
            self.move(0, PLAYER_SPEED)
        if keys[pygame.K_SPACE]:
            return self.shooting()    

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def shooting(self):
        beams = [(PlayerBeam(self.x + PLAYER_WIDTH, self.y + PLAYER_HEIGHT // 2))]
        debug_log("Player fired a beam")
        return beams
    
    def explosion(self):
        self.reduce_life()  
        self.hit = True
        return PlayerExplosion(self.x, self.y)

    def reset(self, init = False):
        self.hit = False
        self.x = INITIAL_PLAYER_X
        self.y = INITIAL_PLAYER_Y
        if init:
            self.lives = INITIAL_LIVES
            self.score = INITIAL_SCORE

    def score_up(self):
        self.score += SCORE_PER_HIT    
