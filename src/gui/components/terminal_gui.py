from collections import deque
from typing import Any

import js  # type: ignore[import]

from gui.element import Element, HTMLElement, Input

KEYCODE_TAB = 9
KEYCODE_ENTER = 13


class _UserInput(Element):
    def __init__(self, text: str, parent: HTMLElement | Element | None = None) -> None:
        super().__init__(tag_name="div", parent=parent)
        self.class_name = "user-input"
        self.text = f"$ {text}"


class _TerminalOutput(Element):
    def __init__(self, text: str, color: str | None = None, parent: HTMLElement | Element | None = None) -> None:
        style = f"--terminal-output-color: {color};" if color is not None else ""
        super().__init__(tag_name="div", parent=parent, style=style)
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

    def clear_history(self) -> None:
        """Clear the terminal history."""
        for element in self._elements:
            self.remove_child(element)
        self._elements.clear()


class _TerminalInput(Element):
    text_input: Input
    suggestion_span: Element
    _input_wrapper: Element

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
        self._input_wrapper = self._make_input_wrapper()

        self.suggestion_span = self._make_suggestion_span()
        self.suggestion_span.class_name = "suggestion-span"
        self.suggestion_span.text = ""

        self.text_input = self._make_text_input()

    def _make_input_wrapper(self) -> Element:
        """Create the input wrapper element."""
        return Element(
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

    def _make_suggestion_span(self) -> Element:
        """Create the suggestion span element."""
        return Element(
            "span",
            parent=self._input_wrapper,
            style="""
                background-color: transparent;
                color: var(--terminal-suggestion-color);
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

    def _make_text_input(self) -> Input:
        """Create the text input element."""
        return Input(
            parent=self._input_wrapper,
            id="terminal-input-field",
            style="""
                background-color: transparent;
                color: var(--terminal-output-color);
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

    # For navigating through previous commands
    # This is used to allow the user to cycle through previous commands with the up/down arrow
    current_command_idx: int | None = None

    def get_suggestion(self, command: str | None) -> str | None:
        """Get a suggestion for the given command. If no suggestion is found, return None."""
        if not command:
            return None
        suggestions = ("help", "ping", "pong", "clear", "clear-terminal", *self.previous_commands)
        return next((suggestion for suggestion in suggestions if suggestion.startswith(command)), None)

    def print_terminal_output(self, text: str, color: str | None = None) -> None:
        """Print the given text to the terminal output with an optional color. If no color is given, white is used."""
        output = _TerminalOutput(text, color=color)
        self.history.add_history(output)

    def clear_terminal_history(self) -> None:
        """Clear the terminal history."""
        self.history.clear_history()
        self.input.text_input["value"] = ""
        self.input.set_suggestion(None)

    def __init__(self, parent: HTMLElement | Element | None = None) -> None:
        super().__init__(
            tag_name="div",
            id="terminal",
            parent=parent,
            style="""
            background-color: var(--terminal-background-color);
            color: var(--terminal-output-color);
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

        self.input.text_input.on("keydown", self._on_input_control_keydown)
        self.input.text_input.on("input", self._on_input)
        self.on("click", self._focus_input)

    def _submit_input(self, event: Any) -> None:  # noqa: ANN401
        value = event.target.value
        self.history.add_history(_UserInput(value))

        last_command = self.previous_commands[-1] if self.previous_commands else None
        if value and (last_command is None or value != last_command):
            self.previous_commands.append(value)

        event.target.value = ""
        self.input.set_suggestion(None)

    def _confirm_suggestion(self, event: Any) -> None:  # noqa: ANN401
        value = event.target.value
        event.target.value = self.get_suggestion(value) or value

    def _navigate_commands(self, offset: int) -> None:
        """Navigate through previous commands based on the offset."""
        if not self.previous_commands:
            return

        if self.current_command_idx is None:
            self.current_command_idx = len(self.previous_commands)

        self.current_command_idx = max(0, self.current_command_idx + offset)
        if self.current_command_idx >= len(self.previous_commands):
            self.current_command_idx = None

        if self.current_command_idx is None:
            self.input.text_input["value"] = ""
        else:
            self.input.text_input["value"] = self.previous_commands[self.current_command_idx]

    def _on_input_control_keydown(self, event: Any) -> None:  # noqa: ANN401
        """Handle keydown events on the terminal input field if a control key was pressed."""
        if event.keyCode == KEYCODE_ENTER:
            self._submit_input(event)
            self.current_command_idx = None
            event.preventDefault()
        elif event.keyCode == KEYCODE_TAB:
            self._confirm_suggestion(event)
            self.current_command_idx = None
            event.preventDefault()
        elif event.key == "ArrowUp":
            self._navigate_commands(-1)
            event.preventDefault()
        elif event.key == "ArrowDown":
            self._navigate_commands(1)
            event.preventDefault()

    def _on_input(self, event: Any) -> None:  # noqa: ANN401
        """Handle input events on the terminal input field."""
        self.input.set_suggestion(self.get_suggestion(event.target.value))
        self.current_command_idx = None

    def _focus_input(self, _event: Any) -> None:  # noqa: ANN401
        """Focus the input field."""
        if len(js.window.getSelection().toString()) > 0:
            # If text is selected, do not steal focus
            return
        self.input.text_input["focus"]()
