from abc import ABC, abstractmethod

class UserInterfaceElement(ABC):
    def __init__(self, font, color):
        self._font = font
        self._color = color

    @abstractmethod
    def text(self):
        raise NotImplementedError
    
    def draw(self, surface, pos):
        rendered = self._font.render(self.text(), True, self._color)
        surface.blit(rendered, pos)

class StaticLabel(UserInterfaceElement):
    def __init__(self,font, color, value):
        super().__init__(font, color)
        self._value = value

    def text(self):
        return self._value
    
class ScoreLabel(UserInterfaceElement):
    def __init__(self, font, color, score_obj, prefix= "score: "):
        super().__init__(font,color)
        self._score_obj = score_obj
        self._prefix = prefix
    
    def text(self):
        return f"{self._prefix}{self._score_obj.score}"
    
class RecordLabel(UserInterfaceElement):
    def __init__(self, font, color, value_getter, prefix = "record:" ):
        super().__init__(font, color)
        self._value_getter = value_getter
        self._prefix = prefix

    def text(self):
        return f"{self._prefix}{self._value_getter()}"