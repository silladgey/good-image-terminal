from typing import TYPE_CHECKING

from commands.base_command import BaseCommand
from utils.color import Color, colors

if TYPE_CHECKING:
    from terminal import Terminal


class DrawLine(BaseCommand):
    """Line drawing on PaintImage.

    @author Mira
    """

    name: str = "draw_line"
    help_pages: tuple[str, ...] = (
        """
        Usage: draw_line x1 y1 x2 y2 color
        or: draw_line x1 y1 x2 y2 r g b

        arguments x1,y1: starting coordinates
        arguments x2,y2: ending coordinates
        argument color: color name
        arguments r,g,b: red,green,blue numbers
        """,
    )

    def __call__(self, terminal: "Terminal", *args: str, **_options: str) -> bool:
        """Draw line command.

        :param terminal: The terminal instance.
        :param args: Arguments to be passed to the command.
        :param options: Options passed to the command with optional arguments with those options.
        :return: True if command was executed successfully.

        @author Mira
        """
        if len(args) == 5:  # noqa: PLR2004
            if args[4] not in colors:
                terminal.output_error("Invalid color name.")
                return False
            col = colors[args[4]]
        elif len(args) == 7:  # noqa: PLR2004
            if not all([a.isdigit() and 0 <= int(a) < 256 for a in args[4:]]):  # noqa: PLR2004, C419
                terminal.output_error("Wrong color, please input `r g b` as numbers 0-255.")
                return False
            col = Color(int(args[4]), int(args[5]), int(args[6]))
        else:
            terminal.output_error("Bad amount of arguments, see help for options.")
            return False

        size = terminal.image.img.size
        if not (
            args[0].isdigit() and args[1].isdigit() and 0 <= int(args[0]) < size[0] and 0 <= int(args[1]) < size[1]
        ):
            terminal.output_error("Invalid starting coordinates.")
            return False
        if not (
            args[2].isdigit() and args[3].isdigit() and 0 <= int(args[2]) < size[0] and 0 <= int(args[3]) < size[1]
        ):
            terminal.output_error("Invalid ending coordinates.")
            return False

        x1, y1 = int(args[0]), int(args[1])
        x2, y2 = int(args[2]), int(args[3])

        terminal.image.draw_line(x1, y1, x2, y2, col)
        terminal.output_info(f"line from {x1}x{y1} to {x2}x{y2} with rgb{col.rgb}")
        return True

    def predict_args(self, _terminal: "Terminal", *args: str, **_options: str) -> str | None:  # noqa: C901
        """Argument predictor."""
        result = ""
        match len(args):
            case 0:
                result = " x1 y1 x2 y2 color"
            case 1:
                result = " y1 x2 y2 color"
            case 2:
                result = " x2 y2 color"
            case 3:
                result = " y2 color"
            case 4:
                result = " color"
            case 5:
                for col in colors:
                    if col.startswith(args[4]):
                        result = col
                if args[4].isdigit():
                    result = " g b"
            case 6:
                result = " b"
            case _:
                pass
        return result
