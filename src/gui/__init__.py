import js # noqa: F401 # type: ignore

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
    font-family: monospace, serif;
}

.image {
    background-color: #adadad;
    height: 50%;
}

.separator {
    background-color: rgb(119, 119, 119);
    width: 100%;
    height: 1%;
    cursor: pointer;
}

.terminal {
    font-size: 1.5em;
    padding: 20px;
    background-color: black;
    color: white;
    flex-grow: 1;
    overflow-y: scroll;
}

.document-panel {
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

.document-panel.open {
    width: 40%;
    height: 100%;
    overflow-y: auto;
    overflow-x: hidden;
}

.expand-btn {
    background-color: rgb(119, 119, 119);
    cursor: pointer;
    width: 100%;
    text-align: center;
    user-select: none;
}

.documents {
    text-align: left;
    padding: 10%;
}
"""

def init_gui() -> Element:
    body = Element(element=js.document.body)
    
    # Set the base style for the app
    base_style = Element("style")
    base_style.text = _base_style
    js.document.head.appendChild(base_style.html_element)

    image = Element("div", parent=body, id="image")
    image.text = "[Placeholder Image]"
    image.class_name = "image"

    is_dragging = False

    def move_separator_to_mouse(_, event):
        if not is_dragging:
            return
        mouse_y = event.clientY
        image["style"].height = str(mouse_y) + "px"
    
    def attach_separator_to_mouse(_, event):
        if event.button != 0:
            return
        nonlocal is_dragging
        is_dragging = True
        body["style"].userSelect = "none"

    def release_separator(_, _event):
        nonlocal is_dragging
        is_dragging = False
        body["style"].userSelect = "auto"
    
    def on_body_mousemove(element, event):
        if is_dragging:
            move_separator_to_mouse(element, event)
    
    body.on("mouseup", release_separator)
    body.on("mousemove", on_body_mousemove)

    separator = Element("div", parent=body, id="separator")
    separator.class_name = "separator"

    separator.on("mousedown", attach_separator_to_mouse)
    separator.on("mouseup", release_separator)
    
    terminal = Element("div", parent=body, id="terminal")
    terminal.class_name = "terminal"
    terminal.text = "Image editor v2.1 $ ping\npong!\nImage editor v2.1 $"

    document_panel = Element("div", parent=body, id="DocumentPanel")
    document_panel.class_name = "document-panel"

    expand_btn = Element("div", parent=document_panel, id="ExpandBtn")
    expand_btn.class_name = "expand-btn"
    expand_btn.text = "☰"

    expand_btn.on("click", lambda _, _event: document_panel["classList"].toggle("open"))

    documents = Element("div", parent=document_panel, id="Documents")
    documents.class_name = "documents"
    documents.text = "How to use the app:"

    return body
