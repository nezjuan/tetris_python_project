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