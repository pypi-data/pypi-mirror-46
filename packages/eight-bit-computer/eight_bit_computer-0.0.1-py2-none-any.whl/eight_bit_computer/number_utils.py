"""
Functions for working with, checking and converting numbers.

All numbers are stored within the computer as the positive equivalent.
They may be interpreted as negative.
"""


def number_to_bitstring(number, bit_width=8):
    """
    Convert a number to an equivalent bitstring of the given width.

    Raises:
        ValueError: If number doesn't fit in the bit width.
    """
    if not number_is_within_bit_limit(number, bit_width=bit_width):
        raise ValueError(
            "{number} will not fit in {num_bits} bits.".format(
                number=number, num_bits=bit_width
            )
        )
    number = get_positive_equivalent(number)

    return "{number:0{bit_width}b}".format(
        number=number, bit_width=bit_width
    )


def number_is_within_bit_limit(number, bit_width=8):
    """
    Check if a number can be stored in the number of bits given.

    Negative numbers are stored in 2's compliment binary.

    Args:
        number (int): The number to check.
        bit_width (int, optional): The number of bits available.
    Returns:
        bool: True if within limits, False if not.
    """

    min_val = (2**bit_width / 2) * -1
    max_val = 2**bit_width - 1

    return min_val <= number <= max_val


def get_positive_equivalent(number):
    """
    Read the 2's compliment equivalent of this number as positive.

    With a 3 bit number, the positive equivalent of -2 is 5. E.g.::

        -4 4 100
        -3 5 101
        -2 6 110
        -1 7 111
         0 0 000
         1 1 001
         2 2 010
         3 3 011

    Args:
        number (int): The number to convert to a positive quivalent
    Returns:
        int: The positive equivalent of the number.
    """

    ret = number
    if number < 0:
        ret = number + 256
    return ret


def bitstring_to_number(bitstring):
    """
    Convert a bitstring to a number.

    E.g. ``10110101`` gives 181.

    Args:
        bitstring (str): String of ``1``\ s and ``0``\ s.
    Returns:
        int: The equivalent integer.

    """
    return int(bitstring, 2)


def bitstring_to_hex_string(bitstring, zero_pad_width=2):
    """
    Convert a bitstring to a hex number.

    Args:
        bitstring (str): String of ``1``\ s and ``0``\ s.
        zero_pad_width (int) (optional): How many zeroes to pad the
            returned hex value with.
    """

    return "{num:0{zero_pad_width}X}".format(
        num=int(bitstring, 2), zero_pad_width=zero_pad_width
    )
