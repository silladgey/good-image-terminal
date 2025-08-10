from dataclasses import dataclass


@dataclass
class Color:
    r: int
    g: int
    b: int
    a: int = 255

    @property
    def rgb(self):
        return self.r, self.g, self.b

    @property
    def rgba(self):
        return self.r, self.g, self.b, self.a

