from abc import ABC, abstractmethod

class UserInterfaceElement(ABC):
    def __init__(self, font, color):
        self._font = font
        self._color = color

    @abstractmethod
    def text(self):
        raise NotImplementedError
    
    def draw(self, surface, pos, min_x=0):
        surf_w, surf_h = surface.get_size()
        text = self.text()
        char_surfaces = [self._font.render(ch, True, self._color) for ch in text]

        text_w = sum(s.get_width() for s in char_surfaces)
        text_h = max((s.get_height() for s in char_surfaces), default=0)

        x = max(min(pos[0], surf_w - text_w - 10), min_x)
        y = max(min(pos[1], surf_h - text_h - 10), 0)

        cursor_x = x
        for s in char_surfaces:
            surface.blit(s, (cursor_x, y))
            cursor_x += s.get_width()

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