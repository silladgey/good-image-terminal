from typing import TYPE_CHECKING

from commands.base_command import BaseCommand
from gui.components.terminal_gui import _TerminalOutput
from utils.color import Color

if TYPE_CHECKING:
    from terminal import Terminal


class Background(BaseCommand):
    """background command

    changes the color of the background of the web page

    @author Julien
    """

    name: str = "bg"
    help_pages: tuple[str, ...] = (
        """background is a command that changes the background

        Usage: bg color
        note: color is an rgb value
        Exemple: bg rgb(255, 100, 0)
        """,
    )

    def __call__(self, terminal: "Terminal", *args: str) -> bool:
        """Change the background color of the web page

        :param terminal: The terminal instance.
        :param args: Arguments to be passed to the command.
        :return: True if command was executed successfully.

        @author Julien
        """

        # filtering user input #
        if not args:
            terminal.output_error("You need to provide the color of the background to change it")
            return False

        if not args[0].startswith("rgb("):
            terminal.output_error("wrong argument expected format: bg rgb(number, number, number)")
            return False

        if len(args) < 3:
            terminal.output_error("wrong argument expected format: bg rgb(number, number, number)")
            return False
        list_args = [args[0].replace("rgb(", ""), args[1], args[2].replace(")", "")]


        rgb = []
        for index in range(3):

            value = list_args[index].replace(",", "")

            if not value.isdigit():
                terminal.output_error(f"wrong argument expected format: bg rgb(number, number, number): {value}")
                return False
            
            value = int(value)

            if 0 > value > 255:
                terminal.output_error("rgb value too high or to low, max value is 255, min is 0")
                return False
            
            rgb.append(value)
        # filtering user input #


        color = Color(rgb[0], rgb[1], rgb[2])


        # changes the background color of the terminal
        terminal.terminal_display["style"].setProperty("--terminal-background-color", f"rgb{color.rgb}")
        text_color = Color(255, 255, 255) if color.hsv[2] < 0.5 else Color(0, 0, 0)
        terminal.info_colour = text_color
        # changes the text color of all the users input
        terminal.terminal_display["style"].setProperty("--terminal-output-color", f"rgb{text_color.rgb}")


        # replace the color of all the outputs in the terminal history #
        old_elements = terminal.terminal_display.history._elements.copy()
        terminal.terminal_display.history.clear_history()
        for element in old_elements:

            if element.class_name == "terminal-output":
                modified_output = _TerminalOutput(element.text, "rgb" + str(text_color.rgb))
                terminal.terminal_display.history.add_history(modified_output)

            else:
                terminal.terminal_display.history.add_history(element)
        # replace the color of all the outputs in the terminal history #


        terminal.output_info("background-color succesfully changed")
        return True
