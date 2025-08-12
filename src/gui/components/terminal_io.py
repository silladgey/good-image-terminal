"""Terminal input and output components for the terminal GUI."""
from gui.element import Element, HTMLElement
import re

class UserInput(Element):
    def __init__(self, text: str, parent: HTMLElement | Element | None = None) -> None:
        super().__init__(tag_name="div", parent=parent)
        self.class_name = "user-input"
        self.text = "$ "

        command_verb_span = Element(tag_name="span")
        command_verb_span.class_name = "command-verb-span"

        command_verb = re.search(r"^(\s*)(\S+)\b", text)

        if command_verb:
            self.text += command_verb.group(1)

            command_verb_span.text = command_verb.group(2)
            self.append_child(command_verb_span)

            command_end = text[len(command_verb.group(0)) :]
            command_end_span = Element(tag_name="span")
            command_end_span.text = command_end
            self.append_child(command_end_span)
        else:
            self.text += text

class TerminalOutput(Element):
    def __init__(self, text: str, color: str | None = None, parent: HTMLElement | Element | None = None) -> None:
        style = f"--terminal-output-color: {color};" if color is not None else ""
        super().__init__(tag_name="div", parent=parent, style=style)
        self.class_name = "terminal-output"
        self.text = text

class TerminalInputVerb(Element):
    def __init__(self, parent: HTMLElement | Element | None = None, style: str | None = None) -> None:
        super().__init__(tag_name="span", parent=parent, style=style)
        self.class_name = "terminal-input-verb"

        self.wrapper = Element(
            tag_name="span",
            parent=self,
            style="""
            position: relative;
            display: inline-block;
            flex-shrink: 0;
        """,
        )

        self.space_span = Element(tag_name="span", parent=self.wrapper)
        self.space_span.class_name = "terminal-input-space"

        self.verb_span = Element(tag_name="span", parent=self.wrapper)
        self.verb_span.class_name = "terminal-input-verb-text"

    def set_text(self, start_space: str, verb: str) -> None:
        self.space_span.text = " " * len(start_space)
        self.verb_span.text = " " * len(verb)

class TerminalHistory(Element):
    _elements: list[UserInput | TerminalOutput]

    def __init__(self, parent: HTMLElement | Element | None = None) -> None:
        super().__init__(tag_name="div", parent=parent, id="terminal-history")
        self._elements = []
        self.class_name = "terminal-history"

    def add_history(self, element: UserInput | TerminalOutput) -> None:
        self._elements.append(element)
        self.append_child(element)
        if self["parentElement"] is not None:
            self["parentElement"].scrollTop = self["parentElement"].scrollHeight

    def clear_history(self) -> None:
        for element in self._elements:
            self.remove_child(element)
        self._elements.clear()
