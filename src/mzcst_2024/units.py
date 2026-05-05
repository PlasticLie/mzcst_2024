"""仿照`cst.units`，实现与之兼容的单位处理。"""

from __future__ import annotations

import cmath
import math
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from numbers import Number
from typing import Dict


class Unit:
    """Class representing a physical unit, compatible with `cst.units`.

    This class supports arithmetic operations to combine units, and can be used
    to create `Quantity` objects by multiplying with numerical values. It also
    supports conversion to SI units and simplification of compound units. The
    unit symbols are resolved from a registry, and the class can be extended by
    adding new units to the registry.

    Parameters
    ----------
    unit_name : str
        The symbol of the unit to create.
    dimensions : Dict[str, Decimal], optional
        The dimension vector of the unit, used for internal construction. This
        should not be provided by users directly, as it is intended for internal
        use when creating new units from arithmetic operations.
    factor : float, optional
        The scaling factor relative to the SI representation of the same
        dimensions, used for internal construction. This should not be provided
        by users directly, as it is intended for internal use when creating new
        units from arithmetic operations.
    """

    def __init__(
        self,
        unit_name: str,
        dimensions: Dict[str, Decimal] | None = None,
        factor: Decimal | Number = Decimal("1"),
    ):
        if dimensions is None:
            dims, factor, symbol = _resolve_unit_symbol(unit_name)
            self._dimensions = dims
            self._factor = factor
            self._symbol = symbol
        else:
            self._dimensions = {k: v for k, v in dimensions.items() if v != 0}
            self._factor = (
                factor if isinstance(factor, Decimal) else Decimal(str(factor))
            )
            self._symbol = unit_name

    @staticmethod
    def decode(arg0: str) -> "Unit":
        """Deserializes the given string to a `Unit`"""
        return Unit(arg0)

    def encode(self) -> str:
        """Serializes the `Unit` to a string"""
        return self.get_symbol()

    def get_symbol(self) -> str:
        """Returns the `Unit` as a string symbol."""
        return self._symbol

    def inSI(self) -> "Unit":
        """Returns the equivalent quantity expressed in strict SI-units."""
        return Unit(
            _format_unit_symbol(self._dimensions),
            dimensions=self._dimensions,
            factor=1.0,
        )

    def pow(self, nom: int, denom: int) -> "Unit":
        """Raises the value and the `Unit` to the power nom/denom use the **
        operator to raise to round integer values."""
        if denom == 0:
            raise ZeroDivisionError("denom must not be zero")
        exponent = Decimal(nom) / Decimal(denom)
        dims = {k: v * exponent for k, v in self._dimensions.items()}
        try:
            factor = self._factor**exponent
        except InvalidOperation:
            # Fallback for cases where Decimal cannot represent the power directly.
            factor = Decimal(str(float(self._factor) ** float(exponent)))
        return Unit(
            _format_unit_symbol(dims),
            dimensions=dims,
            factor=factor,
        )

    def simplify(self) -> "Unit":
        """Tries to simplify the value and unit."""
        known = _find_registered_unit(self._dimensions, self._factor)
        if known:
            return Unit(
                known[0], dimensions=self._dimensions, factor=self._factor
            )
        return Unit(
            _format_unit_symbol(self._dimensions),
            dimensions=self._dimensions,
            factor=self._factor,
        )

    def __mul__(self, other: "Unit") -> "Unit":
        if not isinstance(other, Unit):
            return NotImplemented
        dims = dict(self._dimensions)
        for key, value in other._dimensions.items():
            dims[key] = dims.get(key, Decimal(0)) + value
            if dims[key] == 0:
                del dims[key]
        factor = self._factor * other._factor
        known = _find_registered_unit(dims, factor)
        if known:
            symbol, factor = known
        else:
            symbol = f"{self._symbol}*{other._symbol}"
        return Unit(symbol, dimensions=dims, factor=factor)

    def __truediv__(self, other: "Unit") -> "Unit":
        if not isinstance(other, Unit):
            return NotImplemented
        dims = dict(self._dimensions)
        for key, value in other._dimensions.items():
            dims[key] = dims.get(key, Decimal(0)) - value
            if dims[key] == 0:
                del dims[key]
        factor = self._factor / other._factor
        known = _find_registered_unit(dims, factor)
        if known:
            symbol, factor = known
        else:
            symbol = f"{self._symbol}/{other._symbol}"
        return Unit(symbol, dimensions=dims, factor=factor)

    def __pow__(self, power: int) -> "Unit":
        return self.pow(power, 1)

    def __rmul__(self, value: Number) -> "Quantity":
        if not isinstance(value, Number):
            return NotImplemented
        return Quantity(value, self)

    def __str__(self) -> str:
        return self.get_symbol()

    def __repr__(self) -> str:
        dims_repr = (
            f", dimensions={self._dimensions!r}" if self._dimensions else ""
        )
        factor_repr = (
            f", factor={self._factor!r}" if self._factor != 1.0 else ""
        )
        return f"Unit('{self.get_symbol()}'{dims_repr}{factor_repr})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Unit):
            return False
        return (
            self._dimensions == other._dimensions
            and self._factor == other._factor
        )

    @property
    def dims(self) -> Dict[str, Decimal]:
        """Dimension vector in SI base dimensions.

        `cst.units.Unit`不包含本属性，用户代码中不应直接访问此属性。
        """
        return dict(self._dimensions)

    @property
    def factor(self) -> Decimal:
        """Scaling factor relative to SI representation of the same dimensions.

        `cst.units.Unit`不包含本属性，用户代码中不应直接访问此属性。
        """
        return self._factor

    @property
    def symbol(self) -> str:
        """Symbol of the unit.

        `cst.units.Unit`不包含本属性，用户代码中不应直接访问此属性，而应使用 `get_symbol()` 方法获取单位的符号表示。
        """
        return self._symbol


