# enemy_beam.py

from base_object import BaseObject
from constants import PLAYER_BEAM_WIDTH, PLAYER_BEAM_HEIGHT,PLAYER_BEAM_IMAGE,PLAYER_BEAM_SPEED

class PlayerBeam(BaseObject):
    def __init__(self, x, y):
            super().__init__(x, y, PLAYER_BEAM_IMAGE, PLAYER_BEAM_WIDTH, PLAYER_BEAM_HEIGHT, PLAYER_BEAM_SPEED, 0)
