"""提供与`cst.units`交互的接口。

在理想情况下，这些接口允许用户在Python环境中处理和转换物理单位。但是CST 2024中的
`cst.units`模块目前存在一些问题，限制了其功能。因此，这些接口目前仅作为占位符存在，未来
可能会扩展以提供更全面的功能。


The `cst.units` package offers methods and classes to work with units supported by CST Studio Suite.

"""

import cst.units as cu


class ComplexQuantity:
    """Class to hold a real-valued physical quantity complex_value * Unit.

    convert_to(dest_unit: units.Unit) → units.ComplexQuantity
    Converts the current value * unit and expresses it in the given unit. Will throw an exception if the given dest_unit cannot be converted to.
    """

    def __init__(self, value, unit):

        self.cq = cu.ComplexQuantity(value, unit)
        return

    def pow(self, nom: int, denom: int) -> "ComplexQuantity":
        """Raises the value and the Unit to the power nom/denom use the ** operator to raise to round integer values."""
        return self.cq.pow(nom, denom)

    def sqrt(self) -> "ComplexQuantity":
        """Takes the square root of the value and the Unit."""
        return self.cq.sqrt()

    @property
    def unit(self) -> cu.Unit:
        """The physical Unit pertaining to the quantity."""
        return self.cq.unit

    @property
    def value(self):
        """The value portion of the quantity."""
        return self.cq.value


class Quantity:
    """Class to hold a real-valued physical quantity value * Unit.

    convert_to(dest_unit: units.Unit) → units.Quantity
    Converts the current value * unit and expresses it in the given unit. Will throw an exception if the given dest_unit cannot be converted to.
    """

    def __init__(self, value, unit):

        self.cq = cu.Quantity(value, unit)
        return

    def pow(self, nom: int, denom: int) -> "Quantity":
        """Raises the value and the Unit to the power nom/denom use the ** operator to raise to round integer values."""
        return self.cq.pow(nom, denom)

    def sqrt(self) -> "Quantity":
        """Takes the square root of the value and the Unit."""
        return self.cq.sqrt()

    @property
    def unit(self) -> cu.Unit:
        """
        The physical Unit pertaining to the quantity."""
        return self.cq.unit

    @property
    def value(self):
        """The value portion of the quantity."""
        return self.cq.value


class Unit:
    """Class representing a physical unit."""

    def __init__(self, unit: str):
        self.u = unit
        return

    @staticmethod
    def decode(arg0: str) -> cu.Unit:
        """Deserializes the given string to a Unit"""
        return cu.Unit.decode(arg0)

    def encode(self) -> str:
        """Serializes the Unit to a string"""
        return self.u.encode()

    def get_symbol(self) -> str:
        """Returns the Unit"""
        return self.u.get_symbol()

    def inSI(self) -> cu.Unit:
        """Returns the equivalent quantity expressed in strict SI-units."""
        return self.u.inSI()

    def pow(self, nom: int, denom: int) -> cu.Unit:
        """Raises the value and the Unit to the power nom/denom use the ** operator to raise to round integer values."""
        return self.u.pow(nom, denom)

    def simplify(self) -> cu.Unit:
        """Tries to simplify the value and unit."""
        return self.u.simplify()


def convert_value(value: object, from_unit: Unit, to_unit: Unit) -> object:
    """Converts a value expressed in from_unit to to_unit"""
    return cu.convert_value(value, from_unit, to_unit)


def scaling_factor_to_SI(unit: Unit) -> float:
    """Compute scaling factor into equivalent SI unit.

    Parameters:
    -----------
    unit : Unit
        Simple or compound unit.
    Returns:
    -----------
    float
        numerical scaling factor for converting into SI units.
    """
    return cu.scaling_factor_to_SI(unit)
