from base_object import BaseObject
from constants import (
    ENEMY_BEAM_WIDTH,
    ENEMY_BEAM_HEIGHT,
    ENEMY_BEAM_IMAGE,
    ENEMY_BEAM_SPEED,
)
from constants import (
    PLAYER_BEAM_WIDTH,
    PLAYER_BEAM_HEIGHT,
    PLAYER_BEAM_IMAGE,
    PLAYER_BEAM_SPEED,
    PLAYER_BEAM_FIRE_SOUND,
)
from utils import rotate_image


class EnemyBeam(BaseObject):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(
            x,
            y,
            ENEMY_BEAM_IMAGE,
            ENEMY_BEAM_WIDTH,
            ENEMY_BEAM_HEIGHT,
            ENEMY_BEAM_SPEED,
            0,
        )


class RotateEnemyBeam(BaseObject):
    def __init__(self, x: int, y: int, angle: int) -> None:
        image, speed_x, speed_y = rotate_image(
            ENEMY_BEAM_IMAGE,
            angle,
            ENEMY_BEAM_WIDTH,
            ENEMY_BEAM_HEIGHT,
            ENEMY_BEAM_SPEED,
        )
        super().__init__(x, y, image, speed_x=speed_x, speed_y=speed_y)


class PlayerBeam(BaseObject):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(
            x,
            y,
            PLAYER_BEAM_IMAGE,
            PLAYER_BEAM_WIDTH,
            PLAYER_BEAM_HEIGHT,
            PLAYER_BEAM_SPEED,
            0,
            sound_path=PLAYER_BEAM_FIRE_SOUND,
        )


class RotatePlayerBeam(BaseObject):
    def __init__(self, x: int, y: int, angle: int) -> None:
        image, speed_x, speed_y = rotate_image(
            PLAYER_BEAM_IMAGE,
            angle,
            PLAYER_BEAM_WIDTH,
            PLAYER_BEAM_HEIGHT,
            PLAYER_BEAM_WIDTH,
        )
        super().__init__(
            x, y, image, speed_x=speed_x, speed_y=speed_y, sound_path=PLAYER_BEAM_FIRE_SOUND
        )
