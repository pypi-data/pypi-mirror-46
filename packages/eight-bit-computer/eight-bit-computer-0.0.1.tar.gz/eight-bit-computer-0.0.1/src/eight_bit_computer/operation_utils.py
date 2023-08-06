"""
Common functions for operations.
"""

import re
from copy import deepcopy

from .data_structures import DataTemplate
from .exceptions import OperationParsingError
from .language_defs import MODULE_CONTROL, STEPS
from . import token_utils
from . import bitdef


def assemble_instruction(instruction_bitdefs, flags_bitdefs, control_steps):
    """
    Create templates for all steps to form a complete instruction.

    Args:
        instruction_bitdefs (list(str)): List of the bitdefs that make
            up the instruction byte.
        flags_bitdefs: list(str): List of the bitdefs that make up the
            flags for this instruction.
        control_steps: list(list(str): List of list of bitdefs that
            make up the control signals for each step.
    Returns:
        list(DataTemplate): All the steps for this instruction.
    Raises:
        ValueError: If too many steps were provided.
    """

    num_steps = len(control_steps)
    if num_steps > 6:
        msg = (
            "{num_steps} control steps were passed, "
            "the maxiumum is 6.".format(num_steps=num_steps)
        )
        raise ValueError(msg)

    templates = []

    instruction_bitdef = bitdef.merge(instruction_bitdefs)
    flags_bitdef = bitdef.merge(flags_bitdefs)

    for index, current_step_controls in enumerate(control_steps, start=2):
        step_bitdef = STEPS[index]

        address_bitdef = bitdef.merge(
            [
                instruction_bitdef,
                flags_bitdef,
                step_bitdef
            ]
        )

        # If this is the last step, add a step reset
        if index == num_steps + 1:
            current_step_controls.append(MODULE_CONTROL["CU"]["STEP_RESET"])

        control_bitdef = bitdef.merge(current_step_controls)
        control_bitdef = bitdef.fill(control_bitdef, "0")

        template = DataTemplate(
            address_range=address_bitdef, data=control_bitdef
        )

        templates.append(template)

    return templates


def add_quotes_to_strings(strings):
    """
    Add double quotes strings in a list then join with commas.

    Args:
        strings (list(str)): List of strings to add parentheses to.
    Returns:
        str: The strings with quotes added and joined with commas.
    """
    quote_strings = []
    for _string in strings:
        quote_strings.append("\"{string}\"".format(string=_string))
    pretty_strings = ", ".join(quote_strings)
    return pretty_strings


def match_and_parse_line(line, opcode, op_args_defs=None):
    """
    Examine assembly code to see if it is valid and parse the arguments.

    This is a common function used by most of the assembly operations.

    Args:
        line (str): The line of assembly code.
        opcode (str): The opcode this line is being tested to match.
        op_args_defs (list(list(dict)), optional): Data structure that
            defines the different combinations of arguments. See
            :func:`~.get_arg_def_template` for more details.

    Returns:
        (bool, list(dict)): Whether or not the line matched, and if it
        did, the parsed arguments.

    Raises:
        OperationParsingError: If multiple op_args defs matched. Or
        if no op_args defs matched if the opcode matched (i.e. the
        arguments weren't valid for that assembly operation).
    """

    if op_args_defs is None:
        op_args_defs = []

    line_tokens = token_utils.get_tokens_from_line(line)

    # Return early if there are no tokens
    if not line_tokens:
        return False, []

    # Return early if the opcode doesn't match
    line_opcode = line_tokens[0]
    if line_opcode != opcode:
        return False, []

    # Return early if this op code has no args
    line_args = line_tokens[1:]
    if not line_args and not op_args_defs:
        return True, []

    match = False
    for op_args_def in op_args_defs:
        args_are_correct, parsed_args = match_and_parse_args(
            line_args, op_args_def
        )
        if args_are_correct:
            if match:
                msg = (
                    "Args matched multiple arg possibilities."
                )
                raise OperationParsingError(msg)
            else:
                match = True
                ret_args = parsed_args

    if not match:
        poss_args_list = generate_possible_arg_list(op_args_defs)
        poss_args_quotes_list = [
            add_quotes_to_strings(poss_args) for poss_args in poss_args_list
        ]
        pretty_possible_args = "\n".join(poss_args_quotes_list)
        msg = (
            "Incorrect arguments specified for the {opcode} "
            "operation:\n\n{pretty_args}\n\nThe possible arguments "
            "are:\n\n{pretty_possible_args}.".format(
                opcode=opcode,
                pretty_args=add_quotes_to_strings(line_args),
                pretty_possible_args=pretty_possible_args,
            )
        )
        raise OperationParsingError(msg)

    return True, ret_args


