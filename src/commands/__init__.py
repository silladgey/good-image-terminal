from .base_command import BaseCommand
from .help import Help
from .ping import Ping
from .load_image import LoadImage

all_commands: dict[str, BaseCommand] = {
    Ping.name: Ping(),
    Help.name: Help(),
    LoadImage.name: LoadImage(),
}
