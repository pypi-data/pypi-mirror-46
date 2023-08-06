"""
Operations in the assembly language
"""


def get_all_operations():
    """
    Get a list of all the operations in the assembly language

    Deferring the import to the function so that importing the
    operations module doesn't mean automatically importing all the
    operations.

    Returns:
        list(module): All the modules that represent operations in the
        assembly language
    """

    from . import (
        copy_op,
        load,
        set_op,
    )

    return [
        copy_op,
        load,
        set_op,
    ]
