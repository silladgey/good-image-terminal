from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from terminal import Terminal


class BaseCommand:
    """BaseCommand is the class that all commands should inherit from.

    it contains some utility functions, but most calls should be overridden in full command implementation.

    `name` and `help_pages` should be overwritten in full command implementation.

    @author Philip
    """

    name: str = "BaseCommand"
    help_pages: tuple[str, ...] = (
        """BaseCommand is the class that all commands should inherit from.

        raises NotImplementedError when called as it and this message should never be seen.
        if you see this message in the application report how
        """,
    )

    def __call__(self, terminal: "Terminal", *args: str) -> bool:
        """Preforms the command being called using `*args`.

        This function should be overridden by subclasses.

        The subclasses implementation should handle argument handling.

        :param terminal: The terminal instance.
        :param args: Arguments passed to the command.
        :return: Was the command executed successfully?

        @author Philip
        """
        msg = "BaseCommand should not be called and should be overridden"
        raise NotImplementedError(msg)
