"""
Functionality for working with string tokens on assembly lines
"""

import re


def is_label(test_string):
    """
    Test if a string is a valid label.

    Args:
        test_string (str): The string to test
    Returns:
        bool: True if the string is a valid label, false otherwise.
    """
    match = re.match(r"@[a-zA-Z_]+\w*$", test_string)
    if match:
        return True
    else:
        return False


def is_variable(test_string):
    """
    Test if a string is a valid variable.

    Args:
        test_string (str): The string to test
    Returns:
        bool: True if the string is a valid variable, false otherwise.
    """
    match = re.match(r"\$[a-zA-Z_]+\w*$", test_string)
    if match:
        return True
    else:
        return False


def is_constant(test_string):
    if (is_label(test_string)
            or is_variable(test_string)
            or is_number(test_string)):
        return True
    else:
        return False


def is_number(test_string):
    """
    Test if a string is a valid number.

    Args:
        test_string (str): The string to test
    Returns:
        bool: True if the string is a valid number, false otherwise.
    """
    if not test_string:
        return False
    if test_string[0] == "#":
        stripped = test_string[1:]
        if not stripped:
            return False
        try:
            num = int(stripped, 0)
        except ValueError:
            return False
        return True
    else:
        return False


def number_constant_value(number_constant):
    """
    Get the value that a number constant represents.

    Args:
        number_constant (str): The constant to extract the value from.
    Returns:
        int: The value of the constant.
    """

    return int(number_constant[1:], 0)


def is_memory_index(argument):
    """
    Determine whether this argument is a memory index.

    Memory indexes can be module names or constants with a ``[`` at the start
    and a ``]`` at the end. e.g.:

    - ``[A]``
    - ``[#42]``
    - ``[$variable]``

    Args:
        argument (str): The argument being used for the assembly
            operation.
    Returns:
        bool: True if the argument is a memory index, false if not.

    """
    if (argument.startswith("[")
            and argument.endswith("]")
            and len(argument) > 2):
        return True
    else:
        return False


def represent_as_memory_index(argument):
    """
    Format the argument so it appears as a memory index.

    See :func:`~.is_memory_index` for details on what a memory index is.

    Args:
        argument (str): The argument to represent as a memory index.
    Returns:
        str: The formatted argument.
    """
    return "[{argument}]".format(argument=argument)


def extract_memory_position(argument):
    """
    Extract a memory position from a memory index argument.

    See :func:`~.is_memory_index` for details of what a memory index is.

    Args:
        argument (str): The argument to extract a memory position from.
    Returns:
        str: The location in memory being referenced.
    """

    return argument[1:-1]


def get_tokens_from_line(line):
    """
    Given a line split it into tokens and return them.

    Tokens are runs of characters separated by spaces. If there are no
    tokens return an empty list.

    Args:
        line (str): line to convert to tokens
    Returns:
        list(str): The tokens
    """

    # Does line have any content
    if not line:
        return []

    # Does the line have any content after splitting it
    line_tokens = line.split()
    if not line_tokens:
        return []

    return line_tokens