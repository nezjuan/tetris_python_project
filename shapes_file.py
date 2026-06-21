from copy import deepcopy
from random import choice, randrange
from mixins_file import Drawable, Movable, Rotatable, Collidable
import pygame

class Block:
    __slots__ = ("_x","_y")

    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value):
        self._y = value

    def __repr__(self):
        return f"Block({self._x}, {self._y})"
    
class Figure(Drawable, Movable, Rotatable, Collidable):
    SHAPE = []

    def __init__(self, tile_size, spawn=(0,0), color= None):
        if not self.SHAPE:
            raise NotImplementedError(f"{self.__class__.__name__}must define a non-empty SHAPE")
        self._tile = tile_size
        sx, sy = spawn
        self._blocks = [Block(x + sx, y + sy) for x, y in self.SHAPE]
        self._color = color or self._random_color()

    @staticmethod
    def _random_color():
        return (randrange(30, 256), randrange(30, 256), randrange(30, 256))
    
    @property
    def color(self):
        return self._color
    
    @property
    def blocks(self):
        return self._blocks
    
    def move (self, dx, dy):
        for block in self._blocks:
            block.x += dx
            block.y += dy

    def rotate(self):
        center = self._blocks[0]
        for block in self._blocks:
            x = block.y - center.y
            y = block.x - center.x
            block.x = center.x - x
            block.y = center.y + y

    def collides(self, field):
        for block in self._blocks:
            if block.x < 0 or block.x > field.width - 1:
                return True
            if block.y > field.height -1:
                return True
            if block.y >= 0 and field.cell(block.x, block.y):
                return True
        return False
    
    def draw(self, surface, offset =(0, 0)):
        for block in self.blocks:
            rect = pygame.Rect(block.x * self._tile + offset[0],
                block.y * self._tile + offset[1],
                self._tile -2,
                self._tile -2)
            pygame.draw.rect(surface, self._color,rect)

    def clone(self):
        return deepcopy(self)

    def __repr__(self):
        return f"{self.__class__.__name__}{self.blocks}"
    
class LineFigure(Figure):
    SHAPE = [(-1, 0), (0, 0), (1, 0), (2, 0)]

class BoxFigure(Figure):
    SHAPE = [(0, 0), (1, 0), (0, -1), (1, -1)]
    def rotate(self):
        pass

class TFigure(Figure):
    SHAPE = [(-1, 0), (0, 0), (1, 0), (0, -1)]

class SFigure(Figure):
    SHAPE = [(0, 0), (-1, 0), (0, -1), (1, -1)]

class ZFigure(Figure):
    SHAPE = [(0, 0), (1, 0), (0, -1), (-1, -1)]

class LFigure(Figure):
    SHAPE = [(0, -1), (0, 0), (0, 1), (1, 1)]

class JFigure(Figure):
    SHAPE = [(0, -1), (0, 0), (0, 1), (-1, 1)]

FIGURE_CLASSES = [LineFigure, BoxFigure, TFigure, SFigure, ZFigure, LFigure, JFigure]
def random_figure(tile_size, spawn=(0,0)):
    return choice(FIGURE_CLASSES)(tile_size, spawn=spawn)