def generate_possible_arg_list(op_args_defs):
    """
    Create a readable list of all possible argument combinations.

    Args:
        op_args_defs (list(list(dict))): Data structure that defines
            the different combinations of arguments. See
            :func:`~.get_arg_def_template` for more details.
    Returns:
        list(str): All possible argument combinations.
    """

    arg_possibilities = []
    for op_args_def in op_args_defs:
        args = []
        for op_arg_def in op_args_def:
            arg = ""
            if op_arg_def["value_type"] == "module_name":
                arg = op_arg_def["value"]
            if op_arg_def["value_type"] == "constant":
                arg = "<constant>"
            if op_arg_def["is_memory_location"]:
                arg = token_utils.represent_as_memory_index(arg)
            args.append(arg)
        arg_possibilities.append(args)
    return arg_possibilities


def match_and_parse_args(line_args, op_args_def):
    """
    Parse assembly operation args if they match the definition.

    Take arguments supplied for the assembly operation and see if they
    match this arguments definition.

    Args:
        line_args: (list(str)): The arguments supplied for this assembly
            operation.
        op_args_def (list(dict)): Definition of a set of arguments. See
            :func:`~.get_arg_def_template` for more details.

    Returns:
        (bool, list(dict)): Whether or not the arguments matched, and if
        they did, the parsed values.

    Raises:
        OperationParsingError: If a single argument managed to match
            different kinds of argument definitions.
    """

    if len(line_args) != len(op_args_def):
        return False, []

    parsed_args = []
    for line_arg, op_arg_def in zip(line_args, op_args_def):
        num_matches = 0
        # If the argument is a plain module name
        if (op_arg_def["value_type"] == "module_name"
                and not op_arg_def["is_memory_location"]
                and not token_utils.is_memory_index(line_arg)
                and line_arg == op_arg_def["value"]):
            parsed_arg = deepcopy(op_arg_def)
            parsed_args.append(parsed_arg)
            num_matches += 1

        # If the argument is a module name indexing memory
        if (op_arg_def["value_type"] == "module_name"
                and op_arg_def["is_memory_location"]
                and token_utils.is_memory_index(line_arg)):
            memory_position = token_utils.extract_memory_position(line_arg)
            if memory_position == op_arg_def["value"]:
                parsed_arg = deepcopy(op_arg_def)
                parsed_args.append(parsed_arg)
                num_matches += 1

        # If the argument is a plain constant
        if (op_arg_def["value_type"] == "constant"
                and not op_arg_def["is_memory_location"]
                and not token_utils.is_memory_index(line_arg)
                and token_utils.is_constant(line_arg)):
            parsed_arg = deepcopy(op_arg_def)
            parsed_arg["value"] = line_arg
            parsed_args.append(parsed_arg)
            num_matches += 1

        # If the argument is a constant indexing memory
        if (op_arg_def["value_type"] == "constant"
                and op_arg_def["is_memory_location"]
                and token_utils.is_memory_index(line_arg)):
            memory_position = token_utils.extract_memory_position(line_arg)
            if token_utils.is_constant(memory_position):
                parsed_arg = deepcopy(op_arg_def)
                parsed_arg["value"] = memory_position
                parsed_args.append(parsed_arg)
                num_matches += 1

        # If this argument didn't match, then these args don't match the
        # defs
        if num_matches == 0:
            return False, []

        # If there was more than one match something strange has
        # happened, bail.
        if num_matches > 1:
            msg = (
                "The argument '{line_arg} matched more than one "
                "argument type".format(line_arg=line_arg)
            )
            raise OperationParsingError(msg)

    # If the for loop completes successfully, we've matched all the
    # args.
    return True, parsed_args
