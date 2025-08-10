from .base_command import BaseCommand
from .help import Help
from .load_image import LoadImage
from .ping import Ping

all_commands: dict[str, BaseCommand] = {
    Ping.name: Ping(),
    Help.name: Help(),
    LoadImage.name: LoadImage(),
}
