"""
The fetch steps added to the start of all operations.
"""

from ..language_defs import MODULE_CONTROL, STEPS, EMPTY_ADDRESS
from .. import bitdef
from ..data_structures import DataTemplate


def generate_microcode_templates():
    """
    Generate datatemplates for all the fetch steps.

    Returns:
        list(DataTemplate): Datatemplates that represent the fetch
        steps.
    """

    return [fetch_step_0(), fetch_step_1()]


def fetch_step_0():
    """
    Create template for the first fetch step.

    Returns:
        DataTemplate: The first fetch step.
    """

    address_bitdef = bitdef.merge(
        [
            EMPTY_ADDRESS,
            STEPS[0],
        ]
    )

    control_bitdef = bitdef.merge(
        [
            MODULE_CONTROL["PC"]["OUT"],
            MODULE_CONTROL["MAR"]["IN"],
        ]
    )
    control_bitdef = bitdef.fill(control_bitdef, "0")

    return DataTemplate(address_range=address_bitdef, data=control_bitdef)


def fetch_step_1():
    """
    Create template for the second fetch step.

    Returns:
        DataTemplate: The second fetch step.
    """
    address_bitdef = bitdef.merge(
        [
            EMPTY_ADDRESS,
            STEPS[1],
        ]
    )

    control_bitdef = bitdef.merge(
        [
            MODULE_CONTROL["PC"]["COUNT"],
            MODULE_CONTROL["RAM"]["OUT"],
            MODULE_CONTROL["RAM"]["SEL_PROG_MEM"],
            MODULE_CONTROL["IR"]["IN"],
        ]
    )
    control_bitdef = bitdef.fill(control_bitdef, "0")
    return DataTemplate(address_range=address_bitdef, data=control_bitdef)
