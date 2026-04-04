"""仿照`cst.units`，实现与之兼容的单位处理。

"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from numbers import Number
from typing import Dict


class Unit:
    """Class representing a physical unit.
    """

    def __init__(
        self,
        unit: str,
        *,
        _dims: Dict[str, Fraction] | None = None,
        _factor: float = 1.0,
        _symbol: str | None = None,
    ):
        if _dims is None:
            dims, factor, symbol = _resolve_unit_symbol(unit)
            self._dims = dims
            self._factor = factor
            self._symbol = symbol
        else:
            self._dims = {k: v for k, v in _dims.items() if v != 0}
            self._factor = float(_factor)
            self._symbol = _symbol or _format_unit_symbol(self._dims)

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
            _format_unit_symbol(self._dims),
            _dims=self._dims,
            _factor=1.0,
            _symbol=_format_unit_symbol(self._dims),
        )

    def pow(self, nom: int, denom: int) -> "Unit":
        """Raises the value and the `Unit` to the power nom/denom use the ** operator to raise to round integer values."""
        if denom == 0:
            raise ZeroDivisionError("denom must not be zero")
        p = Fraction(nom, denom)
        dims = {k: v * p for k, v in self._dims.items()}
        return Unit(
            _format_unit_symbol(dims),
            _dims=dims,
            _factor=self._factor ** float(p),
            _symbol=_format_unit_symbol(dims),
        )

    def simplify(self) -> "Unit":
        """Tries to simplify the value and unit."""
        return Unit(
            _format_unit_symbol(self._dims),
            _dims=self._dims,
            _factor=self._factor,
            _symbol=_format_unit_symbol(self._dims),
        )

    def __mul__(self, other: "Unit") -> "Unit":
        if not isinstance(other, Unit):
            return NotImplemented
        dims = dict(self._dims)
        for key, value in other._dims.items():
            dims[key] = dims.get(key, Fraction(0)) + value
            if dims[key] == 0:
                del dims[key]
        return Unit(
            _format_unit_symbol(dims),
            _dims=dims,
            _factor=self._factor * other._factor,
            _symbol=_format_unit_symbol(dims),
        )

    def __truediv__(self, other: "Unit") -> "Unit":
        if not isinstance(other, Unit):
            return NotImplemented
        dims = dict(self._dims)
        for key, value in other._dims.items():
            dims[key] = dims.get(key, Fraction(0)) - value
            if dims[key] == 0:
                del dims[key]
        return Unit(
            _format_unit_symbol(dims),
            _dims=dims,
            _factor=self._factor / other._factor,
            _symbol=_format_unit_symbol(dims),
        )

    def __pow__(self, power: int) -> "Unit":
        return self.pow(power, 1)

    def __rmul__(self, value: Number) -> "Quantity":
        if not isinstance(value, Number):
            return NotImplemented
        return Quantity(value, self)

    def __str__(self) -> str:
        return self.get_symbol()

    def __repr__(self) -> str:
        return f"Unit('{self.get_symbol()}')"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Unit):
            return False
        return self._dims == other._dims and self._factor == other._factor

    @property
    def dims(self) -> Dict[str, Fraction]:
        """Dimension vector in SI base dimensions."""
        return dict(self._dims)

    @property
    def factor(self) -> float:
        """Scaling factor relative to SI representation of the same dimensions."""
        return self._factor


@dataclass(frozen=True)
class Quantity:
    value: Number
    unit: Unit

    def convert_to(self, dest_unit: Unit) -> "Quantity":
        if self.unit.dims != dest_unit.dims:
            raise ValueError(
                f"Cannot convert from '{self.unit.get_symbol()}' to '{dest_unit.get_symbol()}'"
            )
        scale = self.unit.factor / dest_unit.factor
        return Quantity(self.value * scale, dest_unit)

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
        return NotImplemented

    def __str__(self) -> str:
        return f"{self.value} {self.unit.get_symbol()}"

    def __repr__(self) -> str:
        return f"Quantity(value={self.value!r}, unit={self.unit!r})"


def convert_value(value: object, from_unit: Unit, to_unit: Unit) -> object:
    """Converts a value expressed in from_unit to to_unit"""
    return Quantity(value, from_unit).convert_to(to_unit).value


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
    return float(convert_value(1.0, unit, unit.inSI()))


def _format_power(power: Fraction) -> str:
    if power == 1:
        return ""
    if power.denominator == 1:
        return f"^{power.numerator}"
    return f"^({power.numerator}/{power.denominator})"


def _format_unit_symbol(dims: Dict[str, Fraction]) -> str:
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


def _resolve_unit_symbol(unit: str) -> tuple[Dict[str, Fraction], float, str]:
    if unit not in _UNIT_REGISTRY:
        raise ValueError(f"Unknown unit symbol: {unit}")
    dims, factor, symbol = _UNIT_REGISTRY[unit]
    return dict(dims), factor, symbol


def _register(symbol: str, dims: Dict[str, Fraction], factor: float = 1.0) -> None:
    _UNIT_REGISTRY[symbol] = (dict(dims), float(factor), symbol)


_UNIT_REGISTRY: Dict[str, tuple[Dict[str, Fraction], float, str]] = {}

# SI base units
_register("one", {})
_register("m", {"m": Fraction(1)})
_register("kg", {"kg": Fraction(1)})
_register("s", {"s": Fraction(1)})
_register("A", {"A": Fraction(1)})
_register("K", {"K": Fraction(1)})
_register("mol", {"mol": Fraction(1)})
_register("cd", {"cd": Fraction(1)})

# Common derived units
_register("Hz", {"s": Fraction(-1)})
_register("N", {"kg": Fraction(1), "m": Fraction(1), "s": Fraction(-2)})
_register("Pa", {"kg": Fraction(1), "m": Fraction(-1), "s": Fraction(-2)})
_register("J", {"kg": Fraction(1), "m": Fraction(2), "s": Fraction(-2)})
_register("W", {"kg": Fraction(1), "m": Fraction(2), "s": Fraction(-3)})
_register("C", {"A": Fraction(1), "s": Fraction(1)})
_register("V", {"kg": Fraction(1), "m": Fraction(2), "s": Fraction(-3), "A": Fraction(-1)})
_register("Ohm", {"kg": Fraction(1), "m": Fraction(2), "s": Fraction(-3), "A": Fraction(-2)})
_register("S", {"kg": Fraction(-1), "m": Fraction(-2), "s": Fraction(3), "A": Fraction(2)})
_register("F", {"kg": Fraction(-1), "m": Fraction(-2), "s": Fraction(4), "A": Fraction(2)})
_register("H", {"kg": Fraction(1), "m": Fraction(2), "s": Fraction(-2), "A": Fraction(-2)})
_register("Wb", {"kg": Fraction(1), "m": Fraction(2), "s": Fraction(-2), "A": Fraction(-1)})
_register("T", {"kg": Fraction(1), "s": Fraction(-2), "A": Fraction(-1)})

# Time and length convenience units
_register("min", {"s": Fraction(1)}, 60.0)
_register("hour", {"s": Fraction(1)}, 3600.0)
_register("day", {"s": Fraction(1)}, 86400.0)
_register("km", {"m": Fraction(1)}, 1e3)
_register("cm", {"m": Fraction(1)}, 1e-2)
_register("mm", {"m": Fraction(1)}, 1e-3)
_register("um", {"m": Fraction(1)}, 1e-6)
_register("nm", {"m": Fraction(1)}, 1e-9)
_register("pm", {"m": Fraction(1)}, 1e-12)
_register("mil", {"m": Fraction(1)}, 2.54e-5)

# Mass and electrical prefixes used often
_register("g", {"kg": Fraction(1)}, 1e-3)
_register("mg", {"kg": Fraction(1)}, 1e-6)
_register("ug", {"kg": Fraction(1)}, 1e-9)
_register("kA", {"A": Fraction(1)}, 1e3)
_register("mA", {"A": Fraction(1)}, 1e-3)
_register("uA", {"A": Fraction(1)}, 1e-6)

# Exported constants
one = Unit("one")
m = Unit("m")
kg = Unit("kg")
s = Unit("s")
A = Unit("A")
K = Unit("K")
mol = Unit("mol")
cd = Unit("cd")

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

minute = Unit("min")
hour = Unit("hour")
day = Unit("day")
km = Unit("km")
cm = Unit("cm")
mm = Unit("mm")
um = Unit("um")
nm = Unit("nm")
pm = Unit("pm")
mil = Unit("mil")

g = Unit("g")
mg = Unit("mg")
ug = Unit("ug")
kA = Unit("kA")
mA = Unit("mA")
uA = Unit("uA")

# Keep compatibility with cst.units naming without redefining built-in by assignment.
globals()["min"] = minute

__all__ = [
    "Unit",
    "Quantity",
    "convert_value",
    "scaling_factor_to_SI",
    "one",
    "m",
    "kg",
    "s",
    "A",
    "K",
    "mol",
    "cd",
    "Hz",
    "N",
    "Pa",
    "J",
    "W",
    "C",
    "V",
    "Ohm",
    "S",
    "F",
    "H",
    "Wb",
    "T",
    "minute",
    "hour",
    "day",
    "km",
    "cm",
    "mm",
    "um",
    "nm",
    "pm",
    "mil",
    "g",
    "mg",
    "ug",
    "kA",
    "mA",
    "uA",
]


