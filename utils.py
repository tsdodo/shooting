# utils.py
from constants import DEBUG_MODE

def debug_log(message):
    if DEBUG_MODE:
        print(message)

def check_collision(obj1, obj2):

    """マスクを使用して衝突判定を行う関数"""
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None
