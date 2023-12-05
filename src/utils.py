import pandas as pd


def set_pandas_display_settings() -> None:
    """ Simple util function for pandas configuration for better CLI printing """
    pd.set_option('display.width', 2000)
    pd.set_option('display.max_columns', 1000)


def print_title_string(command, query) -> str:
    """ Prints and returns the title string at the beginning of the evaluation

    :param command: str
    :param query: str
    :return: title_str: str
    """
    if query is None:
        title_str = 40 * "=" + f" EVALUATING COMMAND '{command.upper()}' " + 40 * "="
    else:
        title_str = 25 * "=" + f" EVALUATING COMMAND '{command.upper()}' WITH QUERY '{query}' " + 25 * "="
    print(title_str)
    return title_str


def print_end_string(title_str: str, duration: float) -> None:
    """ Simply prints the end seperator string with the same length as the title_str

    :param title_str: str -- Title string, returned from print_title_string() func
    :param duration: float -- How many seconds the execution time took
    """
    time_str = f" EXECUTION TIME: {duration:.2f}s "
    print(int((len(title_str)-len(time_str)) / 2) * "=" + time_str + int((len(title_str)-len(time_str)) / 2) * "="+"\n")
