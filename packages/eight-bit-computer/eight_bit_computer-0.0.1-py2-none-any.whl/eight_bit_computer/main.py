"""
Top level interface for the module
"""

import os

from .assembler import process_assembly_lines
from .assembly_summary import generate_assembly_summary
from .exceptions import AssemblyError
from . import export
from . import rom


def assemble(
        input_path,
        output_path=None,
        variable_start_offset=0,
        output_format="logisim",
        ):
    """
    Read an assembly file and write out equivalent machine code.

    Args:
        input_path (str): The location of the assembly file.
        output_path (str) (optional): The location to write out the
            machine code. If nothing is passed, the output path will be
            the input path with the extension changed to mc or have mc
            added if no extension was present.
        variable_start_offset (int) (optional): How far to offset the
            first variable in data memory from 0.
        output_format (str) (optional): How to foramt the output.
            ``logisim`` or ``cpp``.
    """

    if not input_path.endswith(".asm"):
        print "Input file must have a .asm extension."
        return

    lines = filepath_to_lines(input_path)

    try:
        assembly_line_infos = process_assembly_lines(
            lines, variable_start_offset=variable_start_offset
        )
    except AssemblyError as inst:
        print inst.args[0]
        return

    if output_path is None:
        output_path = get_mc_filepath(input_path)

    print generate_assembly_summary(assembly_line_infos)

    mc_byte_bitstrings = extract_machine_code(assembly_line_infos)
    if output_format == "logisim":
        output = export.bitstrings_to_logisim(mc_byte_bitstrings)
    elif output_format == "cpp":
        output = export.bitstrings_to_cpp(mc_byte_bitstrings)

    with open(output_path, "w") as file:
        file.write(output)


def filepath_to_lines(input_path):
    """
    Take a filepath and get all the lines of the file.

    The lines returned have the newline stripped.

    Args:
        input_path (str): Path to the file of disk to read.
    Returns:
        list(str): Lines of the file.
    """
    with open(input_path) as file:
        lines = file.read().splitlines()
    return lines


def get_mc_filepath(asm_path):
    """
    Get the filepath for the machine code.

    This is the assembly filepath with .asm replaced with .mc

    Args:
        asm_path (str): Path to the assembly file.
    Returns:
        str: Path to the machine code file.
    """

    return "{basepath}.mc".format(basepath=asm_path[:-4])


def extract_machine_code(assembly_lines):
    """
    Extract machine code from assembly line dictionaries.

    Args:
        assembly_lines (list(dict)): List of assembly line info
            dictionaries to extract machine code from. See
            :func:`~.get_assembly_line_template` for details on what
            those dictionaries contain.
    Returns:
        list(str): List of bit strings for the machine code.
    """
    machine_code = []
    for assembly_line in assembly_lines:
        if assembly_line["has_machine_code"]:
            for mc_byte in assembly_line["mc_bytes"]:
                machine_code.append(mc_byte["bitstring"])
    return machine_code


def create_roms(directory="", output_format="logisim"):
    """
    Write files containing microcode for drive the roms.

    Args:
        directory (str) (optional): The directory to write the roms
            into.
        output_format (str) (optional): How to foramt the output.
            ``logisim`` or ``cpp``.
    """
    rom_data = rom.get_rom()
    rom_slices = rom.slice_rom(rom_data)
    for rom_index, rom_slice in enumerate(rom_slices):

        slice_bitstrings = [romdata["data"] for romdata in rom_slice]
        if output_format == "logisim":
            output = export.bitstrings_to_logisim(slice_bitstrings)
        elif output_format == "cpp":
            output = export.bitstrings_to_cpp(slice_bitstrings)

        rom_filename = "rom_{rom_index}".format(rom_index=rom_index)
        filepath = os.path.join(directory, rom_filename)

        with open(filepath, "w") as romfile:
            romfile.write(output)
