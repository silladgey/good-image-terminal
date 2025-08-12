from __future__ import annotations

from collections import deque
from typing import TYPE_CHECKING, Any

import js  # type: ignore[import]

from gui.element import Element, HTMLElement

from .terminal_input import TerminalInput
from .terminal_io import TerminalHistory, TerminalOutput, UserInput

if TYPE_CHECKING:
    from terminal import Terminal

KEYCODE_TAB = 9
KEYCODE_ENTER = 13


class CssVariables:
    """A class for managing CSS variables for an Element."""

    element: Element

    def __init__(self, element: Element) -> None:
        self.element = element

    def __getitem__(self, name: str) -> str:
        return js.window.getComputedStyle(self.element.html_element).getPropertyValue(name)

    def __setitem__(self, name: str, value: str) -> None:
        return self.element.html_element.style.setProperty(name, value)


class TerminalGui(Element):
    """The terminal GUI component for displaying terminal-like output and input."""

    max_previous_commands: int = 20
    previous_commands: deque[str]
    current_command_idx: int | None = None
    terminal: Terminal | None = None

    css_variables: CssVariables

    def get_suggestion(self, command: str | None) -> str | None:
        """Get a suggestion for the given command."""
        if not command:
            return None
        return None
        suggestions = ("help", "ping", "pong", "clear", *self.previous_commands)
        return next((suggestion for suggestion in suggestions if suggestion.startswith(command)), None)

    def print_terminal_output(self, text: str, color: str | None = None) -> None:
        """Print the given text to the terminal output."""
        output = TerminalOutput(text, color=color)
        self.history.add_history(output)

    def clear_terminal_history(self) -> None:
        """Clear the terminal history."""
        self.history.clear_history()
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

        self.css_variables = CssVariables(self)
        self.previous_commands = deque(maxlen=self.max_previous_commands)
        self.class_name = "terminal"

        self.history = TerminalHistory(parent=self)
        self.input = TerminalInput(parent=self)

        self.input.text_input.on("keydown", self._on_input_control_keydown)
        self.input.text_input.on("input", self._on_input)
        self.on("click", self._focus_input)

    def _submit_input(self, event: Any) -> None:  # noqa: ANN401
        value = event.target.value
        self.history.add_history(UserInput(value))

        last_command = self.previous_commands[-1] if self.previous_commands else None
        if value and (last_command is None or value != last_command):
            self.previous_commands.append(value)

        if self.terminal is not None:
            self.terminal.run_str(value)
        else:
            print("Warning: TerminalGui has no Terminal instance assigned.")

        event.target.value = ""
        self.input.set_suggestion(None)
        self.input.set_value("")

    def _confirm_suggestion(self, event: Any) -> None:  # noqa: ANN401
        value = event.target.value
        self.input.set_value(self.get_suggestion(value) or value)

    def _navigate_commands(self, offset: int) -> None:
        if not self.previous_commands:
            return
        if self.current_command_idx is None:
            self.current_command_idx = len(self.previous_commands)
        self.current_command_idx = max(0, self.current_command_idx + offset)
        if self.current_command_idx >= len(self.previous_commands):
            self.current_command_idx = None
        if self.current_command_idx is None:
            self.input.set_value("")
        else:
            self.input.set_value(self.previous_commands[self.current_command_idx])

    def _on_input_control_keydown(self, event: Any) -> None:  # noqa: ANN401
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
        self.input.set_suggestion(self.get_suggestion(event.target.value))
        self.input.set_value(event.target.value)
        self.current_command_idx = None

    def _focus_input(self, _event: Any) -> None:  # noqa: ANN401
        if len(js.window.getSelection().toString()) > 0:
            return
        self.input.text_input["focus"]()
