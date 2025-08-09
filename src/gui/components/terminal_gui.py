from typing import Any

from gui.element import Element, HTMLElement, Input


class _UserInput(Element):
    def __init__(self, text: str, parent: HTMLElement | Element | None = None) -> None:
        super().__init__(tag_name="div", parent=parent)
        self.class_name = "user-input"
        self.text = f"$ {text}"

class _TerminalOutput(Element):
    def __init__(self, text: str, parent: HTMLElement | Element | None = None) -> None:
        super().__init__(tag_name="div", parent=parent)
        self.class_name = "terminal-output"
        self.text = text

class _TerminalHistory(Element):
    _elements = []

    def __init__(self, parent: HTMLElement | Element | None = None) -> None:
        super().__init__(tag_name="div", parent=parent, id="terminal-history")
        self.class_name = "terminal-history"
    
    def add_history(self, element: _UserInput | _TerminalOutput):
        self._elements.append(element)
        self.append_child(element)
        if self["parentElement"] is not None:
            # Scroll to the bottom
            self["parentElement"].scrollTop = self["parentElement"].scrollHeight

class _TerminalInput(Element):
    text_input: Input

    def __init__(self, parent: HTMLElement | Element | None = None) -> None:
        super().__init__(tag_name="div", parent=parent, id="terminal-input", style="""
            display: flex;
            flex-direction: row;
        """)
        self.class_name = "terminal-input"
        self.text = "$ "

        self.text_input = Input(parent=self, id="terminal-input-field", style="""
            background-color: black;
            color: white;
            flex-grow: 1;
            font-family: monospace;
            border: 0;
            outline: 0;
            margin: 0;
            padding: 0;
            font-size: 1rem;
        """)

class TerminalGui(Element):
    def __init__(self, parent: HTMLElement | Element | None = None) -> None:
        super().__init__(tag_name="div", id="terminal", parent=parent, style="""
            background-color: black;
            color: white;
            flex-grow: 1;
            overflow-y: scroll;
            font-family: monospace;
            border: 0;
            outline: 0;
            margin: 0;
            padding: 20px;
            white-space: pre;
        """)
        self.class_name = "terminal"
        self.text = "This is a terminal"

        history = _TerminalHistory(parent=self)
        input = _TerminalInput(parent=self)

        def _submit_input(event: Any) -> None:
            history.add_history(_UserInput(event.target.value, parent=history))
            event.target.value = ""

        input.text_input.on_enter(_submit_input)
