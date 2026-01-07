"""test cst.units module

Only works in CST 2026.

It seems that the `cst.units` module provides a way to create physical 
quantities with units, but in CST 2024 and 2025, the module is not fully 
functional or documented. Therefore, this test script demonstrates how to use 
the `cst.units` module in CST 2026, where it appears to be more complete.
"""

from cst.units import A, Unit, V, W, mil, mm, um

# Create quantities with units
l1 = 2 * mm
l2 = 3 * um
l3 = 5 * mil
p1 = 20 * W
i1 = 5 * A
print(l1)  # prints "2 mm"
print(l2)  # prints "3 µm"
print(l3)  # prints "5 mil"
print(p1)  # prints "20 W"
print(i1)  # prints "5 A"

# Create quantities with string based unit, only string variants from the Predefined units table can be used.
alength = 42 * Unit("mm")
aspeed = (
    120 * Unit("km") / Unit("hour")
)  # Note that you cannot use "km/h" as it is not one of the predefined units
apower = 55 * Unit("GW")

# Compute derived quantities with automatic unit conversions
l4 = l1 + l2  # add "mm" and "µm" resulting in "mm"
l5 = l2 + l1  # add "µm" and "mm" resulting in "µm"
print(l4)  # prints "2.003 mm"
print(l5)  # prints "2003 µm"
u1 = p1 / i1  # divide "W" by "A" resulting in "V"
print(u1)  # prints "4 V"

# Enforce representation using a specific unit
l6 = l3.convert_to(um)
print(l6)  # prints "127 µm"

# Convert to float without unit
# Warning: Only do this, if the exact unit of the quantity is known.
#          Use "convert_to" to enforce a specific unit.
print(l3.value)  # prints "5"
print(l6.value)  # prints "127"
print(i1.value)  # prints "5"

import random

l7 = random.choice([l3, l6])  # result may use either "mil" or "µm"
print(l7.value)  # prints value with unknown/random unit
print(l7.convert_to(mm).value)  # prints value with known unit
