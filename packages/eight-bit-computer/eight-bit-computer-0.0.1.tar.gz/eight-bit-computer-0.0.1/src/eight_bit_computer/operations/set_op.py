"""
The set operation.

Sets a module to a certain value.
"""

from ..language_defs import (
    INSTRUCTION_GROUPS,
    SRC_REGISTERS,
    DEST_REGISTERS,
    MODULE_CONTROL,
    FLAGS,
    instruction_byte_from_bitdefs
)
from ..operation_utils import assemble_instruction, match_and_parse_line
from ..data_structures import (
    get_arg_def_template, get_machine_code_byte_template
)


_NAME = "SET"


def gen_op_args_defs():
    """
    Generate the definitions of all possible arguments passable.

    Returns:
        list(list(dict)): All possible arguments. See
        :func:`~.get_arg_def_template` for more information.
    """

    args_defs = []
    destinations = ("ACC", "A", "B", "C", "SP")
    for dest in destinations:
        args_def = []

        arg0_def = get_arg_def_template()
        arg0_def["value_type"] = "module_name"
        arg0_def["value"] = dest
        args_def.append(arg0_def)

        arg1_def = get_arg_def_template()
        arg1_def["value_type"] = "constant"
        args_def.append(arg1_def)

        args_defs.append(args_def)

    return args_defs


def generate_microcode_templates():
    """
    Generate datatemplates for all the SET operations.

    Returns:
        list(DataTemplate): All the datatemplates that make up the
        SET operation.
    """

    data_templates = []

    op_args_defs = gen_op_args_defs()
    for op_args_def in op_args_defs:

        instruction_byte_bitdefs = generate_instruction_byte_bitdefs(
            op_args_def
        )

        flags_bitdefs = [FLAGS["ANY"]]

        control_steps = [
            [
                MODULE_CONTROL["PC"]["OUT"],
                MODULE_CONTROL["MAR"]["IN"],
            ],
            [
                MODULE_CONTROL["PC"]["COUNT"],
                MODULE_CONTROL["RAM"]["OUT"],
                MODULE_CONTROL["RAM"]["SEL_PROG_MEM"],
                MODULE_CONTROL[op_args_def[0]["value"]]["IN"],
            ],
        ]

        data_templates.extend(
            assemble_instruction(
                instruction_byte_bitdefs, flags_bitdefs, control_steps
            )
        )

    return data_templates


def generate_instruction_byte_bitdefs(op_args_def):
    """
    Generate bitdefs to specify the instruction byte for these args.

    Args:
        op_args_def (list(dict)): List of argument definitions that
            specify which particular set operation to generate
            the instruction byte bitdefs for.
    Returns:
        list(str): Bitdefs that make up the instruction byte.
    """

    return [
        INSTRUCTION_GROUPS["COPY"],
        SRC_REGISTERS["CONST"],
        DEST_REGISTERS[op_args_def[0]["value"]],
    ]


def parse_line(line):
    """
    Parse a line of assembly code to create machine code byte templates.

    If a line is not identifiably a SET assembly line, return an empty
    list instead.

    Args:
        line (str): Assembly line to be parsed.
    Returns:
        list(dict): List of instruction byte template dictionaries or an
        empty list.
    Raises:
        OperationParsingError: If the line was identifiably a
            SET operation but incorrectly specified.
    """

    match, op_args_def = match_and_parse_line(
        line, _NAME, gen_op_args_defs()
    )

    if not match:
        return []

    instruction_byte = instruction_byte_from_bitdefs(
        generate_instruction_byte_bitdefs(op_args_def)
    )

    mc_byte_0 = get_machine_code_byte_template()
    mc_byte_0["byte_type"] = "instruction"
    mc_byte_0["bitstring"] = instruction_byte

    mc_byte_1 = get_machine_code_byte_template()
    mc_byte_1["byte_type"] = "constant"
    mc_byte_1["constant"] = op_args_def[1]["value"]

    return [mc_byte_0, mc_byte_1]
