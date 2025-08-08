class Terminal:
    """Terminal manages a custom command environment.

    @author
    """

    def run_str(self, command_str: str) -> bool:
        """Parse and then run the given command.

        @author Philip
        @param command_str: String of command to be executed
        @return success of command execution
        """
        command_str = command_str.strip()
        print(command_str)
        return True


if __name__ == "__main__":
    test_terminal = Terminal()
    test_terminal.run_str(input())
