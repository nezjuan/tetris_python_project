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
        surf_w, surf_h = surface.get_size()
        text_w, text_h = rendered.get_size()
        x = min(pos[0], surf_w - text_w - 10)
        y = min(pos[1], surf_h - text_h - 10)
        surface.blit(rendered, (max(x, 0), max(y, 0)))

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