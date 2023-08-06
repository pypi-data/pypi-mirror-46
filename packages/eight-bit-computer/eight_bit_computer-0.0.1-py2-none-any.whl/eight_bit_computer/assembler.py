"""
Process assembly code and output machine code.
"""

from .exceptions import (
    LineProcessingError,
    OperationParsingError,
    AssemblyError,
)
from .data_structures import get_assembly_line_template
from .assembly_validity import check_structure_validity
from .operations import get_all_operations
from . import number_utils
from . import token_utils


def process_assembly_lines(lines, variable_start_offset=0):
    """
    Parse, assemble and generate machine code.

    Args:
        lines (list(str)): The lines that made up the assembly file to
            be assembled.
        variable_start_offset (int) (optional): How far to offset the
            first variable in data memory from 0.
    Returns:
        list(dict): The assembly file converted to an equivalent list of
        dictionaries with information about what each line was resolved
        to.
    Raises:
        AssemblyError: If there was an error assembling the machine
            code.
    """

    assembly_lines = []
    for line_no, line in enumerate(lines, start=1):
        try:
            assembly_line = process_line(line)
        except LineProcessingError as inst:
            msg = (
                "Error processing line {line_no} ({line}): "
                "{reason}".format(
                    line_no=line_no,
                    line=line,
                    reason=inst.args[0])
            )
            raise AssemblyError(msg)
        assembly_line["line_no"] = line_no
        assembly_lines.append(assembly_line)

    check_structure_validity(assembly_lines, variable_start_offset)
    assign_machine_code_byte_indexes(assembly_lines)
    assign_labels(assembly_lines)
    resolve_labels(assembly_lines)
    resolve_numbers(assembly_lines)
    resolve_variables(assembly_lines, variable_start_offset)

    return assembly_lines


def process_line(line):
    """
    Process a single line of assembly.

    Args:
        line (str): The line of assembly to process. This line has
            already been cleaned (excess whitespace and comments
            removed).
    Returns:
        dict: A dictionary of information about this line. See the
        :func:`~.get_assembly_line_template` documentation for more
        information about what is in the dictionary.
    """
    assembly_line = get_assembly_line_template()
    assembly_line["raw"] = line

    cleaned_line = clean_line(line)
    if not cleaned_line:
        return assembly_line
    assembly_line["clean"] = cleaned_line

    line_is_label = token_utils.is_label(cleaned_line)
    if line_is_label:
        assembly_line["defines_label"] = True
        assembly_line["defined_label"] = cleaned_line

    line_is_variable = token_utils.is_variable(cleaned_line)
    if line_is_variable:
        assembly_line["defines_variable"] = True
        assembly_line["defined_variable"] = cleaned_line

    if not (line_is_variable or line_is_label):
        mc_bytes = machine_code_bytes_from_line(cleaned_line)
        validate_and_identify_constants(mc_bytes)
        assembly_line["mc_bytes"] = mc_bytes
        assembly_line["has_machine_code"] = True

    return assembly_line


def clean_line(line):
    """
    Clean a line of assembly ready for further processing.

    Removes leading and trailing whitespace, comments, and excess
    whitespace between tokens.

    Args:
        line (str): The line to clean.
    Returns:
        str: The cleaned line.
    """
    no_comments = remove_comments(line)
    no_excess_whitespace = remove_excess_whitespace(no_comments)
    return no_excess_whitespace


def remove_comments(line):
    """
    Remove comments from a line.

    A comment is anything on the line after and including an occurrence
    of ``//``.

    Args:
        line (str): line to remove comments from.
    Returns:
        str: The line with comments removed.
    """
    comment_index = line.find("//")
    comments_removed = line
    if comment_index >= 0:
        comments_removed = line[:comment_index]
    return comments_removed


def remove_excess_whitespace(line):
    """
    Remove excess whitespace from a line.

    Args:
        line (str): line to remove excess whitespace from.
    Returns:
        str: The line with excess whitespace removed.
    """
    return " ".join(line.strip().split())


