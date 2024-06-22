# base_object.py

import pygame
import math

class BaseObject:
    def __init__(self, x, y, image_path, width=None, height=None, speed_x=0, speed_y=0, rotate=False, angle=0):
        self.x = x
        self.y = y

        image = pygame.image.load(image_path).convert_alpha()
        if width and height:
            image = pygame.transform.scale(image, (width, height))

        if rotate:
            radians = math.radians(angle)
            image = pygame.transform.rotate(image, -math.degrees(radians))
            self.speed_x = math.cos(radians) * speed_x - math.sin(radians) * speed_y
            self.speed_y = math.sin(radians) * speed_x + math.cos(radians) * speed_y
        else:
            self.speed_x = speed_x
            self.speed_y = speed_y

        self.image = image       
        self.mask = pygame.mask.from_surface(image)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))