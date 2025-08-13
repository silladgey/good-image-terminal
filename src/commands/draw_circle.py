from typing import TYPE_CHECKING

from utils.color import colors, Color
from commands.base_command import BaseCommand

if TYPE_CHECKING:
    from terminal import Terminal


class DrawCircle(BaseCommand):
    """Circle drawing on PaintImage.

    @author Mira
    """

    name: str = "draw_circle"
    help_pages: tuple[str, ...] = (
        """
        Usage: draw_circle x y radius color
        or: draw_circle x y radius r g b
        
        arguments x,y: coordinate numbers
        argument radius: color name
        argument color: color name
        arguments r,g,b: red,green,blue numbers
        """,
    )

    def __call__(self, terminal: "Terminal", *args: str) -> bool:
        """Draw circle command.

        :param terminal: The terminal instance.
        :param args: Arguments to be passed to the command.
        :return: True if command was executed successfully.

        @author Mira
        """
        if len(args) == 4:
            if args[3] not in colors.keys():
                terminal.output_error("Invalid color name.")
                return False
            col = colors[args[3]]
        elif len(args) == 6:
            if not all([a.isdigit() and 0<=int(a)<256 for a in args[3:]]):
                terminal.output_error("Wrong color, please input `r g b` as numbers 0-255.")
                return False
            col = Color(int(args[3]),int(args[4]),int(args[5]))
        else:
            terminal.output_error("Bad amount of arguments, see help for options")
            return False
        size = terminal.image.img.size
        if not (args[0].isdigit() and args[1].isdigit() and 0 <= int(args[0]) < size[0] and 0 <= int(args[1]) < size[1]):
            terminal.output_error("Invalid coordinates.")
            return False
        x,y = int(args[0]), int(args[1])
        if not (args[2].isdigit()):
            terminal.output_error("Invalid radius.")
            return False
        rad = int(args[2])
        terminal.image.draw_circle(x,y,rad,col)
        terminal.output_info(f"Circle at {x}x{y} size {rad} filled with rgb{col.rgb}.")
        return True

    def predict_args(self, terminal: "Terminal", *args: str) -> str | None: # noqa: ARG002
        '''Argument predictor.'''
        match len(args):
            case 0:
                return " x y radius color"
            case 1:
                return " y radius color"
            case 2:
                return " radius color"
            case 3:
                return " color"
            case 4:
                if args[3].isdigit():
                    return " g b"
                for col in colors:
                    if col.startswith(args[2]):
                        return col
            case 5:
                return " b"
            case _:
                pass
        return ""