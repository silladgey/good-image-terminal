import base64
import io
import pathlib

from PIL import Image as _Image

IMAGES_DIR = pathlib.Path(__file__).parent.resolve() / "images"


class Image:
    """Image for creation of image objects.

    @author Mira
    """

    def __init__(self) -> None:
        """Create an image object.

        @author Mira
        """
        self.buf = io.BytesIO()
        self.img_name = ""
        self.img = _Image.new("RGB", (400, 250), (0, 0, 0))
        self._custom_image = False

    def load(self, image_name: str = "default.png") -> int:
        """Load image from images/.

        @author Mira
        @params image_name: name of an image with .ext
        @return returns 0 if image has loaded 1 if the image wasn't located
        """
        if (IMAGES_DIR / image_name).exists():
            self.img = _Image.open(IMAGES_DIR / image_name, "r")
            self.img_name = image_name
            return 0
        return 1

    def save(self) -> int:
        """Save image to images/.

        @author Mira
        @return returns 0 if image has saved 1 if the image wasn't
        """
        if self.img_name:
            self.img.save(IMAGES_DIR / self.img_name, format="PNG")
        else:
            print("Can't save an empty image.")
            return 1
        return 0

    def get_js_link(self) -> str:
        """Return base64 link for an image file.

        @author Mira
        @return string - image src link
        """
        self.img.save(self.buf, format="PNG")
        data = base64.b64encode(self.buf.getvalue()).decode("utf-8")
        return f"data:image/png;base64,{data}"

    def get_image_info(self) -> dict:
        """Return image information dictionary.

        @author Mira
        @return dictionary
        """
        return {
            "size": self.img.size,
            "format": self.img.format,
        }
