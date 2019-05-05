from . import function
from . import readability


def get_checkers():
    """Get default checkers to run on code.

    :returns: List of default checkers to run.
    """
    return [function, readability]
