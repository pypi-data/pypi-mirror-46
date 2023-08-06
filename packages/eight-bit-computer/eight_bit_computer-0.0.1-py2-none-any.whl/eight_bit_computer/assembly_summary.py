"""
Extract information from a list of assembly line info dictionaries.
"""
from copy import deepcopy

from . import number_utils
from .data_structures import get_summary_entry_template


def generate_assembly_summary(asm_line_infos):
    """
    Produce a summary that combines assembly and machine code.

    The summary will be like this::

         1 $variable0              |
         2 @label1                 |
         3     LOAD [$variable1] A |  0 00 00000000 - @label1 255 FF 11111111
                                   |  1 01 00000001 -           1 01 00000001 $variable1
         4                         |
         5 @label2                 |
         6     LOAD [$variable2] A |  2 02 00000010 - @label2 255 FF 11111111
                                   |  3 03 00000011 -           2 02 00000010 $variable2
         7     JUMP @label1        |  4 04 00000100 -         255 FF 11111111
                                   |  5 05 00000101 -           0 00 00000000 @label1
         8                         |
         9     STORE A [#123]      |  6 06 00000110 -         255 FF 11111111
                                   |  7 07 00000111 -         123 7B 01111011 #123
        10 @label3                 |
        11     LOAD [$variable3] B |  8 08 00001000 - @label3 255 FF 11111111
                                   |  9 09 00001001 -           3 03 00000011 $variable3
        12     LOAD [$variable0] C | 10 0A 00001010 -         255 FF 11111111
                                   | 11 0B 00001011 -           0 00 00000000 $variable0
        13 $variable4              |
        14 // comment

    Args:
        asm_line_infos (list(dict)): List of dictionaries of information
            about the parsed assembly.
    Returns:
        str: Printable summary.
    """
    lines = generate_assembly_summary_lines(asm_line_infos)
    return "\n".join(lines)


def generate_assembly_summary_lines(asm_line_infos):
    """
    Generate list of lines for an assembly summary

    Args:
        asm_line_infos (list(dict)): List of dictionaries of information
            about the parsed assembly.
    Returns:
        list(str): List of lines for the summary.
    """

    summary_data = get_assembly_summary_data(asm_line_infos)
    widest_values = get_widest_column_values(summary_data)
    summary_line_template = (
        "{asm_line_no: >{widest_asm_line_no}} "
        "{raw_assembly_line: <{widest_asm_line}} "
        "| "
        "{mc_index_decimal: >{widest_mc_index_decimal}} "
        "{mc_index_hex} "
        "{mc_index_bitstring} "
        "{mc_byte_sep} "
        "{mc_label: <{widest_mc_label}} "
        "{mc_byte_decimal: >{widest_mc_byte_decimal}} "
        "{mc_byte_hex:} "
        "{mc_byte_bitstring} "
        "{mc_byte_constant}"
    )
    formatted_summary_lines = []
    for summary_line in summary_data:
        if summary_line["has_assembly"]:
            asm_line_info = summary_line["assembly"]["info"]
            asm_line_no = str(asm_line_info["line_no"])
            raw_assembly_line = asm_line_info["raw"]
        else:
            asm_line_no = ""
            raw_assembly_line = ""

        if summary_line["has_mc_byte"]:
            mc_byte_info = summary_line["mc_byte"]["info"]
            mc_index_decimal = str(mc_byte_info["index"])
            mc_index_hex = "{index:02X}".format(
                index=mc_byte_info["index"],
                )
            mc_index_bitstring = number_utils.number_to_bitstring(
                mc_byte_info["index"]
            )
            mc_byte_sep = "-"
            if summary_line["mc_byte"]["has_label"]:
                mc_label = summary_line["mc_byte"]["label"]
            else:
                mc_label = ""
            mc_byte_decimal = str(
                number_utils.bitstring_to_number(mc_byte_info["bitstring"])
            )
            mc_byte_bitstring = mc_byte_info["bitstring"]
            mc_byte_hex = "{mc_byte:02X}".format(
                mc_byte=int(mc_byte_info["bitstring"], 2),
            )
            if mc_byte_info["byte_type"] == "constant":
                mc_byte_constant = mc_byte_info["constant"]
            else:
                mc_byte_constant = ""
        else:
            mc_index_decimal = ""
            mc_index_hex = ""
            mc_index_bitstring = ""
            mc_byte_sep = ""
            mc_label = ""
            mc_byte_decimal = ""
            mc_byte_bitstring = ""
            mc_byte_hex = ""
            mc_byte_constant = ""

        formatted_line = summary_line_template.format(
            asm_line_no=asm_line_no,
            widest_asm_line_no=widest_values["asm_line_no"],
            raw_assembly_line=raw_assembly_line,
            widest_asm_line=widest_values["asm_line"],
            mc_index_decimal=mc_index_decimal,
            widest_mc_index_decimal=widest_values["mc_index_decimal"],
            mc_index_hex=mc_index_hex,
            mc_index_bitstring=mc_index_bitstring,
            mc_byte_sep=mc_byte_sep,
            mc_label=mc_label,
            widest_mc_label=widest_values["mc_label"],
            mc_byte_decimal=mc_byte_decimal,
            widest_mc_byte_decimal=widest_values["mc_byte_decimal"],
            mc_byte_bitstring=mc_byte_bitstring,
            mc_byte_hex=mc_byte_hex,
            mc_byte_constant=mc_byte_constant,
        ).rstrip()
        formatted_summary_lines.append(formatted_line)

    return formatted_summary_lines


