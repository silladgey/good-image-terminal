from commands.background import Background
from commands.base_command import BaseCommand
from commands.draw_circle import DrawCircle
from commands.draw_line import DrawLine
from commands.draw_pixel import DrawPixel
from commands.draw_rectangle import DrawRectangle
from commands.help import Help
from commands.image_info import ImageInfo
from commands.load_image import LoadImage
from commands.ls import Ls
from commands.ping import Ping
from commands.save_image import SaveImage
from commands.undo import Undo

all_commands: dict[str, BaseCommand] = {
    Ping.name: Ping(),
    Help.name: Help(),
    LoadImage.name: LoadImage(),
    Background.name: Background(),
    Ls.name: Ls(),
    SaveImage.name: SaveImage(),
    ImageInfo.name: ImageInfo(),
    DrawPixel.name: DrawPixel(),
    DrawRectangle.name: DrawRectangle(),
    DrawCircle.name: DrawCircle(),
    DrawLine.name: DrawLine(),
    Undo.name: Undo(),
}

image_refresh_needed: list[str] = [
    LoadImage.name,
    DrawPixel.name,
    DrawRectangle.name,
    DrawCircle.name,
    DrawLine.name,
    Undo.name,
]