@dataclass(frozen=True)
class Quantity:
    """Class representing a physical quantity, which is a value associated with a unit.

    This class supports arithmetic operations with automatic unit conversion
    when necessary, compatible with `cst.units.Quantity`.

    Returns
    -------
    Quantity
        The converted quantity.

    Raises
    ------
    ValueError
        If the units are not compatible for conversion.
    """

    value: Number
    unit: Unit

    @classmethod
    def from_string(cls, text: str) -> "Quantity":
        """Builds a quantity from a string like ``"1.234 mm"``.

        Parameters
        ----------
        text : str
            A string containing a numeric value and a unit symbol separated by
            whitespace, for example ``"1.234 mm"``.

        Returns
        -------
        Quantity
            Parsed quantity instance.

        Raises
        ------
        ValueError
            If the input does not match the required format or contains an
            unknown unit symbol.
        """
        raw = text.strip()
        if not raw:
            raise ValueError("Input string must not be empty")

        parts = raw.split(maxsplit=1)
        if len(parts) != 2:
            raise ValueError(
                "Invalid quantity format. Expected '<value> <unit>', e.g. '1.234 mm'"
            )

        value_str, unit_str = parts
        try:
            value = float(value_str)
        except ValueError as exc:
            raise ValueError(f"Invalid numeric value: '{value_str}'") from exc

        return cls(value, Unit(unit_str.strip()))

    def convert_to(self, dest_unit: Unit) -> "Quantity":
        """Converts the quantity to a different unit.

        Parameters
        ----------
        dest_unit : Unit
            The unit to convert to.

        Returns
        -------
        Quantity
            The converted quantity.

        Raises
        ------
        ValueError
            If the units are not compatible for conversion.
        """
        if self.unit.dims != dest_unit.dims:
            raise ValueError(
                f"Cannot convert from '{self.unit.get_symbol()}' to '{dest_unit.get_symbol()}'"
            )
        scale = self.unit.factor / dest_unit.factor
        return Quantity(_multiply_by_scale(self.value, scale), dest_unit)

    def __add__(self, other: "Quantity") -> "Quantity":
        if not isinstance(other, Quantity):
            return NotImplemented
        converted = other.convert_to(self.unit)
        return Quantity(self.value + converted.value, self.unit)

    def __sub__(self, other: "Quantity") -> "Quantity":
        if not isinstance(other, Quantity):
            return NotImplemented
        converted = other.convert_to(self.unit)
        return Quantity(self.value - converted.value, self.unit)

    def __mul__(self, other: Number | "Quantity") -> "Quantity":
        if isinstance(other, Number):
            return Quantity(self.value * other, self.unit)
        if isinstance(other, Quantity):
            return Quantity(self.value * other.value, self.unit * other.unit)
        return NotImplemented

    def __truediv__(self, other: Number | "Quantity") -> "Quantity":
        if isinstance(other, Number):
            return Quantity(self.value / other, self.unit)
        if isinstance(other, Quantity):
            return Quantity(self.value / other.value, self.unit / other.unit)
        if isinstance(other, Unit):
            return Quantity(self.value, self.unit / other)
        return NotImplemented

    def __str__(self) -> str:
        return f"{self.value} {self.unit.get_symbol()}"

    def __repr__(self) -> str:
        return f"Quantity(value={self.value!r}, unit={self.unit!r})"

    def __format__(self, format_spec):
        value_str = format(self.value, format_spec)
        return f"{value_str} {self.unit.get_symbol()}"

    def __eq__(self, other):
        """Checks for approximate equality of two quantities, considering unit conversion."""
        if not isinstance(other, Quantity):
            return NotImplemented
        try:
            converted = other.convert_to(self.unit)
        except ValueError:
            return False

        if isinstance(self.value, complex) or isinstance(
            converted.value, complex
        ):
            return cmath.isclose(self.value, converted.value)
        return math.isclose(self.value, converted.value)


