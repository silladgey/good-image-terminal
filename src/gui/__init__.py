import js  # type: ignore[import]

from gui.components.description import Description
from gui.element import Element
from gui.layout import Layout
from image import PaintImage
from terminal import Terminal

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

:root {
    --terminal-background-color: black;
    --terminal-output-color: white;
    --terminal-suggestion-color: rgb(119, 119, 119);
    --description-background-color: #d3d3d3;
    --image-preview-background-color: #f0f0f0;
    --separator-color: #ccc;
}

#description {
    position:fixed;
    top: 0;
    right: 0;
    width: 50px;
    height: 5%;
    background-color: var(--description-background-color);
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

#image-preview {
    cursor: pointer;
}

#image-preview:hover {
    background-color: #b8b8b8;
}

#image-preview.drag-over {
    background-color: #e3f2fd !important;
    border-color: #2196f3 !important;
}

#image-preview {
    cursor: pointer;
}

#image-preview:hover {
    background-color: #b8b8b8;
}

#image-preview.drag-over {
    background-color: #e3f2fd !important;
    border-color: #2196f3 !important;
}

#terminal, #terminal * {
    color: var(--terminal-output-color);
    background-color: var(--terminal-background-color);
}

#terminal::selection, #terminal *::selection {
    color: var(--terminal-background-color);
    background-color: var(--terminal-output-color);
}

.terminal-input-verb-text, .command-verb-span {
    text-decoration: underline;
}
"""


def init_gui() -> Element:
    """
    Initialize the GUI.

    Authors:
        Jont
        Ricky
    """
    body = Element(element=js.document.body)

    # Set the base style for the app
    base_style = Element("style")
    base_style.text = _base_style
    js.document.head.appendChild(base_style.html_element)

    # Create the main layout with image preview, separator, and terminal
    layout = Layout(parent=body)

    # Create the description component
    description = Description(parent=body)

    # Set up global event handlers
    body.on("click", lambda _: description["classList"].remove("open"))
    body.on("mouseup", image_preview.on_separator_mouse_up)
    body.on("mousemove", image_preview.on_separator_mouse_move)

    return body
