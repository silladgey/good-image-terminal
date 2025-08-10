from collections import deque
from typing import Any

import js  # type: ignore[import]

from gui.element import Element, HTMLElement, Input


class _UserInput(Element):
    def __init__(self, text: str, parent: HTMLElement | Element | None = None) -> None:
        super().__init__(tag_name="div", parent=parent)
        self.class_name = "user-input"
        self.text = f"$ {text}"


class _TerminalOutput(Element):
    def __init__(self, text: str, color: str | None = None, parent: HTMLElement | Element | None = None) -> None:
        if not color:
            color = "white"
        super().__init__(tag_name="div", parent=parent, style=f"--terminal-output-color: {color};")
        self.class_name = "terminal-output"
        self.text = text


class _TerminalHistory(Element):
    _elements: list[_UserInput | _TerminalOutput]

    def __init__(self, parent: HTMLElement | Element | None = None) -> None:
        super().__init__(tag_name="div", parent=parent, id="terminal-history")
        self._elements = []
        self.class_name = "terminal-history"

    def add_history(self, element: _UserInput | _TerminalOutput) -> None:
        self._elements.append(element)
        self.append_child(element)
        if self["parentElement"] is not None:
            # Scroll to the bottom
            self["parentElement"].scrollTop = self["parentElement"].scrollHeight


class _TerminalInput(Element):
    text_input: Input
    suggestion_span: Element

    def __init__(self, parent: HTMLElement | Element | None = None) -> None:
        super().__init__(
            tag_name="div",
            parent=parent,
            id="terminal-input",
            style="""
            display: flex;
            flex-direction: row;
            align-items: center;
            flex-shrink: 0;
        """,
        )
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
            """,
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
            id="suggestion-span",
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
            """,
        )

    def set_suggestion(self, suggestion: str | None) -> None:
        if not suggestion:
            self.suggestion_span.text = ""
            return
        self.suggestion_span.text = suggestion


class TerminalGui(Element):
    """The terminal GUI component for displaying terminal-like output and input."""

    max_previous_commands: int = 20
    previous_commands: deque[str]

    def get_suggestion(self, command: str | None) -> str | None:
        """Get a suggestion for the given command. If no suggestion is found, return None."""
        if not command:
            return None
        suggestions = ("help", "ping", "pong", "clear", *self.previous_commands)
        return next((suggestion for suggestion in suggestions if suggestion.startswith(command)), None)

    def print_terminal_output(self, text: str, color: str | None = None) -> None:
        """Print the given text to the terminal output with an optional color. If no color is given, white is used."""
        output = _TerminalOutput(text, color=color)
        self.history.add_history(output)

    def __init__(self, parent: HTMLElement | Element | None = None) -> None:
        super().__init__(
            tag_name="div",
            id="terminal",
            parent=parent,
            style="""
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
        """,
        )
        self.previous_commands = deque(maxlen=self.max_previous_commands)
        self.class_name = "terminal"

        self.history = _TerminalHistory(parent=self)
        self.input = _TerminalInput(parent=self)

        def submit_input(event: Any) -> None:  # noqa: ANN401
            value = event.target.value
            self.history.add_history(_UserInput(value))
            if value:
                self.previous_commands.appendleft(value)
            event.target.value = ""
            self.input.set_suggestion(None)
            self.print_terminal_output(f"{value!r} is not a valid command", color="red")

        def on_input(event: Any) -> None:  # noqa: ANN401
            self.input.set_suggestion(self.get_suggestion(event.target.value))

        def confirm_suggestion(event: Any) -> None:  # noqa: ANN401
            value = event.target.value
            event.target.value = self.get_suggestion(value) or value

        self.input.text_input.on_enter(submit_input)
        self.input.text_input.on_input(on_input)
        self.input.text_input.on_tab(confirm_suggestion)

        def focus_input(event: Any) -> None:  # noqa: ANN401
            if event.target != event.currentTarget or js.window.getSelection().anchorNode == self.html_element:
                # If the click is on the terminal element itself, focus the input
                # Otherwise, do nothing
                return
            self.input.text_input["focus"]()

        self.on("click", focus_input)
