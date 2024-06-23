from base_object import BaseObject
from constants import (EXPLOSION_IMAGE,ENEMY_EXPLOSION_SOUND,EXPLOSION_DURATION, \
                       ENEMY_WIDTH, ENEMY_HEIGHT, PLAYER_EXPLOSION_SOUND, PLAYER_WIDTH, PLAYER_HEIGHT)

class EnemyExplosion(BaseObject):
    def __init__(self, x, y):
        super().__init__(x, y, EXPLOSION_IMAGE, ENEMY_WIDTH, ENEMY_HEIGHT, \
                         sound_path=ENEMY_EXPLOSION_SOUND,lives= EXPLOSION_DURATION)


class PlayerExplosion(BaseObject):
    def __init__(self, x, y):
        super().__init__(x, y, EXPLOSION_IMAGE, PLAYER_WIDTH, PLAYER_HEIGHT, \
                         sound_path=PLAYER_EXPLOSION_SOUND,lives= EXPLOSION_DURATION)