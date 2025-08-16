from typing import Any

from gui.element import Element


class ImageDisplayManager:
    """Manages image display and placeholder functionality.

    Authors:
        Ricky
    """

    image_container: Element
    image_element: Element
    placeholder_text: Element
    cursor_info_element: Element

    def __init__(self, container: Element, cursor_info_element: Element) -> None:
        """Initialize image display manager.

        Args:
            container: The container element to create image display elements in
            cursor_info_element: The cursor info element to update

        """
        self.container = container
        self.current_image_src: str | None = None
        self.cursor_info = cursor_info_element

        self._setup_elements()

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

        # Add mouse move event to update cursor info
        self.image_element.on("mousemove", self._on_image_mouse_move)

        # Add mouse leave event to clear cursor info
        self.image_element.on("mouseleave", self._on_image_mouse_leave)

    def _on_image_mouse_move(self, event: Any) -> None:  # noqa: ANN401
        """Handle mouse movement over the image to update cursor info."""
        if self.current_image_src:
            intrinsic_mouse_x = int(
                ((event.clientX - self.image_element["offsetLeft"]) / self.image_element["clientWidth"])
                * self.image_element["naturalWidth"],
            )
            intrinsic_mouse_y = int(
                ((event.clientY - self.image_element["offsetTop"]) / self.image_element["clientHeight"])
                * self.image_element["naturalHeight"],
            )
            self.cursor_info.text = f"X: {intrinsic_mouse_x}, Y: {intrinsic_mouse_y}"
        else:
            self.cursor_info.text = ""

    def _on_image_mouse_leave(self, _event: Any) -> None:  # noqa: ANN401
        """Clear cursor info when mouse leaves the image."""
        self.cursor_info.text = ""

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
        print(message)

    def _reset_placeholder(self) -> None:
        """Reset placeholder to original state."""
        if not self.current_image_src:
            self.placeholder_text.text = "Drop an image here or click to upload"
            self.placeholder_text["style"].color = "#666"
