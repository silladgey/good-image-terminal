from dataclasses import dataclass


@dataclass
class Color:
    """Color class.

    Has various conversion and output methods.
    """
    r: int
    g: int
    b: int
    a: int = 255

    @property
    def rgb(self):
        """Output as RGB tuple."""
        return self.r, self.g, self.b

    @property
    def rgba(self):
        """Output as RGBA tuple."""
        return self.r, self.g, self.b, self.a
