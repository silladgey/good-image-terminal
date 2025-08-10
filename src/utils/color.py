from dataclasses import dataclass
from math import atan2, degrees, sqrt


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
    def rgb(self) -> tuple[int, int, int]:
        """Output as RGB tuple."""
        return self.r, self.g, self.b

    @property
    def rgba(self) -> tuple[int, int, int, int]:
        """Output as RGBA tuple."""
        return self.r, self.g, self.b, self.a

    @property
    def hex(self) -> str:
        """Output as hexadecimal string."""
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}{self.a:02x}"

    @property
    def hsv(self) -> tuple[int, int, int]:
        """Output as tuple in HSV color space."""
        mx = max(self.r, self.g, self.b)
        mn = min(self.r, self.g, self.b)
        df = mx - mn
        h = 0
        if mx == mn:
            h = 0
        elif mx == self.r:
            h = (60 * ((self.g - self.b) / df) + 360) % 360
        elif mx == self.g:
            h = (60 * ((self.b - self.r) / df) + 120) % 360
        elif mx == self.b:
            h = (60 * ((self.r - self.g) / df) + 240) % 360
        s = 0 if mx == 0 else df / mx
        v = mx
        return h, s * 100, v * 100

    @property
    def xyz(self) -> tuple[float, float, float]:
        """Output as tuple in XYZ color space."""
        r, g, b = (self.r / 255.0, self.g / 255.0, self.b / 255.0)
        r = r / 12.92 if r <= 0.04045 else ((r + 0.055) / 1.055) ** 2.4
        g = g / 12.92 if g <= 0.04045 else ((g + 0.055) / 1.055) ** 2.4
        b = b / 12.92 if b <= 0.04045 else ((b + 0.055) / 1.055) ** 2.4
        r, g, b = r * 100, g * 100, b * 100
        x = r * 0.4124 + g * 0.3576 + b * 0.1805
        y = r * 0.2126 + g * 0.7152 + b * 0.0722
        z = r * 0.0193 + g * 0.1192 + b * 0.9505
        return x, y, z

    @property
    def lab(self) -> tuple[float, float, float]:
        """Output as tuple in LAB color space."""
        x, y, z = [value / ref for value, ref in zip(self.xyz, (95.047, 100.000, 108.883), strict=False)]
        x = x ** (1 / 3) if x > 0.008856 else (7.787 * x) + (16 / 116)
        y = y ** (1 / 3) if y > 0.008856 else (7.787 * y) + (16 / 116)
        z = z ** (1 / 3) if z > 0.008856 else (7.787 * z) + (16 / 116)
        l = (116 * y) - 16
        a = 500 * (x - y)
        b = 200 * (y - z)
        return l, a, b

    @property
    def lch(self) -> tuple[float, float, float]:
        """Output as tuple in LCH color space."""
        l, a, b = self.lab
        c = sqrt(a**2 + b**2)
        h = degrees(atan2(b, a))
        h = h + 360 if h < 0 else h
        return l, c, h
