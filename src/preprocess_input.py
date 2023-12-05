""" Module that handles the preprocessing of the raw input string """


class Preprocessor:
    """
    Class to preprocess input string from the user in the REPL and return command and query
    """

    def __init__(self, user_input: str):
        """
        :param user_input: str -- Raw user input
        """
        self.user_input = user_input
        self.command = None
        self.query = None

    def preprocess_and_return_input(self) -> tuple[str, str]:
        """ Runs the preporcessing pipeline """
        self.to_lower_str()
        self.split_command_query()
        self.remove_whitestrips_cmd()
        return self.command, self.query

    def to_lower_str(self):
        """ Returns the string set to lower string """
        self.user_input = self.user_input.lower()

    def split_command_query(self):
        """ Splits the query based on the separator token """
        try:
            command, query = self.user_input.split("$")
            self.command = command
            self.query = query
        except ValueError as e:
            self.command = self.user_input

    def remove_whitestrips_cmd(self):
        """ Strips white strips from the command """
        self.command = self.command.strip()
