import commands
from gui.components.terminal_gui import TerminalGui
from image import PaintImage


class Terminal:
    """Terminal manages a custom command environment.

    @author Philip
    """

    info_colour = (255, 255, 255)
    success_colour = (0, 255, 0)
    error_colour = (255, 0, 0)

    def __init__(self, image: PaintImage) -> None:
        self.image = image
        self.terminal_display = None

    def run_str(self, command_str: str) -> bool:
        """Parse and then run the given command.

        :param command_str: String of command to be executed
        :return: success of command execution
        
        @author Philip
        """
        command_str = command_str.strip()
        command, *args = command_str.split()

        if command in commands.all_commands:
            commands.all_commands[command](self, *args)
        else:
            self.output_error(f"`{command_str}` is not a valid command.")
            self.output_error("use `help` to see list of available commands`")
            return False

        return True

    def output_info(self, output: str) -> None:
        """Output the given input to the display with `info_colour`.

        :param output: Text to be printed
        :return: None
        
        @authors Philip
        """
        print(output)

    def output_success(self, output: str) -> None:
        """Output the given input to the display with `success_colour`.

        :param output: Text to be printed
        :return: None
        
        @author Philip
        """
        print(output)

    def output_error(self, output: str) -> None:
        """Output the given input to the display with `error_colour`.

        :param output: Text to be printed
        :return: None
        
        @author Philip
        """
        print(output)


if __name__ == "__main__":
    test_terminal = Terminal()
    while test_terminal.run_str(input("> ")):
        pass
