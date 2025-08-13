from typing import TYPE_CHECKING

from utils.color import colors, Color
from commands.base_command import BaseCommand

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

    def __call__(self, terminal: "Terminal", *args: str) -> bool:
        """Draw line command.

        :param terminal: The terminal instance.
        :param args: Arguments to be passed to the command.
        :return: True if command was executed successfully.

        @author Mira
        """
        if len(args) == 5:
            if args[4] not in colors.keys():
                terminal.output_error("Invalid color name.")
                return False
            col = colors[args[4]]
        elif len(args) == 7:
            if not all([a.isdigit() and 0 <= int(a) < 256 for a in args[4:]]):
                terminal.output_error("Wrong color, please input `r g b` as numbers 0-255.")
                return False
            col = Color(int(args[4]), int(args[5]), int(args[6]))
        else:
            terminal.output_error("Bad amount of arguments, see help for options.")
            return False

        size = terminal.image.img.size
        if not (args[0].isdigit() and args[1].isdigit() and 0 <= int(args[0]) < size[0] and 0 <= int(args[1]) < size[1]):
            terminal.output_error("Invalid starting coordinates.")
            return False
        if not (args[2].isdigit() and args[3].isdigit() and 0 <= int(args[2]) < size[0] and 0 <= int(args[3]) < size[1]):
            terminal.output_error("Invalid ending coordinates.")
            return False

        x1, y1 = int(args[0]), int(args[1])
        x2, y2 = int(args[2]), int(args[3])

        terminal.image.draw_line(x1, y1, x2, y2, col)
        terminal.output_info(f"line from {x1}x{y1} to {x2}x{y2} with rgb{col.rgb}")
        return True

    def predict_args(self, terminal: "Terminal", *args: str) -> str | None:  # noqa: ARG002
        """Argument predictor."""
        match len(args):
            case 0:
                return " x1 y1 x2 y2 color"
            case 1:
                return " y1 x2 y2 color"
            case 2:
                return " x2 y2 color"
            case 3:
                return " y2 color"
            case 4:
                return " color"
            case 5:
                if args[4].isdigit():
                    return " g b"
                for col in colors:
                    if col.startswith(args[4]):
                        return col
            case 6:
                return " b"
            case _:
                pass
        return ""
