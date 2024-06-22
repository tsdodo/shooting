# enemy.py

from base_object import BaseObject
from constants import  ENEMY_IMAGE, ENEMY_WIDTH, ENEMY_HEIGHT, ENEMY_SPEED

class Enemy(BaseObject):
    def __init__(self, x, y, is_shooter=False):
        super().__init__(x, y, ENEMY_IMAGE, ENEMY_WIDTH, ENEMY_HEIGHT, ENEMY_SPEED)
        self.is_shooter = is_shooter
        self.shoot_cooldown = 0
        self.radial_shoot_cooldown = 0

    def update_cooldowns(self):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.radial_shoot_cooldown > 0:
            self.radial_shoot_cooldown -= 1
