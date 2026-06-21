from abc import ABC, abstractmethod

class Drawable(ABC):
    @abstractmethod
    def draw(self, surface, *args, **kwargs):
        raise NotImplementedError
    
class Movable(ABC):
    @abstractmethod
    def move(self, dx, dy):
        raise NotImplementedError
    
class Rotatable(ABC):
    @abstractmethod
    def rotate(self):
        raise NotImplementedError

class Collidable(ABC):
    @abstractmethod
    def collides(self, field):
        raise NotImplementedError

class Loggable:
    def log(self, message):
        print(f"[{self.__class__.__name__}] {message}")