from __future__ import annotations
from abc import ABC, abstractmethod
from typing import override

import pygame as pg
from pygame import Color

from vector import Vec2
from touchpad import Touchpad
from line_cleaner import cleanup_line

class Brush(ABC):
    def __init__(self, width : int | float):
        if not isinstance(width, (int, float)): raise TypeError("width must be an int")
        super().__init__()
        self.__width = width

    @property
    def width(self) -> int | float:
        return self.__width

    @width.setter
    def width(self, value : int | float):
        if not isinstance(value, (int, float)): raise TypeError("width must be an int")
        self.__width = min(max(value, 1), 200)

    @abstractmethod
    def apply(self, canvas : pg.Surface, points : list[Vec2]):
        pass

    @abstractmethod
    def display(self, win : pg.Surface, last_point : Vec2, zoom : float):
        pass

class PaintBrush(Brush):
    def __init__(self, color : Color = Color(255, 255, 255), width : int | float = 5):
        if not isinstance(color, Color): raise TypeError("color must be a Color")
        self.__color : Color = color
        super().__init__(width)

    @property
    def color(self) -> Color:
        return self.__color

    @override
    def apply(self, canvas : pg.Surface, points : list[Vec2]):
        tp : Touchpad = Touchpad()
        points = cleanup_line(points)
        if self.width <= 5 and len(points) >= 2:
            pg.draw.lines(canvas, self.color, False, [p.tuple for p in points], int(self.width))
        elif self.width > 5 and points:
            last_point : Vec2 = points[0]
            for p in points:
                pg.draw.circle(canvas, self.color, p.tuple, self.width // 2)
                dist : int | float = Vec2.distance(last_point, p)
                if dist > self.width / 3:
                    sub_divs : int = dist / (self.width / 3)
                    step : Vec2 = (last_point - p).normalized() * (dist / sub_divs)
                    ps : Vec2 = p + step
                    for i in range(int(sub_divs)):
                        pg.draw.circle(canvas, self.color, ps.tuple, self.width // 2)
                        ps += step
                last_point = p

    @override
    def display(self, win : pg.Surface, last_point : Vec2, zoom : float):
        pg.draw.circle(win, Color(0, 255, 0), last_point.tuple, max((self.width * zoom) // 2, 1), width=2)

class Eraser(PaintBrush):
    def __init__(self, width : int | float = 10):
        super().__init__(Color(0,0,0), width)

    @override
    def display(self, win : pg.Surface, last_point : Vec2, zoom : float):
        pg.draw.circle(win, Color(255, 0, 0), last_point.tuple, max((self.width * zoom) // 2, 1), width=2)
