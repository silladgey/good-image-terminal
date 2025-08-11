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

    name: str = "bg"
    help_pages: tuple[str, ...] = (
        """background is a command that changes the background.

        Usage: bg color
        note: color is an rgb value
        Exemple: bg rgb(255, 100, 0)
        """,
    )

    def __call__(self, terminal: "Terminal", *args: str) -> bool:
        """changes the background color of the web page

        :param terminal: The terminal instance.
        :param args: Arguments to be passed to the command.
        :return: True if command was executed successfully.

        @author Julien
        """

        if not args:
            terminal.output_error(
                "You need to provide the color of the background to change it"
            )
            return False

        if not args[0].startswith("rgb("):
            terminal.output_error(
                "wrong argument expected format: bg rgb(number, number, number)"
            )
            return False

        # Number of expected RGB components
        RGB_COMPONENTS = 3
        if len(args) < RGB_COMPONENTS:
            terminal.output_error(
                "wrong argument expected format: bg rgb(number, number, number)"
            )
            return False
        list_args = [args[0].replace("rgb(", ""), args[1], args[2]]

        rgb = []
        for index in range(3):
            value = list_args[index].replace(",", "")
            value = value.replace(")", "")
            if not value.isdigit():
                terminal.output_error(
                    f"wrong argument expected format: bg rgb(number, number, number): {value}"
                )
                return False
            value = int(value)
            MAX_RGB_VALUE = 255
            if 0 > value > MAX_RGB_VALUE:
                terminal.output_error(
                    f"rgb value too high, max value is {MAX_RGB_VALUE}"
                )
                return False
            rgb.append(value)

        color = Color(rgb[0], rgb[1], rgb[2])

        terminal.terminal_display["style"].setProperty(
            "--terminal-background-color", f"rgb{color.rgb}"
        )
        if color.hsv[2] < 127:
            text_color = (255, 255, 255)
        else:
            text_color = (0, 0, 0)
        terminal.terminal_display["style"].setProperty(
            "--terminal-output-color", f"rgb{text_color}"
        )
        # needs to change the color of some other terminal output text but I'm going to sleep
        # @author Julien
        terminal.output_info("background-color succesfully changed")
        return True
