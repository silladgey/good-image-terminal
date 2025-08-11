from commands.base_command import BaseCommand
from commands.help import Help
from commands.load_image import LoadImage
from commands.ping import Ping
from commands.background import Background

all_commands: dict[str, BaseCommand] = {
    Ping.name: Ping(),
    Help.name: Help(),
    LoadImage.name: LoadImage(),
    Background.name: Background(),
}
