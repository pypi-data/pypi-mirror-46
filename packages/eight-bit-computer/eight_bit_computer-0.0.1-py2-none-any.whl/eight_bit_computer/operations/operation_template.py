"""
Example and explanation of required functions for an operation module.
"""

from ..language_defs import (
    INSTRUCTION_GROUPS,
    SRC_REGISTERS,
    DEST_REGISTERS,
    MODULE_CONTROL,
    FLAGS,
)
from ..operation_utils import assemble_instruction, match_and_parse_line
from ..data_structures import (
    get_arg_def_template, get_machine_code_byte_template
)

_NAME = "OPERATION_TEMPLATE"


def generate_microcode_templates():
    """
    Generate datatemplates for all the OPERATION_TEMPLATE operations.

    Returns:
        list(DataTemplate): All the datatemplates that make up the
        OPERATION_TEMPLATE operation.
    """
    pass


def parse_line(line):
    """
    Parse a line of assembly code to create machine code byte templates.

    If a line is not identifiably a OPERATION_TEMPLATE assembly line,
    return an empty list instead.

    Args:
        line (str): Assembly line to be parsed.
    Returns:
        list(dict): List of instruction byte template dictionaries or an
        empty list.
    Raises:
        OperationParsingError: If the line was identifiably a
            OPERATION_TEMPLATE operation but incorrectly specified.
    """
    pass
