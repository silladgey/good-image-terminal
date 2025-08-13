from typing import TYPE_CHECKING

from utils.color import colors, Color
from commands.base_command import BaseCommand

if TYPE_CHECKING:
    from terminal import Terminal


class DrawPixel(BaseCommand):
    """Pixel drawing on PaintImage.

    @author Mira
    """

    name: str = "draw_pixel"
    help_pages: tuple[str, ...] = (
        """
        Usage: draw_pixel x y color
        or: draw_pixel x y r g b
        
        arguments x,y: coordinate numbers
        argument color: color name
        arguments r,g,b: red,green,blue numbers
        """,
    )

    def __call__(self, terminal: "Terminal", *args: str) -> bool:
        """Draw pixel command.

        :param terminal: The terminal instance.
        :param args: Arguments to be passed to the command.
        :return: True if command was executed successfully.

        @author Mira
        """
        if len(args) == 3:
            if args[2] not in colors.keys():
                terminal.output_error("Invalid color name.")
                return False
            col = colors[args[2]]
        elif len(args) == 5:
            if not all([a.isdigit() and 0<=int(a)<256 for a in args[2:]]):
                terminal.output_error("Wrong color, please input `r g b` as numbers 0-255.")
                return False
            col = Color(int(args[2]),int(args[3]),int(args[4]))
        else:
            terminal.output_error("Bad amount of arguments, see help for options")
            return False
        size = terminal.image.img.size
        if not (args[0].isdigit() and args[1].isdigit() and 0 <= int(args[0]) < size[0] and 0 <= int(args[1]) < size[1]):
            terminal.output_error("Invalid coordinates.")
            return False
        x,y = int(args[0]), int(args[1])
        terminal.image.set_pixel(x,y,col)
        terminal.output_info(f"Pixel at {x}x{y} filled with rgb{col.rgb}.")
        return True

    def predict_args(self, terminal: "Terminal", *args: str) -> str | None: # noqa: ARG002
        '''Argument predictor.'''
        match len(args):
            case 0:
                return " x y color"
            case 1:
                return " y color"
            case 2:
                return " color"
            case 3:
                if args[2].isdigit():
                    return " g b"
                for col in colors:
                    if col.startswith(args[2]):
                        return col
            case 4:
                return " b"
            case _:
                pass
        return ""