def machine_code_bytes_from_line(line):
    """
    Get machine code bytes that describe this line.

    Uses all the defined instructions and defers the work of parsing to
    them. See :func:`~.get_machine_code_byte_template` for information on
    machine code dictionaries from instructions.

    Expects the passed in line to be a valid line of machine code. That
    is, the passed in line should be translatable to valid machine code.

    Args:
        line (str): Line to parse.
    Returns:
        list(dict): Machine code byte information dictionaries.
    Raises:
        LineProcessingError: Failure to extract machine code or matching
        multiple operations.
    """
    operation_matches = []
    for operation in get_all_operations():
        try:
            mc_bytes = operation.parse_line(line)
        except OperationParsingError as e:
            raise LineProcessingError(e)
        if mc_bytes:
            operation_matches.append(mc_bytes)

    num_matches = len(operation_matches)
    if num_matches == 0:
        raise LineProcessingError("Unable to match line to an operation")
    if num_matches > 1:
        raise LineProcessingError("Line matched multiple operations")

    return operation_matches[0]


def validate_and_identify_constants(machine_code_bytes):
    """
    Validate and identify constants from assembly code.

    Assumed constants are returned from the instruction parsers. This
    function then validates them to make sure they are correct and
    determines what kind of constant they are.

    See :func:`~.get_mc_byte_template` for information on
    machine code dictionaries from instructions.

    This function modifies the passed in machine code templates list
    in place.

    Args:
        machine_code_bytes (list(dict)): The machine code byte
            dicts as returned by an instruction line parser.
    Raises:
        LineProcessingError: Invalid constants were specified.
    """

    for mc_byte in machine_code_bytes:
        if mc_byte["byte_type"] != "constant":
            continue

        constant = mc_byte["constant"]

        if not token_utils.is_constant(constant):
            raise LineProcessingError("Not a valid constant")

        constant_is_label = token_utils.is_label(constant)
        constant_is_variable = token_utils.is_variable(constant)
        constant_is_number = token_utils.is_number(constant)

        constants = [
            constant_is_label, constant_is_variable, constant_is_number
        ]

        num_constants = sum([1 for _constant in constants if _constant])
        if num_constants > 1:
            raise LineProcessingError("Constant is of more than one type")

        if constant_is_label:
            mc_byte["constant_type"] = "label"
        elif constant_is_variable:
            mc_byte["constant_type"] = "variable"
        else:
            mc_byte["constant_type"] = "number"
            value = token_utils.number_constant_value(constant)
            if not (number_utils.number_is_within_bit_limit(
                    value, bit_width=8)):
                msg = (
                    "Number specified ({number}) is not within the "
                    "range of values that a byte can store "
                    "(-127 to 255)".format(number=constant)
                )
                raise LineProcessingError(msg)
            mc_byte["number_value"] = value


def assign_machine_code_byte_indexes(assembly_lines):
    """
    Assign indexes to the machine code bytes.

    This modifies the passed in list of assembly lines, adding data to
    it.

    Args:
        assembly_lines (list(dict)): Lines of assembly to add label
        information to.
    """

    mc_byte_index = 0
    for assembly_line in assembly_lines:
        if assembly_line["has_machine_code"]:
            for mc_byte in assembly_line["mc_bytes"]:
                mc_byte["index"] = mc_byte_index
                mc_byte_index += 1


def assign_labels(assembly_lines):
    """
    Assign labels to the lines for later reference

    This modifies the passed in list of assembly lines, adding data to
    it.

    Args:
        assembly_lines (list(dict)): Lines of assembly to add label
        information to.
    """

    label = None
    for assembly_line in assembly_lines:
        if label is None and assembly_line["defines_label"]:
            label = assembly_line["defined_label"]
        if assembly_line["has_machine_code"] and label is not None:
            assembly_line["has_label_assigned"] = True
            assembly_line["assigned_label"] = label
            label = None


