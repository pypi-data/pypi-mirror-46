"""
Data structures use to pass information between functions.
"""

from collections import namedtuple


DataTemplate = namedtuple("DataTemplate", ["address_range", "data"])
"""
Some data and a range of addresses to store that data in

Attributes:
    address_range (str): The range of addresses to store the data in.
        0 and 1 are absolute values, X is either a 0 or 1 and the
        expectation is that the data will expand out to the parts of the
        address marked with an X. and example could be "0010XX001".
    data (str): The data to be stored at the given addresses.
"""


RomData = namedtuple("RomData", ["address", "data"])
"""
Some data and an address to store it in

Attributes:
    address (str): The address to store the data in.
    data (int): The data to be stored at the given address.
"""


def get_summary_entry_template():
    """
    Get a template to describe each line in an assembly summary

    Keys have the following meanings:

    - has_assembly: Does this line of the summary have assembly code.
    - assembly: Information about the assembly in this summary line.
    - assembly/info: The assembly line information dictionary (as
      returned by :func:`~.get_assembly_line_template`) and filled in by
      the assembler.
    - has_mc_byte: Does this line of the summary have a machine code
      byte.
    - mc_byte: Information about the machine code byte on this line.
    - mc_byte/info: Machine code byte information dictionary (as
      returned by :func:`~.get_machine_code_byte_template` and filled by
      the assembly process).
    - mc_byte/has_label: Whether of not this machine code byte has an
      associated label.
    - mc_byte/label: The label of this machine code byte.

    Returns:
        dict: Summary entry template.
    """

    return {
        "has_assembly": False,
        "assembly": {
            "info": {},
        },
        "has_mc_byte": False,
        "mc_byte": {
            "info": {},
            "has_label": False,
            "label": "",
        }
    }


def get_assembly_line_template():
    """
    Get a template for the assembly line information bundle.

    Template for a dictionary that contains information about this line
    of assembly code. The keys have the following meanings:

    - line_no: The line in the assembly file that this line was on.
    - raw: The line as it was in the assembly file.
    - clean: The cleaned up line, ready for parsing.
    - defines_label: Whether or not this line is a label definition.
    - defined_label: The label that this line defined.
    - has_label_assigned: Whether or not this line has a label assigned
      to it.
    - assigned_label: The label that has been assigned to the first
      line of the machine code generated for this line.
    - defines_variable: Whether or not this line is a variable
      definition.
    - defined_variable: The variable that this line defines.
    - has_machine_code: Whether or not this line results in machine
      code. E.g. a comment has no machine code.
    - mc_bytes: List of machine code byte templates (with
      constant expansion information) for this assembly line.

    Returns:
        dict: Assembly line description template.
    """

    return {
        "line_no": -1,
        "raw": "",
        "clean": "",

        "defines_label": False,
        "defined_label": "",

        "has_label_assigned": False,
        "assigned_label": "",

        "defines_variable": False,
        "defined_variable": "",

        "has_machine_code": False,
        "mc_bytes": [],
    }


def get_arg_def_template():
    """
    Get a definition template for an assembly operation argument.

    This is a set of information that describes an argument used in a
    line of assembly.

    The keys have the following meaning:

    - value_type: What kind of argument this is. ``constant`` or
      ``module_name``.
    - is_memory_location: Whether this argument is referring to a
      location in memory.
    - value: The permitted value of the argument if it's a module.

    These dictionaries will be grouped in a list of lists that describe
    the possible arguments for an assembly operation. E.g. if the
    possible arguments for an assembly operation were:

    - ``ACC`` ``A``
    - ``B`` ``C``
    - ``A`` ``[#123]``

    The data structure would be as follows::

        [
            [
                {
                    "value_type": "module_name",
                    "is_memory_location": False,
                    "value": "ACC",
                },
                {
                    "value_type": "module_name",
                    "is_memory_location": False,
                    "value": "A",
                },
            ],
            [
                {
                    "value_type": "module_name",
                    "is_memory_location": False,
                    "value": "B",
                },
                {
                    "value_type": "module_name",
                    "is_memory_location": True,
                    "value": "C",
                },
            ],
            [
                {
                    "value_type": "module_name",
                    "is_memory_location": False,
                    "value": "A",
                },
                {
                    "value_type": "constant",
                    "is_memory_location": True,
                    "value": "",
                },
            ],
        ]

    Returns:
        dict: Machine code byte description template.
    """

    return {
        "value_type": "",
        "is_memory_location": False,
        "value": "",
    }


def get_machine_code_byte_template():
    """
    Get the template used to describe a machine code byte.

    This is a set of information that describes the byte (of which there
    could be many) of machine code that an operation (e.g. LOAD
    [$variable] A) results in.

    The keys have the following meaning:

    - bitstring: A byte bitstring of the final byte that will make up
      the machine code.
    - byte_type: The type of machine code byte. Will be instruction or
      constant.
    - constant_type: The type of the constant. Could be a label,
      variable or number.
    - constant: The constant that this byte will need to become. The
      resolution of the constant to a real machine code byte is done by
      the assembler.
    - number_value: The value of the constant as an int if it's a
      number.
    - index: The index of this byte in program data.

    Returns:
        dict: Machine code byte description template.
    """

    return {
        "bitstring": "",
        "byte_type": "",
        "constant_type": "",
        "constant": "",
        "number_value": 0,
        "index": -1,
    }
