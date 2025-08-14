from typing import Any

from gui.element import Button, Element, HTMLElement

class DescriptionContent(Element):
    def __init__(self, parent: HTMLElement | Element | None = None) -> None:
        super().__init__("div", parent=parent, id="description-content", style="text-align: left;")
        self.class_name = "description-content"
        
        self.content_wrapper = Element(
            "div",
            parent=self,
            style="""padding: 0 20px;""",
        )

        header = Element(
            "h3",
            parent=self.content_wrapper,
        )

        header.text = "How to use the app:"

        paragraph = Element(
            "p",
            parent=self.content_wrapper,
        )

        paragraph.text = (
            "Drag and drop an image file onto the image preview area to upload it. "
            "You can also click the image preview area to select a file from your computer. "
            "Once an image is uploaded, you can interact with it using the terminal commands. "
            "Use the 'help' command to see a list of available commands."
        )

class Description(Element):
    """The description element for displaying useful information to the user."""

    def __init__(self, parent: HTMLElement | Element | None = None) -> None:
        super().__init__("div", parent=parent, id="description")
        self.class_name = "description"

        expand_btn = Button(
            parent=self,
            id="expand-btn",
            style="""
            background-color: var(--description-background-color);
            color: var(--text-color);
            width: 100%;
            text-align: center;
            user-select: none;
            font-family: monospace;
            border: 3px solid var(--description-button-border-color);
        """,
        )
        expand_btn.class_name = "expand-btn"
        expand_btn.text = "About"
        expand_btn.on_click(self._on_expand_btn_click)

        self.description_content = DescriptionContent(parent=self)

        self.on("click", lambda event: event.stopPropagation())

    def _on_expand_btn_click(self, event: Any) -> None:  # noqa: ANN401
        self["classList"].toggle("open")
        event.stopPropagation()
