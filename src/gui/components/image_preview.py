from typing import Any

from gui.element import Element, HTMLElement


class ImagePreview(Element):
    """A component for displaying an image preview with a draggable separator."""

    is_dragging = False

    def __init__(self, parent: HTMLElement | Element | None = None) -> None:
        super().__init__(
            tag_name="div",
            parent=parent,
            id="image-preview",
            style="""
            background-color: #adadad;
            height: 50%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            flex-shrink: 0;
        """,
        )
        self.class_name = "image-preview"
        self.text = "[Placeholder Image]"
        separator = Element(
            "div",
            parent=parent,
            id="separator",
            style="""
            background-color: rgb(119, 119, 119);
            width: 100%;
            height: 1%;
            cursor: pointer;
            flex-shrink: 0;
        """,
        )
        separator.class_name = "separator"

        separator.on("mousemove", self.on_separator_mouse_move)
        separator.on("mousedown", self.on_separator_mouse_down)
        separator.on("mouseup", self.on_separator_mouse_up)

    def on_separator_mouse_move(self, event: Any) -> None:  # noqa: ANN401
        """Handle mouse movement over the separator to adjust the height of the image preview."""
        if not self.is_dragging:
            return
        mouse_y = event.clientY
        self["style"].height = str(mouse_y) + "px"

    def on_separator_mouse_down(self, event: Any) -> None:  # noqa: ANN401
        """Handle mouse down on the separator to start dragging."""
        if event.button != 0:
            return
        self.is_dragging = True

    def on_separator_mouse_up(self, _event: Any) -> None:  # noqa: ANN401
        """Handle mouse up on the separator to stop dragging."""
        self.is_dragging = False
