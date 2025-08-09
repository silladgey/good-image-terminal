from typing import Protocol

class MouseEvent(Protocol):
    """Defines a mouse event from the browser. This is a partial reflection of the DOM API."""
    button: int
    clientX: int  # noqa: N815
    clientY: int  # noqa: N815
