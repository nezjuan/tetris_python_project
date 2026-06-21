import os
import sys
import pygame
from abc import ABC, abstractmethod
from field_file import Field
from score_file import Score, Record
from shapes_file import random_figure
from user_interface_file import StaticLabel, ScoreLabel, RecordLabel
from mixins_file import Loggable

class AbstractGame(ABC):
    @abstractmethod
    def update(self):
        raise NotImplementedError
    
    @abstractmethod
    def render(self):
        raise NotImplementedError
    
    @abstractmethod
    def run(self):
        raise NotImplementedError
    
class Tetris(AbstractGame, Loggable):
    WIDTH, HEIGHT = 10, 20
    TILE = 45
    FPS = 60
    WINDOW_SIZE = (750,940)

    def __init__(self):
        pygame.init()
        self._game_res = (self.WIDTH * self.TILE, self.HEIGHT * self.TILE)
        self._screen = pygame.display.set_mode(self.WINDOW_SIZE)
        pygame.display.set_caption("Tetris")
        self._game_surface = pygame.Surface(self._game_res)
        self._clock = pygame.time.Clock()

        self._field = Field(self.WIDTH, self.HEIGHT)
        self._score = Score()
        self._record = Record()

        self._spawn = (self.WIDTH // 2, 1)
        self._figure = random_figure(self.TILE, spawn=self._spawn)
        self._next_figure = random_figure(self.TILE, spawn=self._spawn)

        self._home_bg = self._load_background("bg_stars.png", (18, 18, 28))
        self._game_bg = self._load_background("bg_melanch.jpg", (28, 22, 34), size=self._game_res)

        self._anim_count = 0
        self._anim_speed = 5
        self._anim_limit = 2000
        self._dx = 0
        self._do_rotate = False

        self._main_font = pygame.font.SysFont(None, 70)
        self._font = pygame.font.SysFont(None, 45)

        self._labels = [(StaticLabel(self._main_font, (255, 140, 0), "TETRIS"), (470, 10)),
            (ScoreLabel(self._font, (60, 200, 80), self._score), (550, 840)),
            (RecordLabel(self._font, (212, 175, 55), self._record.get), (550, 710)),]

        self.log("initialised")

    def _load_background(self, filename, fallback_color, size=None):
        path = os.path.join(os.path.dirname(__file__), "assets", filename)
        size = size or self.WINDOW_SIZE
        try:
            image = pygame.image.load(path).convert()
            return pygame.transform.smoothscale(image, size)
        except (pygame.error, FileNotFoundError):
            surf = pygame.Surface(size)
            surf.fill(fallback_color)
            return surf
        
    def _new_round(self):
        self._field.reset()
        self._score.reset()
        self._anim_count = 0
        self._anim_speed = 5
        self._anim_limit = 2000

    def _spawn_next_figure(self):
        self._figure, self._next_figure = (
            self._next_figure,
            random_figure(self.TILE, spawn=self._spawn),
        )
        self._anim_limit = 2000