import js  # type: ignore[import]

from gui.components.description import Description
from gui.components.image_preview import ImagePreview
from gui.components.terminal_gui import TerminalGui
from gui.element import Element

_base_style = """
html,
body {
    margin: 0;
    width: 100vw;
    height: 100vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    font-family: monospace;
}

#description {
    position:fixed;
    top: 0;
    right: 0;
    width: 50px;
    height: 5%;
    background-color: grey;
    transition: width 0.3s ease, height 0.3s ease;
    z-index: 100;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    align-items: center;
}

#description.open {
    width: 40%;
    height: 100%;
    overflow-y: auto;
    overflow-x: hidden;
}

#terminal::selection,
#terminal-input::selection,
#terminal-input-field::selection,
.user-input::selection {
    background-color: white;
    color: black;
}

.terminal-output::selection {
    color: black;
    background-color: var(--terminal-output-color, white);
}

.terminal-output {
    color: var(--terminal-output-color, white);
    background-color: black;
}
"""


def init_gui() -> Element:
    """Initialize the GUI."""
    body = Element(element=js.document.body)

    # Set the base style for the app
    base_style = Element("style")
    base_style.text = _base_style
    js.document.head.appendChild(base_style.html_element)

    image_preview = ImagePreview(parent=body)
    TerminalGui(parent=body)
    description = Description(parent=body)

    body.on("click", lambda _: description["classList"].remove("open"))
    body.on("mouseup", image_preview.on_separator_mouse_up)
    body.on("mousemove", image_preview.on_separator_mouse_move)

    return body
