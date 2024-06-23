# base_object.py

import pygame
import math
from constants import  SCREEN_WIDTH,SCREEN_HEIGHT

class BaseObject:
    def __init__(self, x, y, image, width=None, height=None, \
                 speed_x=0, speed_y=0, sound_path=None, lives=None):
        self.x = x
        self.y = y

        if isinstance(image, str):       
            image = pygame.image.load(image).convert_alpha()
            if width and height:
                image = pygame.transform.scale(image, (width, height))
            
        self.image = image       
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.mask = pygame.mask.from_surface(image)
        self.lives = lives

        if sound_path is not None:
            pygame.mixer.Sound(sound_path).play()

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def off_screen(self):
        return self.x < 0 or self.x > SCREEN_WIDTH  \
                or self.y < 0 or self.y > SCREEN_HEIGHT
    
    def reduce_life(self, reduce_count=1):
        if self.lives is not None:
            self.lives -= reduce_count

    def dead(self):
        return self.lives == 0
