from commands import all_commands
from gui.components.terminal_gui import TerminalGui
from image import PaintImage
from utils.color import Color


class Terminal:
    """Terminal manages a custom command environment.

    @author Philip
    """

    info_colour: Color = Color(255, 255, 255)
    success_colour: Color = Color(0, 255, 0)
    error_colour: Color = Color(255, 0, 0)

    def __init__(self, image: PaintImage, display: TerminalGui) -> None:
        self.image = image

        self.terminal_display = display
        display.terminal = self

    def run_str(self, command_str: str) -> bool:
        """Parse and then run the given command.

        :param command_str: String of command to be executed
        :return: success of command execution

        @author Philip
        """
        command_str = command_str.strip()
        command, *args = command_str.split()

        if command in all_commands:
            all_commands[command](self, *args)
        else:
            self.output_error(f"`{command}` is not a valid command.")
            self.output_error("use `help` to see list of available commands`")
            return False

        return True

    def predict_command(self, command_str: str) -> str | None:
        """Predicts the command and arguments the user is typing.

        Argument handling is offloaded to commands predict_args.

        :param command_str: Currently typed text in terminal.
        :return: The full predicted command with next argument. Returns None on error.

        @author Philip
        """
        if command_str == "":
            return ""

        command, *args = command_str.split()
        if command in all_commands:
            output = command
            prediction = all_commands[command].predict_args(self, *args)
            if prediction is None:
                return None
            if prediction == "":
                return command_str
            if not prediction.startswith(" "):
                args.pop()
                prediction = " " + prediction
            if args:
                output += " " + " ".join(args)
            output += prediction
            return output

        for full_command in all_commands:
            if full_command.startswith(command):
                return full_command
        return None

    def output_info(self, output: str) -> None:
        """Output the given input to the display with `info_colour`.

        :param output: Text to be printed
        :return: None

        @authors Philip
        """
        self.terminal_display.print_terminal_output(output, self.info_colour.hex)

    def output_success(self, output: str) -> None:
        """Output the given input to the display with `success_colour`.

        :param output: Text to be printed
        :return: None

        @author Philip
        """
        self.terminal_display.print_terminal_output(output, self.success_colour.hex)

    def output_error(self, output: str) -> None:
        """Output the given input to the display with `error_colour`.

        :param output: Text to be printed
        :return: None

        @author Philip
        """
        self.terminal_display.print_terminal_output(output, self.error_colour.hex)
