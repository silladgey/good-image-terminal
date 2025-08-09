from src.commands import BaseCommand
from src.terminal import Terminal


class Ping(BaseCommand):
    """Test ping command.

    Just echos pong to terminal

    @author Philip
    """

    name: str = "ping"
    help_pages: tuple[str, ...] = (
        """Pong!!!
        """,
    )

    def __call__(self, terminal: Terminal, *args: str) -> bool:
        """Print pong to terminal.

        @author Philip
        @param terminal: The terminal instance.
        @param args: Arguments to be passed to the command.
        @return True if command was executed successfully.
        """
        terminal.output_success("pong" + f": {', '.join(args)}" if args else "")
        return True
