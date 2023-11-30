import sqlite3
import os
from color_terminal import Color, input_color, print_color
from enum import Enum
from datetime import datetime

database = "airline_database.db"


class CustomException(Exception):
    """ Custom Exception With WARN, ERROR signals"""

    def __init__(self, sign, message):
        self.sign = sign
        self.message = message

        match sign:
            case "WARN":
                prefix = "⚠️ WARN"
            case "ERROR":
                prefix = "⛔ ERROR"
            case _:
                prefix = ""

        super().__init__(f"{prefix}: {message}")


class User(Enum):
    PASSENGER = 0
    EMPLOYEE = 1


# NOTE: SQL Handlers
def execute_from_file(sql_file):
    conn = sqlite3.connect(database)
    curs = conn.cursor()

    try:
        with open(sql_file, "r") as f:
            sql_statements = f.read()
    except OSError:
        conn.commit()
        conn.close()
        raise CustomException("ERROR", sql_file + " was not found")

    curs.executescript(sql_statements)
    conn.commit()
    conn.close()


def select_query(query, args=None):
    conn = sqlite3.connect(database)
    curs = conn.cursor()

    if args is None:
        curs.execute(query)
    else:
        curs.execute(query, args)

    records = curs.fetchall()
    conn.close()
    return records


def commit_query(query, args=None):
    conn = sqlite3.connect(database)
    curs = conn.cursor()

    if args is None:
        curs.execute(query)
    else:
        curs.execute(query, args)

    new_row_id = curs.lastrowid

    conn.commit()
    conn.close()
    return new_row_id


# NOTE: Input validators
def int_input_validation(string, minimum, maximum, possible_choices=[], first_time=True):
    if first_time:
        print(string)
        user_input = input_color()
    else:
        user_input = input_color()

    try:
        user_int = int(user_input)

        if possible_choices == []:
            if minimum <= user_int <= maximum:
                return user_int
        else:
            if user_int in possible_choices:
                return user_int
        return int_input_validation(string, minimum, maximum, possible_choices, False)
    except ValueError:
        return int_input_validation(string, minimum, maximum, possible_choices, False)


def string_input_validation(string, minimum, maximum, possible_choices=[], first_time=True):
    if first_time:
        print(string)
        user_input = input_color()
    else:
        user_input = input_color()

    if not user_input:
        return ''

    # User inputed string
    user_str = str(user_input)
    if possible_choices == []:
        if minimum <= len(user_str) <= maximum:
            return user_str
    else:
        if user_str in possible_choices:
            return user_str

    return string_input_validation(string, minimum, maximum, possible_choices, False)


# NOTE: Formatting
def option_output(string, user=None):
    os.system('clear')
    match user:
        case User.PASSENGER:
            print_color("--Thompson Airline Customer Terminal--", Color.YELLOW)
        case User.EMPLOYEE:
            print_color("--Thompson Airline Internal Terminal--", Color.RED)
        case _:
            pass

    print("✔️ You Selected ", end='')
    print_color(string, Color.CYAN)
    print_color("⚙️ Loading " + string + " Data\n", Color.CYAN)


def iso8601_to_datetime(string):
    datetime_object = datetime.fromisoformat(string)
    formatted_string = datetime_object.strftime("%Y-%m-%d %H:%M")
    return formatted_string


def string_to_iso8601_time(string):
    try:
        string = datetime.strptime(string, "%Y-%m-%d %H:%M")
        iso8601_format = string.strftime("%Y-%m-%dT%H:%M:00+00:00")
    except ValueError:
        return (False, '')
    return (True, iso8601_format)


def string_to_iso8601_date(string):
    try:
        string = datetime.strptime(string, "%Y-%m-%d")
        iso8601_format = string.strftime("%Y-%m-%d")
    except ValueError:
        return (False, '')
    return (True, iso8601_format)


# NOTE: ISO8601 Helper Functions
def get_month(date_string):
    try:
        date_object = datetime.strptime(date_string, "%Y-%m-%d")
        return date_object.month
    except ValueError:
        return None


def get_week(date_string):
    try:
        date_object = datetime.strptime(date_string, "%Y-%m-%d")
        return date_object.isocalendar()[1]
    except ValueError:
        return None


# NOTE: Misc
def is_between_iso8601(date_time, start_datetime, end_datetime):
    if start_datetime <= date_time <= end_datetime:
        return True
    else:
        return False


def yes_no_prompt(prompt):
    user_input = string_input_validation(prompt, 1, 1)

    match user_input:
        case "y":
            return True
        case "n":
            return False


def return_to_main():
    prompt = """
Return to Main Screen? (y/n):"""
    if yes_no_prompt(prompt):
        return
    else:
        quit_terminal()

def quit_terminal():
    print_color("👋 Shutting Down, see you next time!", Color.CYAN)
    exit()
