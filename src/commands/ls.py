from pathlib import Path

from typing import TYPE_CHECKING

from commands.base_command import BaseCommand

if TYPE_CHECKING:
    from terminal import Terminal

IMAGES_PATH = Path(__file__).parent.parent.resolve() / "images"

class Ls(BaseCommand):
    """Listing of image directory.

    @author Mira
    """

    name: str = "ls"
    help_pages: tuple[str, ...] = (
        """
        Usage: ls
        
        Lists the directory of images.
        Does not need any arguments.
        """,
    )

    def __call__(self, terminal: "Terminal", *args: str) -> bool:
        """list all image files.

        :param terminal: The terminal instance.
        :param args: Arguments to be passed to the command.
        :return: True if command was executed successfully.

        @author Mira
        """
        if args: terminal.output_error("No arguments needed")
        terminal.output_info("Files: "+ " ".join([path.name for path in IMAGES_PATH.iterdir() if path.is_file()]))
        return True
        # +str(len(path.read_bytes()))

    def predict_args(self, terminal: "Terminal", *args: str) -> str | None: # noqa: ARG002
        '''Argument predictor.'''
        return ""