from typing import TYPE_CHECKING

from utils.color import colors, Color
from commands.base_command import BaseCommand

if TYPE_CHECKING:
    from terminal import Terminal


class DrawRectangle(BaseCommand):
    """Rectangle drawing on PaintImage.

    @author Mira
    """

    name: str = "draw_rectangle"
    help_pages: tuple[str, ...] = (
        """
        Usage: draw_rectangle x y width height color
        or: draw_rectangle x y width height r g b
        
        arguments x,y: coordinate numbers
        arguments width,height: width and height of the rectangle
        argument color: color name
        arguments r,g,b: red,green,blue numbers
        """,
    )

    def __call__(self, terminal: "Terminal", *args: str) -> bool:
        """Draw rectangle command.

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
            if not all([a.isdigit() and 0<=int(a)<256 for a in args[4:]]):
                terminal.output_error("Wrong color, please input `r g b` as numbers 0-255.")
                return False
            col = Color(int(args[4]),int(args[5]),int(args[6]))
        else:
            terminal.output_error("Bad amount of arguments, see help for options")
            return False
        size = terminal.image.img.size
        if not (args[0].isdigit() and args[1].isdigit() and 0 <= int(args[0]) < size[0] and 0 <= int(args[1]) < size[1]):
            terminal.output_error("Invalid coordinates.")
            return False
        x,y = int(args[0]), int(args[1])
        if not (args[2].isdigit() and args[3].isdigit()):
            terminal.output_error("Invalid size.")
            return False
        w,h = int(args[2]),int(args[3])
        terminal.image.fill_rect(x,y,w,h,col)
        terminal.output_info(f"rectangle at {x}x{y} size {w}x{h} filled with rgb{col.rgb}")
        return True

    def predict_args(self, terminal: "Terminal", *args: str) -> str | None: # noqa: ARG002
        '''Argument predictor.'''
        match len(args):
            case 0:
                return " x y width height color"
            case 1:
                return " y width height color"
            case 2:
                return " width height color"
            case 3:
                return " height color"
            case 4:
                return " color"
            case 5:
                if args[4].isdigit():
                    return " g b"
                for col in colors:
                    if col.startswith(args[2]):
                        return col
            case 6:
                return " b"
            case _:
                pass
        return ""