def get_assembly_summary_data(asm_line_infos):
    """
    Process assembly data to make formatting easier for the summary.

    Args:
        asm_line_infos (list(dict)): List of line info dictionaries as
            returned by
            :func:`~.process_assembly_lines`
            .
    Returns:
        list: List of entries for the assembly summary print out
    """

    assembly_summary = []

    for asm_line_info in asm_line_infos:
        if asm_line_info["has_machine_code"]:
            dual_entry = get_summary_entry_template()
            dual_entry["has_assembly"] = True
            dual_entry["assembly"]["info"] = deepcopy(asm_line_info)

            dual_entry["has_mc_byte"] = True
            dual_entry["mc_byte"]["info"] = deepcopy(
                asm_line_info["mc_bytes"][0]
            )
            if asm_line_info["has_label_assigned"]:
                dual_entry["mc_byte"]["has_label"] = True
                dual_entry["mc_byte"]["label"] = asm_line_info["assigned_label"]
            assembly_summary.append(dual_entry)

            for mc_byte_info in asm_line_info["mc_bytes"][1:]:
                byte_only_entry = get_summary_entry_template()
                byte_only_entry["has_mc_byte"] = True
                byte_only_entry["mc_byte"]["info"] = deepcopy(mc_byte_info)
                assembly_summary.append(byte_only_entry)

        else:
            assembly_only_entry = get_summary_entry_template()
            assembly_only_entry["has_assembly"] = True
            assembly_only_entry["assembly"]["info"] = deepcopy(asm_line_info)
            assembly_summary.append(assembly_only_entry)

    return assembly_summary


def get_widest_column_values(assembly_summary_data):
    """
    Find widest values in the columns of the output.

    Required for the eventual printed table to line up correctly.

    Args:
        assembly_summary_data (list(dict)): List of dictionaries (as
            returned by :func:`~.get_assembly_summary_data`) with all the
            summary information data.
    Returns:
        dict: Mapping of columns for widest values.
    """

    widest_values = {
        "asm_line_no": 0,
        "asm_line": 0,
        "mc_index_decimal": 0,
        "mc_byte_decimal": 0,
        "mc_label": 0,
    }

    for entry in assembly_summary_data:
        if entry["has_assembly"]:
            # Assembly line number width
            line_no_width = len(str(entry["assembly"]["info"]["line_no"]))
            if line_no_width > widest_values["asm_line_no"]:
                widest_values["asm_line_no"] = line_no_width

            # Assembly line width
            asm_line_width = len(entry["assembly"]["info"]["raw"])
            if asm_line_width > widest_values["asm_line"]:
                widest_values["asm_line"] = asm_line_width

        if entry["has_mc_byte"]:
            # Decimal byte index width
            mcb_index_decimal_width = len(
                str(entry["mc_byte"]["info"]["index"])
            )
            if mcb_index_decimal_width > widest_values["mc_index_decimal"]:
                widest_values["mc_index_decimal"] = mcb_index_decimal_width

            # Decimal byte index width
            mc_byte_decimal_width = len(
                str(
                    number_utils.bitstring_to_number(
                        entry["mc_byte"]["info"]["bitstring"]
                    )
                )
            )
            if mc_byte_decimal_width > widest_values["mc_byte_decimal"]:
                widest_values["mc_byte_decimal"] = mc_byte_decimal_width

            # Label width
            if entry["mc_byte"]["has_label"]:
                mcb_label_width = len(entry["mc_byte"]["label"])
                if mcb_label_width > widest_values["mc_label"]:
                    widest_values["mc_label"] = mcb_label_width

    return widest_values