class ComplexQuantity(Quantity):
    """A quantity with a complex value, compatible with `cst.units.ComplexQuantity`.

    This is a simple extension of `Quantity` to allow for complex values, which
    can be useful in certain contexts such as AC circuit analysis or quantum
    mechanics.

    Parameters
    ----------
    value : complex
        The complex value of the quantity.
    unit : Unit
        The unit of the quantity.
    """

    value: complex


def convert_value(value: Number, from_unit: Unit, to_unit: Unit) -> Number:
    """Converts a value expressed in from_unit to to_unit.

    Parameters
    ----------
    value : Number
        The numerical value to convert.
    from_unit : Unit
        The unit of the input value.
    to_unit : Unit
        The unit to convert to.

    Returns
    -------
    Number
        The converted numerical value.
    Raises
    ------
    ValueError
        If the units are not compatible for conversion.
    """
    return Quantity(value, from_unit).convert_to(to_unit).value


def scaling_factor_to_SI(unit: Unit) -> Decimal:
    """Compute scaling factor into equivalent SI unit.

    Parameters
    ----------
    unit : Unit
        Simple or compound unit.

    Returns
    -------
    Decimal
        numerical scaling factor for converting into SI units.
    """
    return convert_value(Decimal("1"), unit, unit.inSI())


def _multiply_by_scale(value: Number, scale: Decimal) -> Number:
    """Multiplies a numeric value by a Decimal scale while keeping numeric compatibility."""
    if isinstance(value, Decimal):
        return value * scale
    if isinstance(value, complex):
        return value * float(scale)
    return value * float(scale)


def _format_power(power: Decimal) -> str:
    """Formats the power for a unit symbol.

    Parameters
    ----------
    power : Decimal
        The power to format.

    Returns
    -------
    str
        The formatted power as a string.
    """
    if power == 1:
        return ""
    if power.denominator == 1:
        return f"^{power.numerator}"
    return f"^({power.numerator}/{power.denominator})"


def _format_unit_symbol(dims: Dict[str, Decimal]) -> str:
    """Formats a unit symbol from its dimension vector.

    Parameters
    ----------
    dims : Dict[str, Decimal]
        The dimension vector of the unit.

    Returns
    -------
    str
        The formatted unit symbol as a string.
    """
    if not dims:
        return "1"
    num_terms: list[str] = []
    den_terms: list[str] = []
    for base in sorted(dims):
        power = dims[base]
        if power > 0:
            num_terms.append(f"{base}{_format_power(power)}")
        elif power < 0:
            den_terms.append(f"{base}{_format_power(-power)}")
    num_str = "*".join(num_terms) if num_terms else "1"
    if not den_terms:
        return num_str
    return f"{num_str}/{'*'.join(den_terms)}"


