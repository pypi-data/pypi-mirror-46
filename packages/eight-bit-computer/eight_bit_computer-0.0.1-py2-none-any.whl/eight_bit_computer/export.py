"""
Functionality to convert data other package friendly formats.
"""

from . import number_utils


def bitstrings_to_cpp(bitstrings):
    """

    """
    raise NotImplementedError


def bitstrings_to_logisim(bitstrings):
    """
    Convert bitstrigs to a logising RAM/ROM file format.

    Used to convert ROMs and machine code.

    Args:
        bitstrings (list(str)): List of bitstrings to convert to a
            logisim friendly format.
    Returns:
        str: String ready to be written to a file.

    """
    logisim_lines = ["v2.0 raw"]
    for line_bytes in chunker(bitstrings, 16):
        line_parts = []
        for line_chunk_bytes in chunker(line_bytes, 4):
            hex_strings = [
                number_utils.bitstring_to_hex_string(bit_string)
                for bit_string
                in line_chunk_bytes
            ]
            four_hex_bytes = " ".join(hex_strings)
            line_parts.append(four_hex_bytes)
        line = "  ".join(line_parts)
        logisim_lines.append(line)
    logisim_string = "\n".join(logisim_lines)
    logisim_string += "\n"
    return logisim_string


def chunker(seq, chunk_size):
    """
    Take a larger sequence and split it into smaller chunks.

    E.g.::

        chunker([0,1,2,3,4,5], 4) -> [0,1,2,3], [4,5]

    Args:
        seq (list): List of things to chunk up
        chunk_size (int): How big each chunk should be.
    Returns:
        generator: Generator that yields each chunk.
    """
    return (
        seq[pos:pos + chunk_size] for pos in xrange(0, len(seq), chunk_size)
    )
