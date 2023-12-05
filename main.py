import src.evaluation as evaluation
import src.constants as constants
import src.crud_interface as crud

from src.preprocess_input import Preprocessor
from src.guard import Guard


def main():
    """ Main Pipeline: Runs the REPL system and preprocesses and guards the user input """

    # Create Database if it not exists yet
    crud.create_database()

    run = True
    # REPL
    while run:
        # R: Read the input
        x: str = input(">> ")

        # Exit REPL if input is one of the QUIT_COMMANDS
        if x in constants.QUIT_COMMANDS:
            break

        # Call pipeline to preprocess input string x and get command and query (split at seperator token)
        command, query = Preprocessor(user_input=x).preprocess_and_return_input()

        # Check for valid inputs. Skip current loop if any guard clause returns False
        guard = Guard(command, query)
        if not guard.check_input():
            continue

        # E+P: Evaluate based on command and query and print results
        evaluation.evaluate_command_and_query(command, query)


def main_crud_interface():
    """ Only relevant to test / check Task 2 """

    # Create Database if it not exists yet
    crud.create_database()

    # Do CRUD Operations with a Test Sample with the following ID
    ID_TO_SEARCH: str = "d9def405-3c1d-49c4-913a-c743ffd9691d"
    article = crud.read(ID_TO_SEARCH)
    print(article.headline.main)


if __name__ == '__main__':
    main()
    # main_crud_interface()