def _find_registered_unit(
    dims: Dict[str, Decimal], factor: Decimal
) -> tuple[str, Decimal] | None:
    """Find a registered unit matching the given dimensions and factor.

    Returns (symbol, factor) if found, None otherwise.
    """
    for reg_dims, reg_factor, reg_symbol in _UNIT_REGISTRY.values():
        if reg_dims == dims and reg_factor == factor:
            return reg_symbol, reg_factor
    return None


def _resolve_unit_symbol(unit: str) -> tuple[Dict[str, Decimal], Decimal, str]:
    """Resolves a unit symbol to its dimensions, factor, and canonical symbol.

    Parameters
    ----------
    unit : str
        The unit symbol to resolve.

    Returns
    -------
    tuple[Dict[str, Decimal], Decimal, str]
        A tuple containing the dimensions, factor, and canonical symbol of the unit.

    Raises
    ------
    ValueError
        If the unit symbol is not found in the registry.
    """
    if unit not in _UNIT_REGISTRY:
        raise ValueError(f"Unknown unit symbol: {unit}")
    dims, factor, symbol = _UNIT_REGISTRY[unit]
    return dict(dims), factor, symbol


_UNIT_REGISTRY: Dict[str, tuple[Dict[str, Decimal], Decimal, str]] = {}


def _register(
    symbol: str,
    dims: Dict[str, Decimal],
    factor: Decimal | Number = Decimal(1),
) -> None:
    """Registers a unit in the unit registry.

    Parameters
    ----------
    symbol : str
        The symbol of the unit.

    dims : Dict[str, Decimal]
        The dimensions of the unit.
    factor : float, optional
        The conversion factor to the base unit, by default 1.0
    """
    _UNIT_REGISTRY[symbol] = (
        dict(dims),
        factor if isinstance(factor, Decimal) else Decimal(factor),
        symbol,
    )


# Time and length convenience units


#######################################
# region SI base Units
# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

_register("m", {"m": Decimal(1)})
_register("kg", {"kg": Decimal(1)})
_register("s", {"s": Decimal(1)})
_register("A", {"A": Decimal(1)})
_register("K", {"K": Decimal(1)})
_register("mol", {"mol": Decimal(1)})
_register("cd", {"cd": Decimal(1)})

m = Unit("m")
kg = Unit("kg")
s = Unit("s")
A = Unit("A")
K = Unit("K")
mol = Unit("mol")
cd = Unit("cd")

# endregion
# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑


#######################################
# region Dimensionless and angular units
# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

_register("one", {})
_register("rad", {})
_register("sr", {})
_register("degree", {}, 3.141592653589793 / 180.0)

one = Unit("one")
rad = Unit("rad")
sr = Unit("sr")
degree = Unit("degree")

# endregion
# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑


#######################################
# region SI derived units with special names and symbols
# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

_register("Hz", {"s": Decimal(-1)})
_register("N", {"kg": Decimal(1), "m": Decimal(1), "s": Decimal(-2)})
_register("Pa", {"kg": Decimal(1), "m": Decimal(-1), "s": Decimal(-2)})
_register("J", {"kg": Decimal(1), "m": Decimal(2), "s": Decimal(-2)})
_register("W", {"kg": Decimal(1), "m": Decimal(2), "s": Decimal(-3)})
_register("C", {"A": Decimal(1), "s": Decimal(1)})
_register(
    "V",
    {"kg": Decimal(1), "m": Decimal(2), "s": Decimal(-3), "A": Decimal(-1)},
)
_register(
    "Ohm",
    {"kg": Decimal(1), "m": Decimal(2), "s": Decimal(-3), "A": Decimal(-2)},
)
_register(
    "S",
    {"kg": Decimal(-1), "m": Decimal(-2), "s": Decimal(3), "A": Decimal(2)},
)
_register(
    "F",
    {"kg": Decimal(-1), "m": Decimal(-2), "s": Decimal(4), "A": Decimal(2)},
)
_register(
    "H",
    {"kg": Decimal(1), "m": Decimal(2), "s": Decimal(-2), "A": Decimal(-2)},
)
_register(
    "Wb",
    {"kg": Decimal(1), "m": Decimal(2), "s": Decimal(-2), "A": Decimal(-1)},
)
_register("T", {"kg": Decimal(1), "s": Decimal(-2), "A": Decimal(-1)})

