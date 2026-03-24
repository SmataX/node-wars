import math

class Vector:
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    @staticmethod
    def distance(v1: "Vector", v2: "Vector") -> int:
        return math.floor(math.sqrt(math.pow(v2.x - v1.x, 2)+math.pow(v2.y - v1.y, 2)))