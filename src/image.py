from PIL import Image as _Image
import io, base64

class Image:
    def __init__(self) -> None:
        self.buf = io.BytesIO()
        self.img = _Image.new("RGB", (400,250), (0,0,0))
        return
    def load_image(self, image_name: str) -> None:
        self.img = _Image.open(image_name, "r")
        return
    def get_js_link(self) -> str:
        self.img.save(self.buf, format="PNG")
        data = base64.b64encode(self.buf.getvalue()).decode("utf-8")
        return f"data:image/png;base64,{data}"
