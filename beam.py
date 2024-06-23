# enemy_beam.py
import pygame
import math
from base_object import BaseObject
from constants import ENEMY_BEAM_WIDTH, ENEMY_BEAM_HEIGHT,ENEMY_BEAM_IMAGE,ENEMY_BEAM_SPEED
from constants import PLAYER_BEAM_WIDTH, PLAYER_BEAM_HEIGHT,PLAYER_BEAM_IMAGE,PLAYER_BEAM_SPEED,BEAM_FIRE_SOUND

class EnemyBeam(BaseObject):
    def __init__(self, x, y):
            super().__init__(x, y, ENEMY_BEAM_IMAGE, ENEMY_BEAM_WIDTH, ENEMY_BEAM_HEIGHT, ENEMY_BEAM_SPEED, 0)


class RotateEnemyBeam(BaseObject):
    def __init__(self, x, y, angle):
            radians = math.radians(angle)
            image = pygame.image.load(ENEMY_BEAM_IMAGE).convert_alpha()
            image = pygame.transform.scale(image, (ENEMY_BEAM_WIDTH, ENEMY_BEAM_HEIGHT))
            image = pygame.transform.rotate(image, -math.degrees(radians))
            speed_x = math.cos(radians) * ENEMY_BEAM_SPEED  # - math.sin(radians) * 0
            speed_y = math.sin(radians) * ENEMY_BEAM_SPEED  # + math.cos(radians) * 0
            
            super().__init__(x, y, image, speed_x=speed_x, speed_y=speed_y)

class PlayerBeam(BaseObject):

    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_BEAM_IMAGE, PLAYER_BEAM_WIDTH, PLAYER_BEAM_HEIGHT, PLAYER_BEAM_SPEED, 0,sound_path=BEAM_FIRE_SOUND)