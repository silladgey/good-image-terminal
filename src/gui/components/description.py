from typing import Any

from gui.element import Element, HTMLElement, Button

class Description(Element):
    """The description element for displaying useful information to the user."""
    def __init__(self, parent: HTMLElement | Element | None = None) -> None:  # noqa: ANN401
        super().__init__("div", parent=parent, id="description")
        self.class_name = "description"

        expand_btn = Button(parent=self, id="expand-btn", style="""
            background-color: rgb(119, 119, 119);
            width: 100%;
            text-align: center;
            user-select: none;
        """)
        expand_btn.class_name = "expand-btn"
        expand_btn.text = "☰"
        expand_btn.on_click(self._on_expand_btn_click)

        description_content = Element("div", parent=self, id="description-content", style="""
            text-align: left;
            padding: 10%;
        """)
        description_content.class_name = "description-content"
        description_content.text = "How to use the app:"

        self.on("click", lambda event: event.stopPropagation())
    
    def _on_expand_btn_click(self, event: Any) -> None:
        self["classList"].toggle("open")
        event.stopPropagation()
