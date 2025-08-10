from commands import BaseCommand
from terminal import Terminal


class LoadImage(BaseCommand):
    """Help is a command that displays the help documentation of the command given.

    @author Mira
    """

    name: str = "load_image"
    help_pages: tuple[str, ...] = (
        """help is a command that displays the help documentation of the command given.

        Usage: load_image <image.name>

        Default image loading: load_image default
        """,
    )

    def __call__(self, terminal: Terminal, *args: str) -> bool:
        """Loads an image to program memory.

        :param terminal: The terminal instance.
        :param args: Arguments to be passed to the command.
        :return: True if command was executed successfully.

        @author Philip
        """
        if not args:
            terminal.output_error("You need to provide an image name see help for more info.")
            return False
        if args[0] == "default":
            terminal.image.load()
        elif terminal.image.load(args[0]):
            terminal.output_error("Image not found.")
            return False
        return True
