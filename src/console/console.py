class Console:
    """Console manages a custom command environment."""

    def run_str(self, command_str: str) -> bool:
        """Parse and then run the given command.

        :param command_str: String of command to be executed
        :return: success of command execution
        """
        command_str = command_str.strip()
        print(command_str)
        return True


if __name__ == "__main__":
    test_console = Console()
    test_console.run_str(input())
