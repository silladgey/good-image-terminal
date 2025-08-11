from typing import TYPE_CHECKING

from commands.base_command import BaseCommand

if TYPE_CHECKING:
    from terminal import Terminal


class LoadImage(BaseCommand):
    """load_image is a command that loads the given image.

    @author Mira
    """

    name: str = "load_image"
    help_pages: tuple[str, ...] = (
        """
        Usage: load_image <image.name>

        Default image loading: load_image default
        """,
    )

    def __call__(self, terminal: "Terminal", *args: str) -> bool:
        """Load an image to program memory.

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
