from .base_command import BaseCommand
from .help import Help

all_commands: dict[str, BaseCommand] = {
    Help.name: Help(),
}
