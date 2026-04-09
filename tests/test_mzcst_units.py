"""测试 mzcst_2024.units 模块

仿照 test_cst_unit.py，验证 mzcst_2024.units 与 cst.units 的行为兼容性。

由于 mzcst_2024.units 可能在 CST 2024 和 2025 中不完全功能或文档不全，因此本测试脚本主要
演示了在 CST 2026 中使用 mzcst_2024.units 的方式，并验证其行为与 test_cst_unit.py 中的演示一致。

# 测试方法：

在仓库根目录执行下面这组命令即可：

`conda activate mzcst-test`

`cd /Users/limengzi/Documents/GitHub/mzcst_2024`

`python -m unittest tests.test_mzcst_units -v`

如果你想只跑某一个测试类或方法，可以用：

## 只跑一个类
`python -m unittest tests.test_mzcst_units.TestConversion -v`

## 只跑一个方法
`python -m unittest tests.test_mzcst_units.TestConversion.test_mil_to_um -v`

"""

import math
import random
import unittest
from fractions import Fraction

import mzcst_2024.units as mu
from mzcst_2024.units import (
    A,
    C,
    ComplexQuantity,
    F,
    H,
    Hz,
    J,
    K,
    L,
    N,
    Ohm,
    Pa,
    Quantity,
    S,
    T,
    Unit,
    V,
    W,
    Wb,
    bit,
    byte,
    cd,
    cm,
    cm3,
    convert_value,
    day,
    degree,
    eV,
    g,
    hour,
    hPa,
    inch,
    kA,
    kg,
    kibi,
    km,
    kV,
    m,
    mA,
    mg,
    mil,
    mm,
    mol,
    nm,
    one,
    pm,
    rad,
    s,
    scaling_factor_to_SI,
    uA,
    ug,
    um,
)

# ---------------------------------------------------------------------------
# 基本量的创建
# ---------------------------------------------------------------------------


class TestQuantityCreation(unittest.TestCase):
    def test_length_mm(self):
        l1 = 2 * mm
        assert l1.value == 2
        assert l1.unit == mm

    def test_length_um(self):
        l2 = 3 * um
        assert l2.value == 3
        assert l2.unit == um

    def test_length_mil(self):
        l3 = 5 * mil
        assert l3.value == 5
        assert l3.unit == mil

    def test_power_W(self):
        p1 = 20 * W
        assert p1.value == 20
        assert p1.unit == W

    def test_current_A(self):
        i1 = 5 * A
        assert i1.value == 5
        assert i1.unit == A

    def test_str_representation(self):
        assert str(2 * mm) == "2 mm"
        assert str(3 * um) == "3 um"
        assert str(5 * mil) == "5 mil"
        assert str(20 * W) == "20 W"
        assert str(5 * A) == "5 A"


# ---------------------------------------------------------------------------
# 加减法与单位传播
# ---------------------------------------------------------------------------


class TestArithmetic(unittest.TestCase):
    def test_add_mm_um_result_in_mm(self):
        l4 = (2 * mm) + (3 * um)
        assert l4.unit == mm
        assert math.isclose(l4.value, 2.003, rel_tol=1e-9)

    def test_add_um_mm_result_in_um(self):
        l5 = (3 * um) + (2 * mm)
        assert l5.unit == um
        assert math.isclose(l5.value, 2003.0, rel_tol=1e-9)

    def test_sub_same_unit(self):
        result = (5 * mm) - (2 * mm)
        assert result.unit == mm
        assert math.isclose(result.value, 3.0, rel_tol=1e-9)

    def test_sub_cross_unit(self):
        result = (5 * mm) - (1000 * um)
        assert result.unit == mm
        assert math.isclose(result.value, 4.0, rel_tol=1e-9)

    def test_div_W_by_A_gives_V(self):
        u1 = (20 * W) / (5 * A)
        assert u1.unit.dims == V.dims
        assert math.isclose(u1.value, 4.0, rel_tol=1e-9)

    def test_mul_scalar(self):
        result = (3 * mm) * 2
        assert result.value == 6
        assert result.unit == mm

    def test_div_scalar(self):
        result = (6 * mm) / 2
        assert result.value == 3
        assert result.unit == mm

    def test_mul_quantities(self):
        force = 10 * N
        distance = 2 * m
        work = force * distance
        assert work.unit.dims == J.dims
        assert math.isclose(work.value, 20.0, rel_tol=1e-9)


# ---------------------------------------------------------------------------
# 单位转换
# ---------------------------------------------------------------------------


