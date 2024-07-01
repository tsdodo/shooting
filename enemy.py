import random
from typing import Optional

from base_object import BaseObject
from beam import EnemyBeam, RotateEnemyBeam
from constants import (ENEMY_BEAM_ANGLE_UNIT, ENEMY_HEIGHT, ENEMY_IMAGE,
                       ENEMY_SPEED, ENEMY_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH,
                       SHOOTER_ENEMY_IMAGE, SHOOTER_PROB_PER_ENEMY_RECIP)
from explosion import EnemyExplosion
from utils import debug_log


class Enemy(BaseObject):
    def __init__(self) -> None:
        self.x = SCREEN_WIDTH
        self.y = random.randint(0, SCREEN_HEIGHT - ENEMY_HEIGHT)
        self.shoot_cooldown = 0
        self.radial_shoot_cooldown = 0
        # ランダムに放射状ビームを撃つ敵を追加
        self.is_shooter = (
            random.randint(1, SHOOTER_PROB_PER_ENEMY_RECIP) == 1
        )
        image = SHOOTER_ENEMY_IMAGE if self.is_shooter else ENEMY_IMAGE
        super().__init__(
            self.x, self.y, image, ENEMY_WIDTH, ENEMY_HEIGHT, ENEMY_SPEED
        )

        debug_log(f"New enemy added at ({self.x}, {self.y})")

    def update_cooldowns(self) -> None:
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.radial_shoot_cooldown > 0:
            self.radial_shoot_cooldown -= 1

    def move(self, dx: Optional[int]=None, dy: Optional[int]=None) -> None:
        super().move(dx, dy)
        self.update_cooldowns()

    def shooting(self) -> Optional[list[EnemyBeam | RotateEnemyBeam]]:
        beams: list[EnemyBeam | RotateEnemyBeam] = []
        if self.is_shooter and self.radial_shoot_cooldown <= 0:
            # ENEMY_BEAM_ANGLE_UNIT度ごとにビームを放射
            for angle in range(0, 360, ENEMY_BEAM_ANGLE_UNIT):
                beams.append(RotateEnemyBeam(self.x, self.y + ENEMY_HEIGHT // 2, angle))
            self.radial_shoot_cooldown = random.randint(200, 400)
            return beams
        if self.shoot_cooldown <= 0:
            beams.append(EnemyBeam(self.x, self.y + ENEMY_HEIGHT // 2))
            self.shoot_cooldown = random.randint(50, 100)
            return beams
        return None

    def explosion(self) -> EnemyExplosion:
        return EnemyExplosion(self.x, self.y)