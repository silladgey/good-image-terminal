from typing import TYPE_CHECKING

from commands.base_command import BaseCommand
from utils.color import Color, colors

if TYPE_CHECKING:
    from terminal import Terminal

REQUIRED_NUMBER_ARGS = 3


class DrawCircle(BaseCommand):
    """Circle drawing on PaintImage.

    @author Mira
    """

    name: str = "draw_circle"
    help_pages: tuple[str, ...] = (
        """
        Usage: draw_circle x y radius
        or: draw_circle x y radius

        arguments x,y: coordinate numbers
        argument radius: color name
        """,
    )
    known_options = ("fg", "bg")

    def __call__(self, terminal: "Terminal", *args: str, **options: str | Color) -> bool:
        """Draw circle command.

        :param terminal: The terminal instance.
        :param args: Arguments to be passed to the command.
        :param options: Options passed to the command with optional arguments with those options.
        :return: True if command was executed successfully.

        @author Mira
        """
        if len(args) != REQUIRED_NUMBER_ARGS:
            terminal.output_error("Bad amount of arguments, see help for options")
            return False

        size = terminal.image.img.size
        if not (
            args[0].isdigit() and args[1].isdigit() and 0 <= int(args[0]) < size[0] and 0 <= int(args[1]) < size[1]
        ):
            terminal.output_error("Invalid coordinates.")
            return False
        x, y = int(args[0]), int(args[1])

        if not (args[2].isdigit()):
            terminal.output_error("Invalid radius.")
            return False
        rad = int(args[2])
        if rad < 0:
            terminal.output_error("Radius cannot be negative.")
            return False

        terminal.image.draw_circle(x, y, rad, options["fg"])
        terminal.output_info(f"Circle at {x}x{y} size {rad} filled with rgb{options['fg'].rgba}.")
        return True

    def predict_args(self, _terminal: "Terminal", *args: str, **_options: str | Color) -> str | None:
        """Argument predictor."""
        result = ""
        match len(args):
            case 0:
                result = " x y radius color"
            case 1:
                result = " y radius color"
            case 2:
                result = " radius color"
            case 3:
                result = " color"
            case 4:
                for col in colors:
                    if col.startswith(args[2]):
                        result = col
                if args[3].isdigit():
                    result = " g b"
            case 5:
                result = " b"
            case _:
                pass
        return result
