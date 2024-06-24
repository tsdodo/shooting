from typing import Optional
import pygame
from base_object import BaseObject
from beam import PlayerBeam, RotatePlayerBeam
from explosion import PlayerExplosion
from constants import (
    PLAYER_BEAM_ANGLE_UNIT,
    PLAYER_IMAGE,
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    PLAYER_SPEED,
    INITIAL_LIVES,
    INITIAL_SCORE,
    INITIAL_PLAYER_X,
    INITIAL_PLAYER_Y,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SCORE_PER_HIT,
)


class Player(BaseObject):
    def __init__(self) -> None:
        super().__init__(
            INITIAL_PLAYER_X,
            INITIAL_PLAYER_Y,
            PLAYER_IMAGE,
            PLAYER_WIDTH,
            PLAYER_HEIGHT,
            lives=INITIAL_LIVES,
        )

        self.score = INITIAL_SCORE
        self.shooting_gage = 0

    def key_handler(self) -> Optional[list[PlayerBeam|RotatePlayerBeam]]:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.x > 0:
            self.move(-PLAYER_SPEED, 0)
        if keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - PLAYER_WIDTH:
            self.move(PLAYER_SPEED, 0)
        if keys[pygame.K_UP] and self.y > 0:
            self.move(0, -PLAYER_SPEED)
        if keys[pygame.K_DOWN] and self.y < SCREEN_HEIGHT - PLAYER_HEIGHT:
            self.move(0, PLAYER_SPEED)
        if keys[pygame.K_SPACE]:
            return self.shooting()
        return None

    def shooting(self) -> Optional[list[PlayerBeam | RotatePlayerBeam]]:
        beams: list[PlayerBeam | RotatePlayerBeam] = []
        if self.shooting_gage >= 500:
            for angle in range(0, 360, PLAYER_BEAM_ANGLE_UNIT):
                beams.append(RotatePlayerBeam(self.x, self.y + PLAYER_HEIGHT // 2, angle))
            if self.shooting_gage >= 600:
                self.reset_shooting_gage()  
        else:
            beams.append(PlayerBeam(self.x + PLAYER_WIDTH, self.y + PLAYER_HEIGHT // 2))
        return beams

    def explosion(self) -> PlayerExplosion:
        self.reduce_life()
        self.hit = True
        return PlayerExplosion(self.x, self.y)

    def reset(self, init=False) -> None:
        self.hit = False
        self.x = INITIAL_PLAYER_X
        self.y = INITIAL_PLAYER_Y
        if init:
            self.lives = INITIAL_LIVES
            self.score = INITIAL_SCORE
        self.shooting_gage = 0

    def score_up(self) -> None:
        self.score += SCORE_PER_HIT

    def shooting_gage_up(self) -> None:
        self.shooting_gage +=1
    
    def reset_shooting_gage(self) -> None:
        self.shooting_gage = 0
