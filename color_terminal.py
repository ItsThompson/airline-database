from enum import Enum

# INFO: Defines possible colors for printing and inputs
class Color(Enum):
    RED = 0
    GREEN = 1
    YELLOW = 2
    PURPLE = 3
    CYAN = 4


# REF: https://www.geeksforgeeks.org/print-colors-python-terminal/
def string_color(content, color):
    out = ""
    match color:
        case Color.RED:
            out = "\033[91m{}\033[00m".format(content)
        case Color.GREEN:
            out = "\033[92m{}\033[00m".format(content)
        case Color.YELLOW:
            out = "\033[93m{}\033[00m".format(content)
        case Color.PURPLE:
            out = "\033[95m{}\033[00m".format(content)
        case Color.CYAN:
            out = "\033[96m{}\033[00m".format(content)
    return out


def print_color(content, color):
    print(string_color(content, color))


def input_color():
    out = input(string_color("> ", Color.RED))
    return out
