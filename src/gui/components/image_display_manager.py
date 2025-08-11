import traceback

import js  # type: ignore[import]

from gui.element import Element
from image import PaintImage


class ImageDisplayManager:
    """Manages image display and placeholder functionality.

    Authors:
        Ricky
    """

    def __init__(self, container: Element) -> None:
        """Initialize image display manager.

        Args:
            container: The container element to create image display elements in

        """
        self.container = container
        self.current_image_src: str | None = None
        self._setup_elements()
        self._load_default_image()

    def _setup_elements(self) -> None:
        """Create the image container, image element, and placeholder text."""
        # Create container for image or placeholder
        self.image_container = Element(
            "div",
            parent=self.container,
            style="""
            width: 100%;
            height: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
        """,
        )

        # Create image element (initially hidden)
        self.image_element = Element(
            "img",
            parent=self.image_container,
            style="""
            max-width: 100%;
            max-height: 100%;
            display: none;
            object-fit: contain;
        """,
        )

        # Create placeholder text
        self.placeholder_text = Element(
            "div",
            parent=self.image_container,
            style="""
            font-size: 18px;
            color: #666;
            text-align: center;
            user-select: none;
        """,
        )
        self.placeholder_text.text = "Loading default image..."

    def _load_default_image(self) -> None:
        """Load and display the default.png image from the images folder."""
        try:
            img = PaintImage()
            result = img.load("default.png")

            if result == 0:  # success
                js_link = img.get_js_link()
                self.display_image(js_link)
            else:
                # Update placeholder to show drag/drop functionality
                self.placeholder_text.text = "Drop an image here or click to upload"
        except ImportError as e:
            print(f"Import error loading image module: {e!s}")
            self.placeholder_text.text = "Drop an image here or click to upload"
        except (AttributeError, OSError, ValueError) as e:
            print(f"Error loading default image: {e!s}")
            self.placeholder_text.text = "Drop an image here or click to upload"
            traceback.print_exc()

    def display_image(self, image_src: str) -> None:
        """Display an image in the preview area."""
        self.current_image_src = image_src
        self.image_element["src"] = image_src
        self.image_element["style"].display = "block"
        self.placeholder_text["style"].display = "none"

    def hide_image(self) -> None:
        """Hide the current image (useful during drag operations)."""
        if self.current_image_src:
            self.image_element["style"].display = "none"

    def show_image(self) -> None:
        """Show the current image again."""
        if self.current_image_src:
            self.image_element["style"].display = "block"

    def show_error(self, message: str) -> None:
        """Show an error message."""
        self.placeholder_text.text = f"Error: {message}"
        self.placeholder_text["style"].color = "red"
        js.setTimeout(self._reset_placeholder, 3000)

    def _reset_placeholder(self) -> None:
        """Reset placeholder to original state."""
        if not self.current_image_src:
            self.placeholder_text.text = "Drop an image here or click to upload"
            self.placeholder_text["style"].color = "#666"
