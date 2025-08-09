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

    def __call__(self, terminal: Terminal, *args: list[str]) -> bool:
        """Pushes the text present in the help_pages of each command.

        @author Philip
        @param terminal: The terminal instance.
        @param args: Arguments to be passed to the command.
        @return True if command was executed successfully.
        """

        terminal.output_info(f"help command ran with given arguments: {args}")
        return True