def resolve_labels(assembly_lines):
    """
    Resolve labels to indexes in the machine code bytes.

    This modifies the passed in list of assembly line dictionaries.

    Args:
        assembly_lines (list(dict)): List of assembly lines to resolve
            label references in.
    """

    label_map = create_label_map(assembly_lines)
    for assembly_line in assembly_lines:
        if assembly_line["has_machine_code"]:
            for mc_byte in assembly_line["mc_bytes"]:
                if (mc_byte["byte_type"] == "constant"
                        and mc_byte["constant_type"] == "label"):
                    label = mc_byte["constant"]
                    mc_byte["bitstring"] = label_map[label]


def create_label_map(assembly_lines):
    """
    Create a map of labels to machine code byte indexes.

    Args:
        assembly_lines (list(dict)): List of assembly lines to create a
            label map for.
    Returns:
        dict(str:str): Dictionary of label names to machine code
        indexes.
    """

    label_map = {}
    mc_byte_index = 0
    for assembly_line in assembly_lines:
        if assembly_line["has_label_assigned"]:
            index_bit_string = number_utils.number_to_bitstring(mc_byte_index)
            label_map[assembly_line["assigned_label"]] = index_bit_string
        if assembly_line["has_machine_code"]:
            mc_byte_index += len(assembly_line["mc_bytes"])
    return label_map


def resolve_numbers(assembly_lines):
    """
    Resolve number constants to machine code byte values.

    This modifies the passed in list of assembly line dictionaries.

    Args:
        assembly_lines (list(dict)): List of assembly lines to resolve
            numbers for.
    """
    for assembly_line in assembly_lines:
        if assembly_line["has_machine_code"]:
            for mc_byte in assembly_line["mc_bytes"]:
                if (mc_byte["byte_type"] == "constant"
                        and mc_byte["constant_type"] == "number"):
                    number = mc_byte["number_value"]
                    mc_byte["bitstring"] = number_utils.number_to_bitstring(
                        number
                    )


def resolve_variables(assembly_lines, variable_start_offset):
    """
    Resolve variable constants to indexes in data memory.

    This modifies the passed in list of assembly line dictionaries.

    Args:
        assembly_lines (list(dict)): List of assembly lines to resolve
            variables in.
        variable_start_offset (int): An offset into data
            memory for where to start storing the variables.
    """
    variable_map = create_variable_map(assembly_lines, variable_start_offset)
    for assembly_line in assembly_lines:
        if assembly_line["has_machine_code"]:
            for mc_byte in assembly_line["mc_bytes"]:
                if (mc_byte["byte_type"] == "constant"
                        and mc_byte["constant_type"] == "variable"):
                    variable = mc_byte["constant"]
                    mc_byte["bitstring"] = variable_map[variable]


def create_variable_map(assembly_lines, variable_start_offset):
    """
    Create a map of variables to indexes in data memory.

    Args:
        assembly_lines (list(dict)): List of assembly lines to create a
            variable map for.
        variable_start_offset (int): An offset into data
            memory for where to start storing the variables.
    Returns:
        dict(str:str): Dictionary of variable names to machine code
        indexes.
    """

    variable_map = {}
    variable_index = variable_start_offset
    for assembly_line in assembly_lines:

        # Check for defined variable
        if assembly_line["defines_variable"]:
            variable = assembly_line["defined_variable"]
            if variable in variable_map:
                continue
            variable_map[variable] = number_utils.number_to_bitstring(
                variable_index
            )
            variable_index += 1
            continue

        # Check for variable in machine code
        if assembly_line["has_machine_code"]:
            for mc_byte in assembly_line["mc_bytes"]:
                if mc_byte["byte_type"] != "constant":
                    continue
                if mc_byte["constant_type"] != "variable":
                    continue
                variable = mc_byte["constant"]
                if variable in variable_map:
                    continue
                variable_map[variable] = number_utils.number_to_bitstring(
                    variable_index
                )
                variable_index += 1
    return variable_map
