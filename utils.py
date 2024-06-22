# utils.py

import pygame
from constants import DEBUG_MODE

def debug_log(message):
    if DEBUG_MODE:
        print(message)

def check_collision(mask1, x1, y1, mask2, x2, y2):
    """マスクを使用して衝突判定を行う関数"""
    offset_x = x2 - x1
    offset_y = y2 - y1
    return mask1.overlap(mask2, (offset_x, offset_y)) is not None