Hz = Unit("Hz")
N = Unit("N")
Pa = Unit("Pa")
J = Unit("J")
W = Unit("W")
C = Unit("C")
V = Unit("V")
Ohm = Unit("Ohm")
S = Unit("S")
F = Unit("F")
H = Unit("H")
Wb = Unit("Wb")
T = Unit("T")

# endregion
# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑


#######################################
# region SI prefixes
# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

_register("yotta", {}, Decimal("1e24"))
_register("zetta", {}, Decimal("1e21"))
_register("exa", {}, Decimal("1e18"))
_register("peta", {}, Decimal("1e15"))
_register("tera", {}, Decimal("1e12"))
_register("giga", {}, Decimal("1e9"))
_register("mega", {}, Decimal("1e6"))
_register("kilo", {}, Decimal("1e3"))
_register("deci", {}, Decimal("1e-1"))
_register("centi", {}, Decimal("1e-2"))
_register("milli", {}, Decimal("1e-3"))
_register("micro", {}, Decimal("1e-6"))
_register("nano", {}, Decimal("1e-9"))
_register("pico", {}, Decimal("1e-12"))
_register("femto", {}, Decimal("1e-15"))
_register("atto", {}, Decimal("1e-18"))
_register("zepto", {}, Decimal("1e-21"))

yotta = Unit("yotta")
zetta = Unit("zetta")
exa = Unit("exa")
peta = Unit("peta")
tera = Unit("tera")
giga = Unit("giga")
mega = Unit("mega")
kilo = Unit("kilo")
deci = Unit("deci")
centi = Unit("centi")
milli = Unit("milli")
micro = Unit("micro")
nano = Unit("nano")
pico = Unit("pico")
femto = Unit("femto")
atto = Unit("atto")
zepto = Unit("zepto")

# endregion
# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑


#######################################
# region length units
# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

_register("km", {"m": Decimal(1)}, Decimal("1e3"))
_register("cm", {"m": Decimal(1)}, Decimal("1e-2"))
_register("mm", {"m": Decimal(1)}, Decimal("1e-3"))
_register("μm", {"m": Decimal(1)}, Decimal("1e-6"))
_register("um", {"m": Decimal(1)}, Decimal("1e-6"))
_register("nm", {"m": Decimal(1)}, Decimal("1e-9"))
_register("pm", {"m": Decimal(1)}, Decimal("1e-12"))

_register("mil", {"m": Decimal(1)}, Decimal("2.54e-5"))
_register("inch", {"m": Decimal(1)}, Decimal("0.0254"))
_register("foot", {"m": Decimal(1)}, Decimal("0.3048"))
_register("yard", {"m": Decimal(1)}, Decimal("0.9144"))
_register("mile", {"m": Decimal(1)}, Decimal("1609.344"))

_register("angstrom", {"m": Decimal(1)}, Decimal("1e-10"))

km = Unit("km")
cm = Unit("cm")
mm = Unit("mm")
um = Unit("μm")
μm = um  # pylint: disable=non-ascii-name
nm = Unit("nm")
pm = Unit("pm")

mil = Unit("mil")
inch = Unit("inch")
foot = Unit("foot")
yard = Unit("yard")
mile = Unit("mile")

angstrom = Unit("angstrom")

# endregion
# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑


#######################################
# region area units
# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

_register("km^2", {"m": Decimal(2)}, Decimal("1e6"))
_register("ha", {"m": Decimal(2)}, Decimal("1e4"))
_register("m^2", {"m": Decimal(2)}, Decimal("1.0"))
_register("cm^2", {"m": Decimal(2)}, Decimal("1e-4"))
_register("mm^2", {"m": Decimal(2)}, Decimal("1e-6"))

_register("acre", {"m": Decimal(2)}, Decimal("4046.8564224"))

km2 = Unit("km^2")
ha = Unit("ha")
m2 = Unit("m^2")
cm2 = Unit("cm^2")
mm2 = Unit("mm^2")

acre = Unit("acre")

# endregion
# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑


