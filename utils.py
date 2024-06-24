# utils.py
import math
import pygame
from typing import Optional
from constants import DEBUG_MODE


def debug_log(message):
    if DEBUG_MODE:
        print(message)


def check_collision(obj1, obj2):
    """マスクを使用して衝突判定を行う関数"""
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None


def rotate_image(
    image: str | pygame.Surface,
    angle: int,
    width: Optional[int] = None,
    height: Optional[int] = None,
    speed_x: Optional[int] = None,
    speed_y: Optional[int] = None,
) -> tuple[pygame.Surface,int,int]:
    if isinstance(image, str):
        image = pygame.image.load(image).convert_alpha()
        if width and height:
            image = pygame.transform.scale(image, (width, height))

    radians = math.radians(angle)
    rotate_image = pygame.transform.rotate(image, -math.degrees(radians))

    rotate_speed_x = 0
    rotate_speed_y = 0
    if speed_x:
        rotate_speed_x += int(math.cos(radians) * speed_x)
        rotate_speed_y += int(math.sin(radians) * speed_x)
    if speed_y:
        rotate_speed_x -= int(math.sin(radians) * speed_y)
        rotate_speed_y += int(math.cos(radians) * speed_y)

    return (rotate_image, rotate_speed_x, rotate_speed_y)