import os
import sys
from abc import ABC, abstractmethod
 
import pygame
 
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

        self._anim_count = 0
        self._anim_speed = 5
        self._anim_limit = 500
        self._dx = 0
        self._do_rotate = False
        self._soft_drop = False

        self._home_bg = self._load_background("bg_stars.png", (18, 18, 28))
        self._game_bg = self._load_background("bg_melanch.jpeg", (28, 22, 34), size=self._game_res)


        self._main_font = pygame.font.Font('slkscre.ttf', 70)
        self._font = pygame.font.Font('slkscre.ttf', 45)

        self._labels = [(StaticLabel(self._main_font, (255, 140, 0), "TETRIS"), (470, 10)),
            (ScoreLabel(self._font, (60, 200, 80), self._score), (480, 840)),
            (RecordLabel(self._font, (212, 175, 55), self._record.get), (480, 710)),]

        self.log("initialised")

    def _load_background(self, filename, fallback_color, size=None):
        base_dir = os.path.dirname(__file__)
        candidates = [os.path.join(base_dir, filename),
            os.path.join(base_dir, "assets", filename)]
        size = size or self.WINDOW_SIZE
        for path in candidates:
            try:
                image = pygame.image.load(path).convert()
                return pygame.transform.smoothscale(image, size)
            except (pygame.error, FileNotFoundError):
                continue
        surf = pygame.Surface(size)
        surf.fill(fallback_color)
        return surf
        
    def _new_round(self):
        self._field.reset()
        self._score.reset()
        self._anim_count = 0
        self._anim_speed = 5
        self._anim_limit = 500

    def _spawn_next_figure(self):
        self._figure, self._next_figure = (self._next_figure,
            random_figure(self.TILE, spawn=self._spawn))
        self._anim_limit = 500

    def update(self):
        if self._dx:
            previous = self._figure.clone()
            self._figure.move(self._dx, 0)
            if self._figure.collides(self._field):
                self._figure = previous
            self._dx = 0

        if self._do_rotate:
            previous = self._figure.clone()
            self._figure.rotate()
            if self._figure.collides(self._field):
                self._figure = previous
            self._do_rotate = False

        effective_speed = self._anim_speed * (20 if self._soft_drop else 1)
        self._anim_count += effective_speed
        if self._anim_count > self._anim_limit:
            self._anim_count = 0
            previous = self._figure.clone()
            self._figure.move(0, 1)
            if self._figure.collides(self._field):
                self._figure = previous
                self._field.freeze(self._figure)
                self._spawn_next_figure()

        cleared = self._field.clear_lines()
        if cleared:
            self._score.add_lines(cleared)
            self._anim_speed += 0.3
            self.log(f"cleared {cleared} line(s), score={self._score.score}")

        if self._field.top_row_occupied():
            new_record = self._record.update(self._score.score)
            self.log(f"game over, record={new_record}")
            self._new_round()

    def render(self):
        self._screen.blit(self._home_bg, (0, 0))
        self._game_surface.blit(self._game_bg, (0, 0))

        for x in range(self.WIDTH):
            for y in range(self.HEIGHT):
                rect = pygame.Rect(x * self.TILE, y * self.TILE, self.TILE, self.TILE)
                pygame.draw.rect(self._game_surface, (70, 70, 80), rect, 1)

        for y, row in enumerate(self._field):
            for x, color in enumerate(row):
                if color:
                    rect = pygame.Rect(x * self.TILE, y * self.TILE, self.TILE - 2, self.TILE - 2)
                    pygame.draw.rect(self._game_surface, color, rect)

        self._figure.draw(self._game_surface)
        self._screen.blit(self._game_surface, (20, 20))
        self._next_figure.draw(self._screen, offset=(380, 185))

        for label, pos in self._labels:
            label.draw(self._screen, pos)

        pygame.display.flip()

    def run(self):
        while True:
            self._handle_events()
            self.update()
            self.render()
            self._clock.tick(self.FPS)

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self._dx = -1
                elif event.key == pygame.K_RIGHT:
                    self._dx = 1
                elif event.key == pygame.K_DOWN:
                    self._soft_drop = True
                elif event.key == pygame.K_UP:
                    self._do_rotate = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self._soft_drop = False