#######################################
# region volume units
# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

_register("m^3", {"m": Decimal(3)}, Decimal("1.0"))
_register("cm^3", {"m": Decimal(3)}, Decimal("1e-6"))

_register("L", {"m": Decimal(3)}, Decimal("1e-3"))
_register("mL", {"m": Decimal(3)}, Decimal("1e-6"))

m3 = Unit("m^3")
cm3 = Unit("cm^3")

L = Unit("L")
mL = Unit("mL")

# endregion
# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑


#######################################
# region Mass units
# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

_register("g", {"kg": Decimal(1)}, Decimal("1e-3"))
_register("mg", {"kg": Decimal(1)}, Decimal("1e-6"))
_register("ug", {"kg": Decimal(1)}, Decimal("1e-9"))

g = Unit("g")
mg = Unit("mg")
ug = Unit("ug")

# endregion
# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑


#######################################
# region Time units
# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

_register("min", {"s": Decimal(1)}, Decimal("60"))
_register("hour", {"s": Decimal(1)}, Decimal("3600"))
_register("day", {"s": Decimal(1)}, Decimal("86400"))

minute = Unit("min")
hour = Unit("hour")
day = Unit("day")

_register("ps", {"s": Decimal(1)}, Decimal("1e-12"))
_register("ns", {"s": Decimal(1)}, Decimal("1e-9"))
_register("us", {"s": Decimal(1)}, Decimal("1e-6"))
_register("ms", {"s": Decimal(1)}, Decimal("1e-3"))

ps = Unit("ps")
ns = Unit("ns")
us = Unit("us")
ms = Unit("ms")

# endregion
# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

#######################################
# region frequency units
# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

_register("kHz", {"s": Decimal(-1)}, Decimal("1e3"))
_register("MHz", {"s": Decimal(-1)}, Decimal("1e6"))
_register("GHz", {"s": Decimal(-1)}, Decimal("1e9"))
_register("THz", {"s": Decimal(-1)}, Decimal("1e12"))

kHz = Unit("kHz")
MHz = Unit("MHz")
GHz = Unit("GHz")
THz = Unit("THz")

# endregion
# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑


#######################################
# region temperature units
# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

_register("degC", {"K": Decimal(1)}, Decimal("1"))
_register("degF", {"K": Decimal(1)}, Decimal("5") / Decimal("9"))

degC = Unit("degC")
degF = Unit("degF")

# endregion
# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑


#######################################
# region force units
# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

_register(
    "kN", {"kg": Decimal(1), "m": Decimal(1), "s": Decimal(-2)}, Decimal("1e3")
)

kN = Unit("kN")

# endregion
# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

#######################################
# region pressure units
# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

_register(
    "Pa", {"kg": Decimal(1), "m": Decimal(-1), "s": Decimal(-2)}, Decimal("1")
)
_register(
    "hPa",
    {"kg": Decimal(1), "m": Decimal(-1), "s": Decimal(-2)},
    Decimal("100"),
)
_register(
    "kPa",
    {"kg": Decimal(1), "m": Decimal(-1), "s": Decimal(-2)},
    Decimal("1e3"),
)
_register(
    "bar",
    {"kg": Decimal(1), "m": Decimal(-1), "s": Decimal(-2)},
    Decimal("1e5"),
)
_register(
    "MPa",
    {"kg": Decimal(1), "m": Decimal(-1), "s": Decimal(-2)},
    Decimal("1e6"),
)

_register(
    "psi",
    {"kg": Decimal(1), "m": Decimal(-1), "s": Decimal(-2)},
    Decimal("6894.75729"),
)
_register(
    "mmHg",
    {"kg": Decimal(1), "m": Decimal(-1), "s": Decimal(-2)},
    Decimal("133.322368"),
)

Pa = Unit("Pa")
hPa = Unit("hPa")
kPa = Unit("kPa")
bar_ = Unit("bar")
MPa = Unit("MPa")

psi = Unit("psi")
mmHg = Unit("mmHg")

# endregion
# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

#######################################
# region energy units
# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

