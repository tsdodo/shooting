# enemy.py
import random
from base_object import BaseObject
from beam import EnemyBeam,RotateEnemyBeam
from explosion import EnemyExplosion
from constants import  (ENEMY_IMAGE, ENEMY_WIDTH, ENEMY_HEIGHT, ENEMY_SPEED, \
                        ENEMY_BEAM_ANGLE_UNIT,SCREEN_WIDTH,SCREEN_HEIGHT)
from utils import debug_log

class Enemy(BaseObject):
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.y = random.randint(0, SCREEN_HEIGHT - ENEMY_HEIGHT)
        self.shoot_cooldown = 0
        self.radial_shoot_cooldown = 0
        self.is_shooter = random.randint(1, 5) == 1  # ランダムに放射状ビームを撃つ敵を追加
        super().__init__(self.x, self.y, ENEMY_IMAGE, ENEMY_WIDTH, ENEMY_HEIGHT, ENEMY_SPEED)

        debug_log(f"New enemy added at ({self.x}, {self.y})")

    def update_cooldowns(self):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.radial_shoot_cooldown > 0:
            self.radial_shoot_cooldown -= 1

    def move(self):
        super().move()
        self.update_cooldowns()

    def shooting(self):
        beams = []
        if self.is_shooter and self.radial_shoot_cooldown <= 0:
            for angle in range(0, 360, ENEMY_BEAM_ANGLE_UNIT):  # ENEMY_BEAM_ANGLE_UNIT度ごとにビームを放射
                beams.append(RotateEnemyBeam(self.x, self.y + ENEMY_HEIGHT // 2, angle))
            self.radial_shoot_cooldown = random.randint(200, 400)
            return beams
        if self.shoot_cooldown <= 0:
            beams.append(EnemyBeam(self.x, self.y + ENEMY_HEIGHT // 2))
            self.shoot_cooldown = random.randint(50, 100)
            return beams        

    def explosion(self):
        return EnemyExplosion(self.x, self.y)    