class TestConversion(unittest.TestCase):
    def test_mil_to_um(self):
        l3 = 5 * mil
        l6 = l3.convert_to(um)
        assert l6.unit == um
        assert math.isclose(l6.value, 127.0, rel_tol=1e-9)

    def test_mm_to_um(self):
        result = (1 * mm).convert_to(um)
        assert math.isclose(result.value, 1000.0, rel_tol=1e-9)

    def test_km_to_m(self):
        result = (1 * km).convert_to(m)
        assert math.isclose(result.value, 1000.0, rel_tol=1e-9)

    def test_cm_to_mm(self):
        result = (1 * cm).convert_to(mm)
        assert math.isclose(result.value, 10.0, rel_tol=1e-9)

    def test_hour_to_s(self):
        result = (1 * hour).convert_to(s)
        assert math.isclose(result.value, 3600.0, rel_tol=1e-9)

    def test_day_to_hour(self):
        result = (1 * day).convert_to(hour)
        assert math.isclose(result.value, 24.0, rel_tol=1e-9)

    def test_kA_to_A(self):
        result = (2 * kA).convert_to(A)
        assert math.isclose(result.value, 2000.0, rel_tol=1e-9)

    def test_mA_to_A(self):
        result = (500 * mA).convert_to(A)
        assert math.isclose(result.value, 0.5, rel_tol=1e-9)

    def test_incompatible_conversion_raises(self):
        with self.assertRaises(ValueError):
            (1 * mm).convert_to(s)

    def test_incompatible_conversion_message(self):
        with self.assertRaisesRegex(ValueError, "Cannot convert"):
            (1 * W).convert_to(m)

    def test_convert_value_function(self):
        result = convert_value(5.0, mil, um)
        assert math.isclose(result, 127.0, rel_tol=1e-9)

    def test_degree_to_rad(self):
        result = (180 * degree).convert_to(rad)
        assert math.isclose(result.value, math.pi, rel_tol=1e-9)

    def test_inch_to_mm(self):
        result = (1 * inch).convert_to(mm)
        assert math.isclose(result.value, 25.4, rel_tol=1e-9)

    def test_liter_to_cm3(self):
        result = (1 * L).convert_to(cm3)
        assert math.isclose(result.value, 1000.0, rel_tol=1e-9)

    def test_hpa_to_pa(self):
        result = (1 * hPa).convert_to(Pa)
        assert math.isclose(result.value, 100.0, rel_tol=1e-9)

    def test_ev_to_joule(self):
        result = (1 * eV).convert_to(J)
        assert math.isclose(result.value, 1.602176634e-19, rel_tol=1e-9)

    def test_kv_to_v(self):
        result = (2 * kV).convert_to(V)
        assert math.isclose(result.value, 2000.0, rel_tol=1e-9)

    def test_byte_to_bit(self):
        result = (1 * byte).convert_to(bit)
        assert math.isclose(result.value, 8.0, rel_tol=1e-9)

    def test_kibi_to_byte(self):
        result = (1 * kibi).convert_to(byte)
        assert math.isclose(result.value, 128.0, rel_tol=1e-9)


# ---------------------------------------------------------------------------
# .value 属性（已知单位下直接读取数值）
# ---------------------------------------------------------------------------


class TestValueAccess(unittest.TestCase):
    def test_value_mil(self):
        l3 = 5 * mil
        assert l3.value == 5

    def test_value_um_after_conversion(self):
        l6 = (5 * mil).convert_to(um)
        assert math.isclose(l6.value, 127.0, rel_tol=1e-9)

    def test_value_current(self):
        assert (5 * A).value == 5

    def test_convert_to_known_unit_then_read(self):

        l3 = 5 * mil
        l6 = l3.convert_to(um)
        l7 = random.choice([l3, l6])
        # 无论选哪个，转换到 mm 后值应相同
        assert math.isclose(l7.convert_to(mm).value, 0.127, rel_tol=1e-9)


# ---------------------------------------------------------------------------
# Unit 类本身
# ---------------------------------------------------------------------------


class TestUnit(unittest.TestCase):
    def test_unit_str(self):
        assert str(mm) == "mm"
        assert str(V) == "V"
        assert str(Hz) == "Hz"

    def test_unit_repr(self):
        r = repr(mm)
        assert r.startswith("Unit('mm'")
        assert "_dims=" in r
        assert "factor=" in r

    def test_unit_eq(self):
        assert Unit("mm") == Unit("mm")
        assert Unit("mm") != Unit("um")

    def test_unit_get_symbol(self):
        assert mm.get_symbol() == "mm"
        assert A.get_symbol() == "A"

    def test_unit_dims(self):

        assert mm.dims == {"m": Fraction(1)}
        assert A.dims == {"A": Fraction(1)}

    def test_unit_factor(self):
        assert math.isclose(mm.factor, 1e-3, rel_tol=1e-9)
        assert math.isclose(um.factor, 1e-6, rel_tol=1e-9)
        assert math.isclose(km.factor, 1e3, rel_tol=1e-9)

    def test_unit_mul(self):
        area_unit = m * m
        assert area_unit.dims == {"m": Fraction(2)}

    def test_unit_div(self):
        speed_unit = m / s
        assert speed_unit.dims == {"m": Fraction(1), "s": Fraction(-1)}

    def test_unit_pow(self):
        vol_unit = m**3
        assert vol_unit.dims == {"m": Fraction(3)}

    def test_unit_pow_fraction(self):
        sqrt_m = m.pow(1, 2)
        assert sqrt_m.dims == {"m": Fraction(1, 2)}

    def test_unit_pow_zero_denom_raises(self):
        with self.assertRaises(ZeroDivisionError):
            m.pow(1, 0)

    def test_unit_inSI(self):
        si = mm.inSI()
        assert math.isclose(si.factor, 1.0, rel_tol=1e-9)
        assert si.dims == mm.dims

    def test_unit_simplify(self):
        simplified = mm.simplify()
        assert simplified.dims == mm.dims
        assert math.isclose(simplified.factor, mm.factor, rel_tol=1e-9)

    def test_unit_decode_encode(self):
        u = Unit.decode("mm")
        assert u == mm
        assert u.encode() == "mm"

    def test_unknown_unit_raises(self):
        with self.assertRaisesRegex(ValueError, "Unknown unit symbol"):
            Unit("foobar")

    def test_unit_dimensionless_one(self):
        assert one.dims == {}

    def test_unit_decode_bar_symbol(self):
        pressure = Unit.decode("bar")
        assert pressure.dims == Pa.dims
        assert math.isclose(pressure.factor, 1e5, rel_tol=1e-9)