_register(
    "kJ", {"kg": Decimal(1), "m": Decimal(2), "s": Decimal(-2)}, Decimal("1e3")
)
_register(
    "MJ", {"kg": Decimal(1), "m": Decimal(2), "s": Decimal(-2)}, Decimal("1e6")
)
_register(
    "GJ", {"kg": Decimal(1), "m": Decimal(2), "s": Decimal(-2)}, Decimal("1e9")
)

_register(
    "eV",
    {"kg": Decimal(1), "m": Decimal(2), "s": Decimal(-2)},
    Decimal("1.602176634e-19"),
)
_register(
    "keV",
    {"kg": Decimal(1), "m": Decimal(2), "s": Decimal(-2)},
    Decimal("1.602176634e-16"),
)
_register(
    "MeV",
    {"kg": Decimal(1), "m": Decimal(2), "s": Decimal(-2)},
    Decimal("1.602176634e-13"),
)
_register(
    "GeV",
    {"kg": Decimal(1), "m": Decimal(2), "s": Decimal(-2)},
    Decimal("1.602176634e-10"),
)
_register(
    "TeV",
    {"kg": Decimal(1), "m": Decimal(2), "s": Decimal(-2)},
    Decimal("1.602176634e-7"),
)

kJ = Unit("kJ")
MJ = Unit("MJ")
GJ = Unit("GJ")

eV = Unit("eV")
keV = Unit("keV")
MeV = Unit("MeV")
GeV = Unit("GeV")
TeV = Unit("TeV")

# endregion
# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

#######################################
# region power units
# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

_register(
    "kW", {"kg": Decimal(1), "m": Decimal(2), "s": Decimal(-3)}, Decimal("1e3")
)
_register(
    "MW", {"kg": Decimal(1), "m": Decimal(2), "s": Decimal(-3)}, Decimal("1e6")
)
_register(
    "GW", {"kg": Decimal(1), "m": Decimal(2), "s": Decimal(-3)}, Decimal("1e9")
)

kW = Unit("kW")
MW = Unit("MW")
GW = Unit("GW")

# endregion
# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑


#######################################
# region Electrical units
# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

_register("kA", {"A": Decimal(1)}, Decimal("1e3"))
_register("mA", {"A": Decimal(1)}, Decimal("1e-3"))
_register("uA", {"A": Decimal(1)}, Decimal("1e-6"))

kA = Unit("kA")
mA = Unit("mA")
uA = Unit("uA")

_register(
    "kV",
    {"kg": Decimal(1), "m": Decimal(2), "s": Decimal(-3), "A": Decimal(-1)},
    Decimal("1e3"),
)
_register(
    "mV",
    {"kg": Decimal(1), "m": Decimal(2), "s": Decimal(-3), "A": Decimal(-1)},
    Decimal("1e-3"),
)
_register(
    "uV",
    {"kg": Decimal(1), "m": Decimal(2), "s": Decimal(-3), "A": Decimal(-1)},
    Decimal("1e-6"),
)

kV = Unit("kV")
mV = Unit("mV")
uV = Unit("uV")


# endregion
# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑


#######################################
# region radioactivity and radiation units
# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓


_register("Bq", {"s": Decimal(-1)}, Decimal(1))
Bq = Unit("Bq")

_register(
    "Sv", {"kg": Decimal(1), "m": Decimal(2), "s": Decimal(-2)}, Decimal(1)
)
Sv = Unit("Sv")

_register(
    "Gy", {"kg": Decimal(1), "m": Decimal(2), "s": Decimal(-2)}, Decimal(1)
)
Gy = Unit("Gy")


# endregion
# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

#######################################
# region data types
# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

_register("bit", {}, Decimal(1))
_register("byte", {}, Decimal(8))
bit = Unit("bit")
byte = Unit("byte")

_register("kibi", {}, Decimal(1024))
_register("mebi", {}, Decimal(1024**2))
_register("gibi", {}, Decimal(1024**3))
_register("tebi", {}, Decimal(1024**4))
_register("pebi", {}, Decimal(1024**5))

kibi = Unit("kibi")
mebi = Unit("mebi")
gibi = Unit("gibi")
tebi = Unit("tebi")
pebi = Unit("pebi")

# endregion
# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑


# Keep compatibility with cst.units naming without redefining built-in by assignment.
globals()["min"] = minute
