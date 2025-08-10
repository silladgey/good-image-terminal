import base64
import io
import pathlib

from PIL import Image as _Image

from utils.color import Color

IMAGES_DIR = pathlib.Path(__file__).parent.resolve() / "images"


class PaintImage:
    """Image for creation of image objects.

    :author: Mira
    """

    def __init__(self) -> None:
        """Create an image object."""
        self.buf = io.BytesIO()
        self.img_name = ""
        self.img = _Image.new("RGB", (400, 250), (0, 0, 0))
        self._custom_image = False

    def load(self, image_name: str = "default.png") -> int:
        """Load image from images.

        params image_name: name of an image with .ext
        return returns 0 if image has loaded 1 if the image wasn't located
        """
        if (IMAGES_DIR / image_name).exists():
            self.img = _Image.open(IMAGES_DIR / image_name, "r").copy()
            self.img_name = image_name
            return 0
        return 1

    def save(self) -> int:
        """Save image to images/.

        return returns 0 if image has saved 1 if the image wasn't
        """
        if self.img_name:
            self.img.save(IMAGES_DIR / self.img_name, format="PNG")
        else:
            print("Can't save an empty image.")
            return 1
        return 0

    def get_js_link(self) -> str:
        """Return base64 link for an image file.

        return string - image src link
        """
        self.img.save(self.buf, format="PNG")
        data = base64.b64encode(self.buf.getvalue()).decode("utf-8")
        return f"data:image/png;base64,{data}"

    def get_image_info(self) -> dict:
        """Return image information dictionary.

        return dictionary
        """
        return {
            "size": self.img.size,
            "format": self.img.format,
        }

    def set_pixel(self, x: int, y: int, color: Color) -> None:
        """Set an image pixel."""
        self.img.putpixel((x, y), color)

    def get_pixel(self, x: int, y: int) -> tuple[int, ...]:
        """Get an image pixel."""
        return self.img.getpixel((x, y))
