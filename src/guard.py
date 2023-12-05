""" Module that handles guard clauses for command and queries inputs """
import src.constants as constants


class Guard:

    def __init__(self, command: str, query: str):
        self.command = command
        self.query = query

    def check_input(self) -> bool:
        if not self.check_if_valid_command():
            return False

        return True

    def check_if_valid_command(self) -> bool:
        if self.command not in constants.COMMANDS:
            print(f"Unknown command '{self.command}'! Type 'help' for more information.")
            return False
        else:
            return True
