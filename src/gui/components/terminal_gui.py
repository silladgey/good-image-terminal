from collections import deque
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
    suggestion_span: Element

    def __init__(self, parent: HTMLElement | Element | None = None) -> None:
        super().__init__(tag_name="div", parent=parent, id="terminal-input", style="""
            display: flex;
            flex-direction: row;
            align-items: center;
            flex-shrink: 0;
        """)
        self.class_name = "terminal-input"
        self.text = "$ "

        # Wrapper for suggestion and input, to allow overlap
        self._input_wrapper = Element(
            "div",
            parent=self,
            style="""
                position: relative;
                flex-grow: 1;
                width: 100%;
                display: flex;
                align-items: center;
            """
        )

        self.suggestion_span = Element(
            "span",
            parent=self._input_wrapper,
            style="""
                background-color: transparent;
                color: rgb(119, 119, 119);
                font-family: monospace;
                position: absolute;
                left: 0;
                top: 0;
                width: 100%;
                font-size: 1rem;
                pointer-events: none;
                white-space: pre;
            """,
            id="suggestion-span"
        )
        self.suggestion_span.class_name = "suggestion-span"
        self.suggestion_span.text = ""

        self.text_input = Input(
            parent=self._input_wrapper,
            id="terminal-input-field",
            style="""
                background-color: transparent;
                color: white;
                width: 100%;
                font-family: monospace;
                border: 0;
                outline: 0;
                margin: 0;
                padding: 0;
                font-size: 1rem;
                position: relative;
                z-index: 1;
            """
        )
    
    def set_suggestion(self, suggestion: str | None) -> None:
        if not suggestion:
            self.suggestion_span.text = ""
            return
        self.suggestion_span.text = suggestion

class TerminalGui(Element):
    max_previous_commands: int = 20
    previous_commands: deque[str]

    def get_suggestion(self, command: str | None) -> str | None:
        if not command:
            return None
        suggestions = (
            "help",
            "ping",
            "pong",
            "clear",
        ) + tuple(self.previous_commands)
        return next((suggestion for suggestion in suggestions if suggestion.startswith(command)), None)
    
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
        self.previous_commands = deque(maxlen=self.max_previous_commands)
        self.class_name = "terminal"
        self.text = "This is a terminal"

        history = _TerminalHistory(parent=self)
        input = _TerminalInput(parent=self)

        def _submit_input(event: Any) -> None:
            value = event.target.value
            history.add_history(_UserInput(value, parent=history))
            if value:
                self.previous_commands.appendleft(value)
            event.target.value = ""
            input.set_suggestion(None)
        
        def _on_input(event: Any) -> None:
            input.set_suggestion(self.get_suggestion(event.target.value))
        
        def _confirm_suggestion(event: Any) -> None:
            value = event.target.value
            event.target.value = self.get_suggestion(value) or value
        
        input.text_input.on_enter(_submit_input)
        input.text_input.on_input(_on_input)
        input.text_input.on_tab(_confirm_suggestion)

        self.on("click", lambda _: input.text_input["focus"]())
