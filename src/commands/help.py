from src import commands
from src.commands import BaseCommand
from src.terminal import Terminal


class Help(BaseCommand):
    """Help is a command that displays the help documentation of the command given.

    @author Philip
    """

    name = "help"
    help_pages = (
        """help is a command that displays the help documentation of the command given.

        Usage: help command integer

        The help documentation may also contain multiple pages so it can either be call multiple times
        with the same arguments to get the next page or be called with the page number you are looking for
        """,
    )

    def __call__(self, terminal: Terminal, *args: str) -> bool:
        """Pushes the text present in the help_pages of each command.

        @author Philip
        @param terminal: The terminal instance.
        @param args: Arguments to be passed to the command.
        @return True if command was executed successfully.
        """
        page = 1
        if len(args) == 0:
            terminal.output_info("Available commands: ")
            terminal.output_info(", ".join(sorted(commands.all_commands.keys())))
            terminal.output_info("for more information on a command use `help command`.")
            return True
        if len(args) >= 3:
            terminal.output_error("too many arguments.")
            return False
        if len(args) == 2:
            if not args[1].isdigit():
                terminal.output_error("second argument must be an integer.")
            page = args[1]

        if args[0] not in commands.all_commands:
            terminal.output_error(f"`{args[0]}` is an Unknown command.")
            terminal.output_error("use `help` to see a list of available commands")
            return False

        command = commands.all_commands[args[0]]

        if page > len(command.help_pages):
            terminal.output_error(f"`{args[0]}` is not a valid page.")
            return False

        terminal.output_info(f"help for `{args[0]}`\t\t page: {page}/{len(command.help_pages)}")
        terminal.output_info(command.help_pages[page - 1])

        return True
