""" Module that handles the evaluation of the commands and corresponding queries """
import sqlite3
import time
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import src.constants as constants
import src.utils as utils
import src.crud_interface as crud_interface

from typing import Union, List
from src.data_classes import Article
from queries.queries import QUERIES_LIST


# Global DataFrames loaded by load_tables() func
article_df = None
authored_by_df = None
has_breadcrumb_df = None
in_department_df = None
in_topic_df = None


def evaluate_command_and_query(command: str, query: str) -> None:
    """
    Calls the respective evaluation based on the command input

    :param command: str -- Command, e.g. 'query'
    :param query: str -- Corresponding query statement, e.g. 'select * from articles LIMIT 10'
    :return: None
    """
    # Set pandas options
    utils.set_pandas_display_settings()
    # Print seperator / title string
    title_str = utils.print_title_string(command, query)
    start_time = time.time()

    if command == "help":
        eval_help()

    if command == "query":
        _ = eval_query(query)

    if command == "describe database":
        eval_describe_database()

    if command == "add directory":
        eval_add_directory(query)

    if command == "remove directory":
        eval_remove_directory(query)

    if command == "lookup":
        _ = eval_lookup(query)

    if command == "example":
        _ = eval_example(query)

    if command == "plot":
        eval_plot(query)

    # Print seperator string
    duration = time.time() - start_time
    utils.print_end_string(title_str, duration)


def eval_help() -> None:
    """ Prints information about the REPL system """
    print("This is a Read-Eval-Print-Loop (REPL) system. Enter a command and a query for evaluation.\n"
          "Valid commands are:\n"
          f"{constants.COMMANDS}\n\n"
          f"Seperator token is '{constants.SEPERATOR}', e.g. use 'query $SQL' to execute SQL statements.\n"
          f"Example statements would be:\n"
          f"\t* query $SQL, e.g. query $select * from article LIMIT 10\n"
          f"\t* describe database, to get information about the tables\n"
          f"\t* add directory $DIR, e.g. add directory $data/1\n"
          f"\t* remove directory $DIR, e.g. remove directory $data/1\n"
          f"\t* lookup $KEYWORD, e.g. lookup $Covid to search for articles with 'Covid' in it\n"
          f"\t* example $[1...8], e.g. example $1 to execute first example query\n"
          f"\t* plot $SQL, e.g. plot $SELECT DATE(article.date_published), count(article.date_published) FROM article "
          f"GROUP BY DATE(article.date_published) ORDER BY DATE(article.date_published) ASC\n\n"
          f"To exit the REPL use one of the following commands:\n"
          f"{constants.QUIT_COMMANDS}")


def eval_query(query, verbose: bool = True) -> Union[None, pd.DataFrame]:
    """ Executes the SQL query and returns the results as pd.DataFrame

    :param query: str -- SQL statement to execute
    :param verbose: bool -- Whether to print the results or not
    :return: Union[None, pd.DataFrame]
    """
    try:
        with sqlite3.connect(constants.PATH_DB) as connection:
            df = pd.read_sql(query, connection)
    except pd.errors.DatabaseError:
        print(f"Invalid SQL statement! Please try again and use a valid SQL statement.")
        return None

    if verbose:
        print(df)

    return df


def eval_describe_database() -> None:
    """ Prints information about the database """

    # Load tables and store as DataFrame globally
    load_tables()

    # Get first and last day of record for information printing
    first_day = list(article_df["date_published"])[1].split("T")[0]  # Take second, since the first is an outlier
    last_day = list(article_df["date_published"])[-1].split("T")[0]

    print(f"articles.db contains 'Der Spiegel' (a german journal) articles ranging from {first_day} to {last_day}.\n"
          f"The database is split into several tables to ensure a valid relational schema.\n"
          f"articles.db consists of the following tables:\n"
          f"\t* article (primary key: id, shape: {article_df.shape} -- "
          f"Contains the following columns: {list(article_df.columns)}\n"

          f"\t* authored_by (primary key: article_id, author_name, foreign key: article_id, shape: {authored_by_df.shape} -- "
          f"Contains the following columns: {list(authored_by_df.columns)}\n"

          f"\t* has_breadcrumb (primary key: article_id, breadcrumb, foreign key: article_id, shape: {has_breadcrumb_df.shape} -- "
          f"Contains the following columns: {list(has_breadcrumb_df.columns)}\n"

          f"\t* in_department (primary key: article_id, department_name, foreign key: article_id, shape: {in_department_df.shape} -- "
          f"Contains the following columns: {list(in_department_df.columns)}\n"

          f"\t* in_topic (primary key: article_id, topic_name, foreign key: article_id, shape: {in_topic_df.shape} -- "
          f"Contains the following columns: {list(in_topic_df.columns)}\n"
          )


