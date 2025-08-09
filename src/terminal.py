class Terminal:
    """Terminal manages a custom command environment.

    @author Philip
    """

    info_colour = (255, 255, 255)
    success_colour = (0, 255, 0)
    error_colour = (255, 0, 0)

    def run_str(self, command_str: str) -> bool:
        """Parse and then run the given command.

        @author Philip
        @param command_str: String of command to be executed
        @return success of command execution
        """
        command_str = command_str.strip()
        print(command_str)
        return True

    def output_info(self, output: str) -> None:
        """Output the given input to the display with `info_colour`.

        @author Philip
        @param output: Text to be printed
        @return None
        """
        print(output)

    def output_success(self, output: str) -> None:
        """Output the given input to the display with `success_colour`.

        @author Philip
        @param output: Text to be printed
        @return None
        """
        print(output)

    def output_error(self, output: str) -> None:
        """Output the given input to the display with `error_colour`.

        @author Philip
        @param output: Text to be printed
        @return None
        """
        print(output)


if __name__ == "__main__":
    test_terminal = Terminal()
    test_terminal.run_str(input())
