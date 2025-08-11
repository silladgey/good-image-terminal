from typing import Any

import js  # type: ignore[import]

from gui.element import Element, HTMLElement


class ImagePreview(Element):
    """A component for displaying an image preview with a drag-drop upload functionality."""

    is_dragging = False
    current_image_src = None

    def __init__(self, parent: HTMLElement | Element | None = None) -> None:
        super().__init__(
            tag_name="div",
            parent=parent,
            id="image-preview",
            style="""
            background-color: #adadad;
            height: 50%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            flex-shrink: 0;
            position: relative;
            border: 2px dashed transparent;
            transition: border-color 0.3s ease, background-color 0.3s ease;
        """,
        )
        self.class_name = "image-preview"

        # Create container for image or placeholder
        self.image_container = Element(
            "div",
            parent=self,
            style="""
            width: 100%;
            height: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
        """,
        )

        # Create image element (initially hidden)
        self.image_element = Element(
            "img",
            parent=self.image_container,
            style="""
            max-width: 100%;
            max-height: 100%;
            display: none;
            object-fit: contain;
        """,
        )

        # Create placeholder text
        self.placeholder_text = Element(
            "div",
            parent=self.image_container,
            style="""
            font-size: 18px;
            color: #666;
            text-align: center;
            user-select: none;
        """,
        )
        self.placeholder_text.text = "Loading default image..."

        # Create drag overlay
        self.drag_overlay = Element(
            "div",
            parent=self,
            style="""
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 123, 255, 0.1);
            border: 2px dashed #007bff;
            display: none;
            justify-content: center;
            align-items: center;
            z-index: 10;
        """,
        )

        overlay_text = Element(
            "div",
            parent=self.drag_overlay,
            style="""
            font-size: 24px;
            color: #007bff;
            font-weight: bold;
            text-align: center;
            user-select: none;
        """,
        )
        overlay_text.text = "Drop image here"

        # Add drag and drop event listeners
        self._setup_drag_and_drop()

        # Add click to upload functionality
        self.on("click", self._handle_click_upload)

        separator = Element(
            "div",
            parent=parent,
            id="separator",
            style="""
            background-color: rgb(119, 119, 119);
            width: 100%;
            height: 1%;
            cursor: pointer;
            flex-shrink: 0;
        """,
        )
        separator.class_name = "separator"

        separator.on("mousemove", self.on_separator_mouse_move)
        separator.on("mousedown", self.on_separator_mouse_down)
        separator.on("mouseup", self.on_separator_mouse_up)

        self._load_default_image()

    def _load_default_image(self) -> None:
        """Load and display the default.png image from the images folder."""
        try:
            from image import Image

            img = Image()
            result = img.load("default.png")

            if result == 0:  # success
                js_link = img.get_js_link()
                self.display_image(js_link)
            else:
                # Update placeholder to show drag/drop functionality
                self.placeholder_text.text = "Drop an image here or click to upload"
        except ImportError as e:
            print(f"Import error loading image module: {str(e)}")
            self.placeholder_text.text = "Drop an image here or click to upload"
        except Exception as e:
            print(f"Error loading default image: {str(e)}")
            self.placeholder_text.text = "Drop an image here or click to upload"
            import traceback

            traceback.print_exc()

    def _setup_drag_and_drop(self) -> None:
        """Set up drag and drop event handlers."""
        self.on("dragover", self._handle_drag_over)
        self.on("dragenter", self._handle_drag_enter)
        self.on("dragleave", self._handle_drag_leave)
        self.on("drop", self._handle_drop)

    def _handle_drag_over(self, event: Any) -> None:  # noqa: ANN401
        """Handle drag over event."""
        event.preventDefault()
        event.stopPropagation()

    def _handle_drag_enter(self, event: Any) -> None:  # noqa: ANN401
        """Handle drag enter event."""
        event.preventDefault()
        event.stopPropagation()
        self.drag_overlay["style"].display = "flex"
        self["style"].borderColor = "#007bff"

        # Hide the current image when dragging over
        if self.current_image_src:
            self.image_element["style"].display = "none"

    def _handle_drag_leave(self, event: Any) -> None:  # noqa: ANN401
        """Handle drag leave event."""
        event.preventDefault()
        event.stopPropagation()
        # Only hide overlay if we're leaving the image preview container
        try:
            related_target = event.relatedTarget
            if related_target is None or not self.html_element.contains(related_target):
                self.drag_overlay["style"].display = "none"
                self["style"].borderColor = "transparent"

                # Show the image again when drag leaves
                if self.current_image_src:
                    self.image_element["style"].display = "block"
        except (AttributeError, TypeError):
            # If there's any issue accessing relatedTarget, just hide the overlay
            self.drag_overlay["style"].display = "none"
            self["style"].borderColor = "transparent"
            if self.current_image_src:
                self.image_element["style"].display = "block"

    def _handle_drop(self, event: Any) -> None:  # noqa: ANN401
        """Handle file drop event."""
        event.preventDefault()
        event.stopPropagation()

        self.drag_overlay["style"].display = "none"
        self["style"].borderColor = "transparent"

        files = event.dataTransfer.files
        if files.length > 0:
            file = files[0]
            if file.type.startswith("image/"):
                self._handle_file_upload(file)
            else:
                self._show_error("Please drop an image file (PNG, JPG, etc.)")

    def _handle_click_upload(self, event: Any) -> None:  # noqa: ANN401
        """Handle click to upload functionality."""
        # Create a hidden file input
        file_input = js.document.createElement("input")
        file_input.type = "file"
        file_input.accept = "image/*"
        file_input.style.display = "none"

        # Handle file selection
        def handle_file_select(e):
            files = e.target.files
            if files.length > 0:
                self._handle_file_upload(files[0])

        file_input.addEventListener("change", handle_file_select)
        js.document.body.appendChild(file_input)
        file_input.click()
        js.document.body.removeChild(file_input)

    def _handle_file_upload(self, file: Any) -> None:  # noqa: ANN401
        """Handle the uploaded file."""
        # Create FileReader to read the file
        reader = js.FileReader.new()

        def on_load(event):
            # Get the file data
            array_buffer = event.target.result
            uint8_array = js.Uint8Array.new(array_buffer)

            # Convert to Python bytes
            image_bytes = bytes(uint8_array.to_py())

            # Load into our Image class
            try:
                from image import Image

                img = Image()
                if img.load_from_bytes(image_bytes, file.name) == 0:
                    # Successfully loaded, display the image
                    self.display_image(img.get_js_link())
                    print(f"Successfully loaded image: {file.name}")
                    print(f"Image size: {img.get_image_info()['size']}")
                else:
                    self._show_error("Failed to load image")
            except Exception as e:
                self._show_error(f"Error processing image: {str(e)}")

        reader.addEventListener("load", on_load)
        reader.readAsArrayBuffer(file)

    def display_image(self, image_src: str) -> None:
        """Display an image in the preview area."""
        self.current_image_src = image_src
        self.image_element["src"] = image_src
        self.image_element["style"].display = "block"
        self.placeholder_text["style"].display = "none"

    def _show_error(self, message: str) -> None:
        """Show an error message."""
        self.placeholder_text.text = f"Error: {message}"
        self.placeholder_text["style"].color = "red"
        js.setTimeout(self._reset_placeholder(), 3000)

    def _reset_placeholder(self) -> None:
        """Reset placeholder to original state."""
        if not self.current_image_src:
            self.placeholder_text.text = "Drop an image here or click to upload"
            self.placeholder_text["style"].color = "#666"

    def on_separator_mouse_move(self, event: Any) -> None:  # noqa: ANN401
        """Handle mouse movement over the separator to adjust the height of the image preview."""
        if not self.is_dragging:
            return
        mouse_y = event.clientY
        self["style"].height = str(mouse_y) + "px"

    def on_separator_mouse_down(self, event: Any) -> None:  # noqa: ANN401
        """Handle mouse down on the separator to start dragging."""
        if event.button != 0:
            return
        self.is_dragging = True

    def on_separator_mouse_up(self, _event: Any) -> None:  # noqa: ANN401
        """Handle mouse up on the separator to stop dragging."""
        self.is_dragging = False