def eval_add_directory(query) -> None:
    """ Parsed the JSON files found in the query (dir path) and adds them to the articles.db

    :param query: str -- Directory to add Article Objects (e.g. "add directory $../UB1/data/1")
    :return: None
    """
    try:
        # Read and Parse Data
        articles: List[Article] = crud_interface.load_articles(root=query)
        print(f"Parsed {len(articles)} Articles ...")
        # Add to articles.db
        crud_interface.createMany(articles)
        print(f"Added {len(articles)} Articles to articles.db ...")
    except TypeError:
        print("Error in provided path! You must provide a directory, e.g. $data/1")


def eval_remove_directory(query) -> None:
    """ Removes the data from the given directory (query) from articles.db

    :param query: str -- Directory path
    :return: None
    """
    try:
        articles: List[Article] = crud_interface.load_articles(root=query)
        print(f"Parsed {len(articles)} Articles ...")
        crud_interface.deleteMany(articles)
        print(f"Deleted {len(articles)} Articles from articles.db ...")
    except TypeError:
        print("Error in provided path! You must provide a directory, e.g. $data/1")


def eval_lookup(query) -> Union[None, pd.DataFrame]:
    """ Searches the article.db for articles with full_text containing a keyword (query).

    :param query: str -- Query / Keyword to search for
    :return: None
    """
    KEYWORD = query
    if KEYWORD is None:
        print("Please provide a keyword, e.g. 'lookup $Covid' ...")
        return None
    else:
        SQL_STATEMENT = "SELECT article.id, article.headline_main " \
                        "FROM article " \
                        f"WHERE article.full_text LIKE '%{KEYWORD}%'"
        df = eval_query(SQL_STATEMENT)
        print(f"Found {df.shape[0]} Articles with Keyword '{KEYWORD}' ...")

        return df


def eval_example(query) -> Union[None, pd.DataFrame]:
    """ Executes the example queries from exercise 02

    :param query: str -- Number which of the 8 queries to execute
    :return: Union[None, pd.DataFrame]
    """
    try:
        query_number: int = int(query)
    except Exception as e:
        print(f"Invalid example query. Must be in [1, 8], e.g. 'example $1'")
        return None

    print(f"Executing example query #{query_number} from Exercise 02 ...")

    try:
        example_query = QUERIES_LIST[query_number]
        df = eval_query(example_query)
        return df
    except IndexError as e:
        print(f"{e}: Please use a number in [1...8]")
        return None


def eval_plot(query) -> bool:
    """ Plots the given query statement if it fulfills the given constraints

    :param query: str -- SQL statement
    :return: bool -- Whether it was successful or not
    """
    df = eval_query(query, verbose=False)
    if df is None:
        return False

    first_col_name = list(df.columns)[0]
    second_col_name = list(df.columns)[1]

    # First constraint
    if len(df.columns) != 2:
        print("SQL statement must select exactly 2 columns!")
        return False

    # Second constraint
    if not first_col_name.startswith("date"):
        print("First column must be an ISO-Timestamp!")
        return False

    # Third constraint
    if not pd.api.types.is_numeric_dtype(df[second_col_name]):
        print("Second column must be a numerical column!")
        return False

    # Convert first column to datetime if it's prefixed with 'date'
    df[first_col_name] = df[first_col_name].apply(lambda x: datetime.datetime.fromisoformat(x))

    # Plot line plot with x-axis being the time axis and y a numerical attribute
    save_str = constants.PATH_OUTPUT_DIR + f"{datetime.datetime.now()}.png"
    plt.figure(figsize=(12, 4))
    sns.lineplot(data=df, x=first_col_name, y=second_col_name)
    plt.title(f"Analysis of {second_col_name} over time", size=16, fontweight="bold")
    plt.savefig(save_str, dpi=126)
    plt.show()

    print(f"Saved figure in {constants.PATH_OUTPUT_DIR} as {save_str}")
    return True


def load_tables() -> None:
    """ Loads all tables from articles.db into the global variables """

    global article_df, authored_by_df, has_breadcrumb_df, in_department_df, in_topic_df
    article_df = eval_query(query='select * from article ORDER BY date_published ASC', verbose=0)
    authored_by_df = eval_query(query='select * from authored_by', verbose=0)
    has_breadcrumb_df = eval_query(query='select * from has_breadcrumb', verbose=0)
    in_department_df = eval_query(query='select * from in_department', verbose=0)
    in_topic_df = eval_query(query='select * from in_topic', verbose=0)
