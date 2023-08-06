"""
Custom exceptions used in this project.
"""


class EightBitComputerError(Exception):
    """
    Base class for exceptions in the computer
    """
    pass


class OperationParsingError(EightBitComputerError):
    """
    Raised when parsing an operation fails.

    E.g. An incorrect argument is used with the LOAD operation.
    """
    pass


class LineProcessingError(EightBitComputerError):
    """
    Raised when processing a line fails.

    E.g. The line was not a constant declaration and no operations
    matched.
    """
    pass


class AssemblyError(EightBitComputerError):
    """
    Raised when the assembly could not be converted to machine code.
    """
    pass
