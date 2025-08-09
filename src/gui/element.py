"""
Defines GUI elements.

@author Jont
"""

from __future__ import annotations

from typing import Protocol, Callable, Any

import js # noqa: F401 # type: ignore
from pyodide.ffi import create_proxy


class HTMLElement(Protocol):
    """ Define a protocol for HTML elements to allow for type checking. This is a subset of the DOM API. """

    id: str
    textContent: str
    innerHTML: str
    value: str
    style: Any
    className: str

    def appendChild(self, child: HTMLElement) -> None:
        ...
    
    def addEventListener(self, event: str, handler: Callable) -> None:
        ...
    
    def setAttribute(self, name: str, value: str) -> None:
        ...


class Element:
    """ 
    Base class for all GUI elements. This is a wrapper around an HTML element. 

    Element provides several convenience methods for accessing the underlying HTML element. Getting or setting an item 
    will access the underlying HTML element directly.

    ```py
    element = Element("div")
    element["style"].color = "red"
    ```

    If a convenience method exists on Element, it should be used instead of accessing the underlying HTML element directly.
    """
    _html_element: HTMLElement

    def __init__(self, tag_name: str | None = None, *, element: HTMLElement | None = None, parent: HTMLElement | Element | None = None, **kwargs) -> None:
        if element is not None:
            # Initialize from an existing HTML element
            assert tag_name is None, "Cannot specify both element and tag name"
            assert parent is None, "Cannot specify both element and parent"
            assert not kwargs, "Cannot specify both element and kwargs"
            self._html_element = element
            return
        
        self._html_element = js.document.createElement(tag_name, kwargs)

        for key, value in kwargs.items():
            self._html_element.setAttribute(key, value)
        
        if isinstance(parent, Element):
            root = parent.html_element
        elif parent is None:
            root = js.document.body
        else:
            root = parent

        root.appendChild(self.html_element)

    @property
    def html_element(self) -> HTMLElement:
        """ Get the underlying HTML element. This is a read-only property. """
        return self._html_element
    
    def on(self, event: str, handler: Callable[[Element, Any], None]) -> None:
        """ Add an event handler to the element. The handler will be called with the element as the first argument. """
        def event_handler(event: Any) -> None:
            handler(self, event)
        self.html_element.addEventListener(event, create_proxy(event_handler))
    
    @property
    def text(self) -> str:
        """ Get or set the text content of the element. """
        return self.html_element.textContent
    
    @text.setter
    def text(self, value: str) -> None:
        self.html_element.textContent = value

    @property
    def html(self) -> str:
        """ Get or set the HTML content of the element. """
        return self.html_element.innerHTML
    
    @html.setter
    def html(self, value: str) -> None:
        self.html_element.innerHTML = value
    
    @property
    def class_name(self) -> str:
        """ Get or set the class name of the element. """
        return self.html_element.className
    
    @class_name.setter
    def class_name(self, value: str) -> None:
        self.html_element.className = value
    
    def __getitem__(self, key: str) -> Any:
        return getattr(self.html_element, key)
    
    def __setitem__(self, key: str, value: Any) -> None:
        setattr(self.html_element, key, value)

class Button(Element):
    def __init__(self, parent: HTMLElement | None = None, **kwargs) -> None:
        super().__init__("button", parent=parent, **kwargs)

    def on_click(self, handler: Callable[[Element, Any], None]) -> None:
        self.on("click", handler)

class Input(Element):
    def __init__(self, parent: HTMLElement | None = None, **kwargs) -> None:
        super().__init__("input", parent=parent, **kwargs)
    
    def on_change(self, handler: Callable[[Element, Any], None]) -> None:
        self.on("change", handler)

    def on_input(self, handler: Callable[[Element, Any], None]) -> None:
        self.on("input", handler)
    