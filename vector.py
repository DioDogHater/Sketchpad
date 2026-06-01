from __future__ import annotations
import math

class Vec2:
    def __init__(self, x : int | float = 0, y : int | float = 0):
        self.x : int | float = x
        self.y : int | float = y

    @property
    def length2(self) -> int | float:
        return self.x ** 2 + self.y ** 2

    @property
    def length(self) -> int | float:
        return math.sqrt(self.length2)

    @property
    def angle(self) -> int | float:
        return math.atan2(self.y, self.x)

    @property
    def tuple(self) -> tuple:
        return (self.x, self.y)

    def __add__(self, other : Vec2) -> Vec2:
        if not isinstance(other, Vec2):
            raise TypeError("other must be Vec2")
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other : Vec2) -> Vec2:
        if not isinstance(other, Vec2):
            raise TypeError("other must be Vec2")
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, other : Vec2 | int | float) -> Vec2:
        if not isinstance(other, (Vec2, int, float)):
            raise TypeError("other must be a Vec2, int or float")
        if isinstance(other, Vec2):
            return Vec2(self.x * other.x, self.y * other.y)
        else:
            return Vec2(self.x * other, self.y * other)

    def __rmul__(self, other : Vec2 | int | float) -> Vec2:
        return self * other

    def __truediv__(self, other : Vec2 | int | float) -> Vec2:
        if not isinstance(other, (Vec2, int, float)):
            raise TypeError("other must be a Vec2, int or float")
        if isinstance(other, Vec2):
            return Vec2(self.x / other.x, self.y / other.y)
        else:
            return Vec2(self.x / other, self.y / other)

    def __pow__(self, other : int | float) -> Vec2:
        if not isinstance(other, (int, float)):
            raise TypeError("other must be an int or a float")
        return Vec2(self.x ** other, self.y ** other)

    def normalized(self) -> Vec2:
        length : int | float = self.length
        if length == 0:
            return Vec2()
        return self / length

    def dot(self, other : Vec2) -> Vec2:
        if not isinstance(other, Vec2):
            raise TypeError("other must be a Vec2")
        return self.x * other.x + self.y * other.y

    @staticmethod
    def distance2(u : Vec2, v : Vec2) -> Vec2:
        return (u - v).length2

    @staticmethod
    def distance(u : Vec2, v : Vec2) -> Vec2:
        return (u - v).length

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __repr__(self) -> str:
        return str(self)
