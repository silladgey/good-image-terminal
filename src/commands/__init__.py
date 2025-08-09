from .base_command import BaseCommand
from .help import Help
from .ping import Ping

all_commands: dict[str, BaseCommand] = {
    Ping.name: Ping(),
    Help.name: Help(),
}
