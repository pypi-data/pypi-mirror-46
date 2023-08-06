"""
Create and export roms for the computer
"""

import os

from .operations import get_all_operations, fetch
from .language_defs import EMPTY_ADDRESS, MODULE_CONTROLS_DEFAULT
from .data_structures import RomData
from . import bitdef
from . import number_utils


def get_rom():
    """
    Get complete representation of the rom.

    Returns:
        list(RomData): All the defined microcode.
    """

    language_templates = collect_language_datatemplates()
    romdatas = collapse_datatemplates_to_romdatas(language_templates)
    full_rom = populate_empty_addresses(romdatas)
    if romdatas_have_duplicate_addresses(full_rom):
        raise ValueError("Romdata set has duplicate addresses")
    full_rom.sort(key=lambda romdata: romdata.address)
    return full_rom


def collect_language_datatemplates():
    """
    Get all the datatemplates from all the defined operations.

    Returns:
        list(DataTemplate): All the data templates from the defined
            operations
    """

    operations = get_all_operations()
    operations.append(fetch)

    templates = []
    for operation in operations:
        templates.extend(operation.generate_microcode_templates())
    return templates


def collapse_datatemplates_to_romdatas(datatemplates):
    """
    Collapse any addresses in datatemplates to real values.

    If an address does need collapsing the original data is copied out
    to all the collapsed addresses.

    Args:
        datatemplates list(DataTemplates): A list of templates to
            collapse.
    Returns:
        list(RomData): The expanded datatemplates
    """

    romdatas = []
    for datatemplate in datatemplates:
        addresses = bitdef.collapse(datatemplate.address_range)
        for address in addresses:
            romdatas.append(
                RomData(address=address, data=datatemplate.data)
            )
    return romdatas


def populate_empty_addresses(romdatas):
    """
    Form a complete set of rom data by filling any undefined addresses.

    Args:
        romdatas list(RomData): The romdatas defined by the
            instructions.
    Returns:
        list(RomData): List of RomDatas representing a completely full
            rom
    """

    all_addresses = bitdef.collapse(EMPTY_ADDRESS)
    filled_addresses = {romdata.address: romdata.data for romdata in romdatas}
    complete_rom = []
    for address in all_addresses:
        if address in filled_addresses:
            complete_rom.append(
                RomData(address=address, data=filled_addresses[address])
            )
        else:
            complete_rom.append(
                RomData(address=address, data=MODULE_CONTROLS_DEFAULT)
            )
    return complete_rom


def romdatas_have_duplicate_addresses(romdatas):
    """
    Check if any of the romdatas have duplicate addresses.

    Args:
        romdatas list(RomData): List of romdatas to check.
    Returns:
        Bool: Whether or not there were any duplicated addresses.
    """

    duplicates = False
    addresses = []
    for romdata in romdatas:
        if romdata.address in addresses:
            duplicates = True
            break
        else:
            addresses.append(romdata.address)
    return duplicates


def slice_rom(rom):
    """
    Slice a rom into chunks 8 bits wide.

    This is to prepare the data to write into the roms. To take a single
    RomData as an example, if it looked like this (spaces added for
    clarity)::

        RomData(
            address="0000000 0000 000",
            data="10101010 111111111 00000000 11001100"
        )

    We would end up with::

        {
            0: RomData(
                address="0000000 0000 000",
                data="11001100"
            ),
            1: RomData(
                address="0000000 0000 000",
                data="00000000"
            ),
            2: RomData(
                address="0000000 0000 000",
                data="11111111"
            ),
            3: RomData(
                address="0000000 0000 000",
                data="10101010"
            )
        }

    Args:
        rom (list(RomData)): The complete ROM

    Returns:
        dict(int:list(RomData)) Dictionary of ROM slices
    """

    rom_slices = {}
    for rom_index in range(4):
        rom_offset = 8 * rom_index
        rom_slice = get_romdata_slice(rom, rom_offset + 7, rom_offset)
        rom_slices[rom_index] = rom_slice
    return rom_slices


def get_romdata_slice(romdatas, end, start):
    """
    Get a slice of the data in the romdatas.

    Args:
        romdatas (list(RomData)): The romdatas to get a slice from
        end (int): The index for the end of the slice. Starts at zero at
            the rightmost (least significant) bit.
        start (int): The index for the start of the slice. Starts at
            zero at the rightmost (least significant) bit.
    Returns:
        list(RomData): The sliced list of romdatas
    """

    sliced_romdatas = []
    for romdata in romdatas:
        data_slice = bitdef.extract_bits(romdata.data, end, start)
        sliced_romdata = RomData(address=romdata.address, data=data_slice)
        sliced_romdatas.append(sliced_romdata)
    return sliced_romdatas