# ---------------------------------------------------------------------------
# ComplexQuantity
# ---------------------------------------------------------------------------


class TestComplexQuantity(unittest.TestCase):
    def test_complex_value_keeps_unit(self):
        z = ComplexQuantity(3 + 4j, Ohm)
        assert z.value == 3 + 4j
        assert z.unit == Ohm

    def test_complex_quantity_repr(self):
        z = ComplexQuantity(1 - 2j, V)
        assert "ComplexQuantity" not in repr(z)
        assert "Quantity(" in repr(z)


# ---------------------------------------------------------------------------
# 单位量纲测试
# ---------------------------------------------------------------------------


class TestUnitDimensions(unittest.TestCase):
    """验证复合单位运算后的量纲是否正确。"""

    def test_pressure_dims_from_force_over_area(self):
        pressure_unit = N / (m**2)
        assert pressure_unit.dims == Pa.dims

    def test_voltage_dims_from_power_over_current(self):
        voltage_unit = W / A
        assert voltage_unit.dims == V.dims

    def test_magnetic_flux_density_dims(self):
        magnetic_flux_density = Wb / (m**2)
        assert magnetic_flux_density.dims == T.dims

    def test_frequency_dims(self):
        assert Hz.dims == {"s": Fraction(-1)}

    def test_dimensionless_after_cancellation(self):
        dimless = m / m
        assert dimless.dims == {}

    def test_compound_unit_scaling_factor(self):
        speed_unit = km / hour
        si_speed = m / s
        result = convert_value(1.0, speed_unit, si_speed)
        assert math.isclose(result, 1000.0 / 3600.0, rel_tol=1e-9)


# ---------------------------------------------------------------------------
# scaling_factor_to_SI
# ---------------------------------------------------------------------------


class TestScalingFactor(unittest.TestCase):
    def test_mm_to_SI(self):
        assert math.isclose(scaling_factor_to_SI(mm), 1e-3, rel_tol=1e-9)

    def test_km_to_SI(self):
        assert math.isclose(scaling_factor_to_SI(km), 1e3, rel_tol=1e-9)

    def test_m_to_SI(self):
        assert math.isclose(scaling_factor_to_SI(m), 1.0, rel_tol=1e-9)

    def test_hour_to_SI(self):
        assert math.isclose(scaling_factor_to_SI(hour), 3600.0, rel_tol=1e-9)

    def test_mil_to_SI(self):
        assert math.isclose(scaling_factor_to_SI(mil), 2.54e-5, rel_tol=1e-9)


# ---------------------------------------------------------------------------
# 与 cst.units 行为一致性（演示性用例）
# ---------------------------------------------------------------------------


class TestCstUnitsCompatibility(unittest.TestCase):
    """验证 mzcst_2024.units 的行为与 test_cst_unit.py 中的演示一致。"""

    def test_demo_l4(self):
        # l4 = l1 + l2 => "2.003 mm"
        l1 = 2 * mm
        l2 = 3 * um
        l4 = l1 + l2
        assert str(l4) == "2.003 mm"

    def test_demo_l5(self):
        # l5 = l2 + l1 => "2003 µm"，mzcst 使用 "um" 符号
        l1 = 2 * mm
        l2 = 3 * um
        l5 = l2 + l1
        assert l5.unit == um
        assert math.isclose(l5.value, 2003.0, rel_tol=1e-9)

    def test_demo_u1(self):
        # u1 = p1 / i1 => "4 V"
        p1 = 20 * W
        i1 = 5 * A
        u1 = p1 / i1
        assert u1.unit.dims == V.dims
        assert math.isclose(u1.value, 4.0, rel_tol=1e-9)

    def test_demo_l6(self):
        # l6 = l3.convert_to(um) => "127 µm"
        l3 = 5 * mil
        l6 = l3.convert_to(um)
        assert l6.unit == um
        assert math.isclose(l6.value, 127.0, rel_tol=1e-9)


if __name__ == "__main__":
    unittest.main()
