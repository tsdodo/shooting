# enemy_beam.py

from base_object import BaseObject
from constants import ENEMY_BEAM_WIDTH, ENEMY_BEAM_HEIGHT,ENEMY_BEAM_IMAGE,ENEMY_BEAM_SPEED

class EnemyBeam(BaseObject):
    def __init__(self, x, y):
            super().__init__(x, y, ENEMY_BEAM_IMAGE, ENEMY_BEAM_WIDTH, ENEMY_BEAM_HEIGHT, ENEMY_BEAM_SPEED, 0)


class RotateEnemyBeam(BaseObject):
    def __init__(self, x, y, angle):
            super().__init__(x, y, ENEMY_BEAM_IMAGE, ENEMY_BEAM_WIDTH, ENEMY_BEAM_HEIGHT, ENEMY_BEAM_SPEED, 0, True, angle)
