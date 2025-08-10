from typing import TYPE_CHECKING

import commands
from commands.base_command import BaseCommand

if TYPE_CHECKING:
    from terminal import Terminal


class Help(BaseCommand):
    """Help is a command that displays the help documentation of the command given.

    @author Philip
    """

    name: str = "help"
    help_pages: tuple[str, ...] = (
        """help is a command that displays the help documentation of the command given.

        Usage: help command integer

        The help documentation may also contain multiple pages so it can either be call multiple times
        with the same arguments to get the next page or be called with the page number you are looking for
        """,
    )

    def __call__(self, terminal: "Terminal", *args: str) -> bool:
        """Pushes the text present in the help_pages of each command.

        :param terminal: The terminal instance.
        :param args: Arguments to be passed to the command.
        :return: True if command was executed successfully.

        @author Philip
        """
        page = 1
        match len(args):
            case 0:
                terminal.output_info("Available commands: ")
                terminal.output_info(", ".join(sorted(commands.all_commands.keys())))
                terminal.output_info("for more information on a command use `help command`.")
                return True
            case 1:
                page = 1
            case 2:
                if not args[1].isdigit():
                    terminal.output_error("second argument must be an integer.")
                page = args[1]
            case _:
                terminal.output_error("too many arguments.")
                return False

        if args[0] not in commands.all_commands:
            terminal.output_error(f"`{args[0]}` is an Unknown command.")
            terminal.output_error("use `help` to see a list of available commands")
            return False

        command = commands.all_commands[args[0]]

        if page > len(command.help_pages):
            terminal.output_error(f"`{args[0]}` is not a valid page.")
            return False

        terminal.output_info(f"help for `{args[0]}`\t\t page: {page}/{len(command.help_pages)}")
        for line in command.help_pages[page - 1].split("\n"):
            terminal.output_info(line.strip())

        return True
