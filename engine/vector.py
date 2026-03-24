import math

class Vector:
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    @staticmethod
    def distance(v1: "Vector", v2: "Vector") -> int:
        return math.floor(math.hypot(v2.x - v1.x, v2.y - v1.y))