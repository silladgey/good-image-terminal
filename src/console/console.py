class Console:
    def run_str(self, command_str: str):
        command_str = command_str.strip()
        print(command_str)


if __name__ == '__main__':
    test_console = Console()
    test_console.run_str(input())
