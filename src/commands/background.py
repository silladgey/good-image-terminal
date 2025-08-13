from typing import TYPE_CHECKING

from commands.base_command import BaseCommand
from utils.color import Color

if TYPE_CHECKING:
    from terminal import Terminal


class Background(BaseCommand):
    """background command.

    changes the color of the background of the web page

    @author Julien
    """

    RGB_COMPONENTS = 3
    MAX_RGB_VALUE = 255
    MIN_RGB_VALUE = 0
    BRIGHTNESS_THRESHOLD = 0.5

    name: str = "bg"
    help_pages: tuple[str, ...] = (
        """background is a command that changes the background.

        Usage: bg color
        note: color is an rgb value
        Exemple: bg rgb(255, 100, 0)
        """,
    )

    def __call__(self, terminal: "Terminal", *args: str, **_options: str) -> bool:
        """Change the background color of the web page.

        :param terminal: The terminal instance.
        :param args: Arguments to be passed to the command.
        :param options: Options passed to the command with optional arguments with those options.
        :return: True if command was executed successfully.

        @author Julien
        """
        # filtering user input #
        if not args:
            terminal.output_error(
                "You need to provide the color of the background to change it",
            )
            return False

        if not args[0].startswith("rgb("):
            terminal.output_error(
                "wrong argument expected format: bg rgb(number, number, number)",
            )
            return False

        if len(args) < self.RGB_COMPONENTS:
            terminal.output_error(
                "wrong argument expected format: bg rgb(number, number, number)",
            )
            return False
        list_args = [args[0].replace("rgb(", ""), args[1], args[2].replace(")", "")]

        rgb = []
        for index in range(3):
            value = list_args[index].replace(",", "")

            if not value.isdigit():
                terminal.output_error(
                    f"wrong argument expected format: bg rgb(number, number, number): {value}",
                )
                return False

            value = int(value)

            if value < self.MIN_RGB_VALUE or value > self.MAX_RGB_VALUE:
                terminal.output_error(
                    f"rgb value too high or too low, max value is {self.MAX_RGB_VALUE}, min is {self.MIN_RGB_VALUE}",
                )
                return False

            rgb.append(value)
        # filtering user input #

        color = Color(rgb[0], rgb[1], rgb[2])

        # changes the background color of the terminal
        terminal.terminal_display.background_color = f"rgb{color.rgb}"

        text_color = Color(255, 255, 255) if color.hsv[2] < self.BRIGHTNESS_THRESHOLD else Color(0, 0, 0)

        # changes the text color of all the users input
        terminal.terminal_display.output_color = f"rgb{text_color.rgb}"

        terminal.output_info("background-color succesfully changed")
        return True
