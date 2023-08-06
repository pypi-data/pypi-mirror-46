"""
The bitdef and associated functions.

A bitdef is a string made up of ``.``\ s, ``0``\ s, and ``1``\ s.

 - ``.`` means that the bit at this position could be a 0 or a 1.
 - ``0`` means that the bit at this position is a 0.
 - ``1`` means that the bit at this position is a 1.

When indexing into a bitdef, indexes start at 0 and begin at the right
hand side or least significant bit of the value. E.g.::

    Index:  76543210
    Bitdef: 010.1..1

"""


def same_length(bitdefs):
    """
    Check if the passed in bitdefs are all the same length.

    Args:
        bitdefs list(str): Bitdefs to check length of.
    Returns:
        bool: True if all the bitdefs are the same length, False
        otherwise
    """

    all_same = True
    first_length = length(bitdefs[0])
    for other_bitdef in bitdefs[1:]:
        other_length = length(other_bitdef)
        if first_length != other_length:
            all_same = False
            break
    return all_same


def length(bitdef):
    """
    Calculate length of a bitdef.

    Args:
        bitdef (str): The bitdef to find the length of.
    Returns:
        int: The length of the bitdef.
    """

    return len(bitdef)


def have_overlapping_bits(bitdefs):
    """
    Check if the bitdefs have any bits set in the same position.

    Example with overlap (bits at index 2 and 6 overlap):

    - ``0...101.``
    - ``11...1..``

    Example with no overlap:

    - ``11010...``
    - ``......11``

    Args:
        bitdefs (list(str)): Bitdefs to check for overlaps.
    Returns:
        bool: Whether or not there were overlaps.
    """

    if not same_length(bitdefs):
        raise ValueError("Bitdefs are not all the same length.")

    different_bits = False
    for bitdef_index, bitdef in enumerate(bitdefs):
        for bit_index, bit in enumerate(bitdef):
            for test_bitdef in bitdefs[(bitdef_index + 1):]:
                test_bit = test_bitdef[bit_index]
                if bit != "." and test_bit != ".":
                    different_bits = True

    return different_bits


def merge(bitdefs):
    """
    Merge the bitdefs to a single bitdef.

    Bitdefs must

    - All be the same length.
    - Not have any bits defined in the same position.

    Args:
        bitdefs (list(str)): Bitdefs to merge.
    Returns:
        str: The merged bitdef.
    Raises:
        ValueError: If the bitdefs are not all the same length or have
        overlapping bits.
    """

    if not same_length(bitdefs):
        raise ValueError("Bitdefs are not all the same length.")
    if have_overlapping_bits(bitdefs):
        raise ValueError("Bitdefs have overlapping bits.")

    output = ""
    for index in range(length(bitdefs[0])):
        for bitdef in bitdefs:
            bit = bitdef[index]
            if bit != ".":
                output += bit
                break
        else:
            output += "."

    return output


def collapse(bitdef):
    """
    Collapse undefined bits into real bits to make new bitdefs.

    The undefined bits are expanded in order, from left to right, with 0
    first, then 1.

    For example, ``10.0.`` becomes:

    - ``10000``
    - ``10001``
    - ``10100``
    - ``10101``

    Args:
        bitdef(str): The bitdef to collapse.
    Returns:
        list(str): The list of bitdefs the original bitdef has collapsed
        to.
    """

    if "." in bitdef:
        res = collapse(bitdef.replace(".", "0", 1))
        res.extend(collapse(bitdef.replace(".", "1", 1)))
    else:
        res = [bitdef]

    return res


def fill(bitdef, value):
    """
    Fill undefined bits with a value.

    For example ``1..0100.1`` becomes ``111010011`` when filled with 1s.

    Args:
        bitdef (str): The bitdef to fill.
        value (str): The value to fill with, "0" or "1".
    Returns:
        str: The filled bitdef.
    """

    output = ""
    for bit in bitdef:
        if bit == ".":
            output += value
        else:
            output += bit
    return output


def extract_bits(bitdef, end, start):
    """
    Extract a region from the bitdef.

    Indexes for start and end start at zero from the right or least
    significant bit.

    For example, if the bitdef was ``00101011`` and the extraction end
    was 4 and start was 1 the result would be ``0101``::

        Extracted bits:      xxxx
        Index:            76543210
        Bitdef:           00101011
        Result:              0101

    Args:
        bitdef (str): The bitdef to extract bits from.
        end (int): Index of the leftmost bit of the portion to extract.
        start (int): Index of the rightmost bit of the portion to
            extract.
    Returns:
        str: The extracted portion of the bitdef.
    Raises:
        ValueError: If:

            - Extraction region is larger than bitdef.
            - Extraction end index is before extraction start index.
            - Extraction start index is less than 0.
    """

    bitdef_length = length(bitdef)
    if end > bitdef_length:
        raise ValueError("Extraction region is larger than bitdef.")
    if end < start:
        raise ValueError(
            "Extraction end index is before extraction start index."
        )
    if start < 0:
        raise ValueError("Extraction start index is less than 0.")
    if bitdef_length == 0:
        return bitdef

    reverse_end = reverse_index(end, bitdef_length)
    reverse_start = reverse_index(start, bitdef_length)

    return bitdef[reverse_end:reverse_start + 1]


def remove_whitespace(input_string):
    """
    Remove the whitespace from a string.

    Args:
        input_string (str): The string to remove whitespace from.
    Returns:
        str: The string with the whitespace removed.
    """
    return "".join(input_string.strip().split())


def reverse_index(index, length):
    """
    Reverse the passed in index as if the index direction was flipped.

    Taking the string "hello" as an example the regular indexes for
    each letter are::

        01234
        hello

    Reversing the indexes yields::

        43210
        hello

    This allows easily indexing into a bitdef on bitdef indexing terms.

    Args:
        index (int): The index position to reverse.
        length (int): The length of the array being indexed into.
    Returns:
        int: The reversed index.
    """

    return length - index - 1
