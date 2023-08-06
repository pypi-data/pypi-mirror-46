"""Coloring to string functions"""


def black(string):
    """foreground color to black"""

    return '\033[30m' + string + '\033[0m'


def red(string):
    """foreground color to red"""

    return '\033[31m' + string + '\033[0m'


def green(string):
    """foreground color to green"""

    return '\033[32m' + string + '\033[0m'


def yellow(string):
    """foreground color to yellow"""

    return '\033[33m' + string + '\033[0m'


def blue(string):
    """foreground color to blue"""

    return '\033[34m' + string + '\033[0m'


def magenta(string):
    """foreground color to magenta"""

    return '\033[35m' + string + '\033[0m'


def cyan(string):
    """foreground color to cyan"""

    return '\033[36m' + string + '\033[0m'


def white(string):
    """foreground color to white"""

    return '\033[37m' + string + '\033[0m'


def black_b(string):
    """background color to black"""

    return '\033[40m' + string + '\033[0m'


def red_b(string):
    """background color to red"""

    return '\033[41m' + string + '\033[0m'


def green_b(string):
    """background color to green"""

    return '\033[42m' + string + '\033[0m'


def yellow_b(string):
    """background color to yellow"""

    return '\033[43m' + string + '\033[0m'


def blue_b(string):
    """background color to blue"""

    return '\033[44m' + string + '\033[0m'


def magenta_b(string):
    """background color to magenta"""

    return '\033[45m' + string + '\033[0m'


def cyan_b(string):
    """background color to cyan"""

    return '\033[46m' + string + '\033[0m'


def white_b(string):
    """background color to white"""

    return '\033[47m' + string + '\033[0m'
