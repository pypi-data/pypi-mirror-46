"""
The COPY operation.

Copies a value from one module into another.
"""

from itertools import product

from ..language_defs import (
    INSTRUCTION_GROUPS,
    SRC_REGISTERS,
    DEST_REGISTERS,
    MODULE_CONTROL,
    FLAGS,
    instruction_byte_from_bitdefs,
)

from ..operation_utils import assemble_instruction, match_and_parse_line
from ..data_structures import (
    get_arg_def_template, get_machine_code_byte_template
)

_NAME = "COPY"


def gen_op_args_defs():
    """
    Generate the definitions of all possible arguments passable.

    Returns:
        list(list(dict)): All possible arguments. See
        :func:`~.get_arg_def_template` for more information.
    """

    args_defs = []
    sources = ("ACC", "A", "B", "C", "PC", "SP")
    destinations = ("ACC", "A", "B", "C", "SP")
    for src, dest in product(sources, destinations):
        if src != dest:
            args_def = []

            arg0_def = get_arg_def_template()
            arg0_def["value_type"] = "module_name"
            arg0_def["value"] = src
            args_def.append(arg0_def)

            arg1_def = get_arg_def_template()
            arg1_def["value_type"] = "module_name"
            arg1_def["value"] = dest
            args_def.append(arg1_def)

            args_defs.append(args_def)

    return args_defs


def generate_microcode_templates():
    """
    Generate microcode for all the COPY operations.

    Returns:
        list(DataTemplate): DataTemplates for all the COPY microcode.
    """

    data_templates = []

    op_args_defs = gen_op_args_defs()
    for op_args_def in op_args_defs:
        templates = generate_operation_templates(op_args_def)
        data_templates.extend(templates)

    return data_templates


def generate_operation_templates(op_args_def):
    """
    Create the DataTemplates to define a copy with the given args.

    Args:
        op_args_def (list(dict)): List of argument definitions that
            specify which particular copy operation to generate
            templates for.
    Returns:
        list(DataTemplate) : Datatemplates that define this copy.
    """
    instruction_byte_bitdefs = generate_instruction_byte_bitdefs(op_args_def)

    flags_bitdefs = [FLAGS["ANY"]]

    control_steps = [
        [
            MODULE_CONTROL[op_args_def[0]["value"]]["OUT"],
            MODULE_CONTROL[op_args_def[1]["value"]]["IN"],
        ]
    ]

    return assemble_instruction(
        instruction_byte_bitdefs, flags_bitdefs, control_steps
    )


def generate_instruction_byte_bitdefs(op_args_def):
    """
    Generate bitdefs to specify the instruction byte for these args.

    Args:
        op_args_def (list(dict)): List of argument definitions that
            specify which particular copy operation to generate
            the instruction byte bitdefs for.
    Returns:
        list(str): Bitdefs that make up the instruction_byte
    """

    return [
        INSTRUCTION_GROUPS["COPY"],
        SRC_REGISTERS[op_args_def[0]["value"]],
        DEST_REGISTERS[op_args_def[1]["value"]],
    ]


def parse_line(line):
    """
    Parse a line of assembly code to create machine code byte templates.

    If a line is not identifiably a COPY assembly line, return an empty
    list instead.

    Args:
        line (str): Assembly line to be parsed.
    Returns:
        list(dict): List of instruction byte template dictionaries or an
        empty list.
    """

    match, op_args_def = match_and_parse_line(
        line, _NAME, gen_op_args_defs()
    )

    if not match:
        return []

    instruction_byte = instruction_byte_from_bitdefs(
        generate_instruction_byte_bitdefs(op_args_def)
    )
    mc_byte = get_machine_code_byte_template()
    mc_byte["byte_type"] = "instruction"
    mc_byte["bitstring"] = instruction_byte

    return [mc_byte]
