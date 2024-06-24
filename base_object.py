from typing import Optional
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class BaseObject():
    
    def __init__(
        self,
        x: int,
        y: int,
        image: str | pygame.Surface,
        width: Optional[int] = None,
        height: Optional[int] = None,
        speed_x: int = 0,
        speed_y: int = 0,
        sound_path: Optional[str] = None,
        lives: int = 0,
    ) -> None:
        self.x = x
        self.y = y

        if isinstance(image, str):
            image = pygame.image.load(image).convert_alpha()
            if width and height:
                image = pygame.transform.scale(image, (width, height))

        self.image = image
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.mask = pygame.mask.from_surface(image)
        self.lives = lives

        if sound_path is not None:
            pygame.mixer.Sound(sound_path).play()

    def move(self, dx: Optional[int]=None, dy: Optional[int]=None) -> None:
        if dx is not None and dy is not None:
            self.x += dx
            self.y += dy
        else:
            self.x += self.speed_x
            self.y += self.speed_y

    def draw(self, screen) -> None:
        screen.blit(self.image, (self.x, self.y))

    def off_screen(self) -> bool:
        return (
            self.x < 0 or self.x > SCREEN_WIDTH or self.y < 0 or self.y > SCREEN_HEIGHT
        )

    def reduce_life(self, reduce_count=1) -> None:
        if self.lives is not None:
            self.lives -= reduce_count

    def dead(self) -> bool:
        return self.lives == 0
