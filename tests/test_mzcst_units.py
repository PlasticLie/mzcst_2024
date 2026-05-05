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
from decimal import Decimal

import mzcst_2024.units as mzu
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
    """测试基本物理量的创建与字符串表示。"""

    def test_length_mm(self):
        """创建毫米量并验证数值与单位。"""
        l1 = 2 * mm
        assert l1.value == 2
        assert l1.unit == mm

    def test_length_um(self):
        """创建微米量并验证数值与单位。"""
        l2 = 3 * um
        assert l2.value == 3
        assert l2.unit == um

    def test_length_mil(self):
        """创建 mil 量并验证数值与单位。"""
        l3 = 5 * mil
        assert l3.value == 5
        assert l3.unit == mil

    def test_power_W(self):
        """创建瓦特量并验证数值与单位。"""
        p1 = 20 * W
        assert p1.value == 20
        assert p1.unit == W

    def test_current_A(self):
        """创建安培量并验证数值与单位。"""
        i1 = 5 * A
        assert i1.value == 5
        assert i1.unit == A

    def test_str_representation(self):
        """检查多个基础物理量的字符串表示。"""
        assert f"{2 * mm:.0f}" == "2 mm"
        assert f"{3 * um:.0f}" == "3 μm"
        assert f"{5 * mil:.0f}" == "5 mil"
        assert f"{20 * W:.0f}" == "20 W"
        assert f"{5 * A:.0f}" == "5 A"

    def test_unit_creation_from_string(self):
        """通过字符串创建单位并验证。"""
        alength = Quantity.from_string("42 mm")
        assert f"{alength:.0f}" == "42 mm"


# ---------------------------------------------------------------------------
# 加减法与单位传播
# ---------------------------------------------------------------------------


class TestArithmetic(unittest.TestCase):
    """测试算术运算与结果单位传播。"""

    def test_add_mm_um_result_in_mm(self):
        """mm 与 um 相加，结果应保留为 mm。"""
        l4 = (2 * mm) + (3 * um)
        assert l4.unit == mm
        assert math.isclose(l4.value, 2.003, rel_tol=1e-9)

    def test_add_um_mm_result_in_um(self):
        """um 与 mm 相加，结果应保留为 um。"""
        l5 = (3 * um) + (2 * mm)
        assert l5.unit == um
        assert math.isclose(l5.value, 2003.0, rel_tol=1e-9)

    def test_sub_same_unit(self):
        """同单位物理量相减。"""
        result = (5 * mm) - (2 * mm)
        assert result.unit == mm
        assert math.isclose(result.value, 3.0, rel_tol=1e-9)

    def test_sub_cross_unit(self):
        """兼容但不同单位的物理量相减。"""
        result = (5 * mm) - (1000 * um)
        assert result.unit == mm
        assert math.isclose(result.value, 4.0, rel_tol=1e-9)

    def test_div_W_by_A_gives_V(self):
        """功率除以电流并验证电压量纲。"""
        u1 = (20 * W) / (5 * A)
        assert u1.unit == V
        assert math.isclose(u1.value, 4.0, rel_tol=1e-9)

    def test_mul_scalar(self):
        """物理量与标量相乘。"""
        result = (3 * mm) * 2
        assert result.value == 6
        assert result.unit == mm

    def test_div_scalar(self):
        """物理量除以标量。"""
        result = (6 * mm) / 2
        assert result.value == 3
        assert result.unit == mm

    def test_mul_quantities(self):
        """两个物理量相乘并验证派生量纲。"""
        force = 10 * N
        distance = 2 * m
        work = force * distance
        assert work.unit == J
        assert math.isclose(work.value, 20.0, rel_tol=1e-9)

    def test_div_quantities(self):
        """两个物理量相除并验证派生量纲。"""
        power = 100 * W
        current = 5 * A
        voltage = power / current
        assert voltage.unit == V
        assert math.isclose(voltage.value, 20.0, rel_tol=1e-9)


# ---------------------------------------------------------------------------
# 单位转换
# ---------------------------------------------------------------------------


class TestConversion(unittest.TestCase):
    """测试兼容单位之间的数值转换。"""

    def test_mil_to_um(self):
        """将 mil 转为 um 并验证数值。"""
        l3 = 5 * mil
        l6 = l3.convert_to(um)
        assert l6.unit == um
        assert math.isclose(l6.value, 127.0, rel_tol=1e-9)

    def test_mm_to_um(self):
        """将 mm 转为 um。"""
        result = (1 * mm).convert_to(um)
        assert math.isclose(result.value, 1000.0, rel_tol=1e-9)

    def test_km_to_m(self):
        """将 km 转为 m。"""
        result = (1 * km).convert_to(m)
        assert math.isclose(result.value, 1000.0, rel_tol=1e-9)

    def test_cm_to_mm(self):
        """将 cm 转为 mm。"""
        result = (1 * cm).convert_to(mm)
        assert math.isclose(result.value, 10.0, rel_tol=1e-9)

    def test_hour_to_s(self):
        """将 hour 转为 s。"""
        result = (1 * hour).convert_to(s)
        assert math.isclose(result.value, 3600.0, rel_tol=1e-9)

    def test_day_to_hour(self):
        """将 day 转为 hour。"""
        result = (1 * day).convert_to(hour)
        assert math.isclose(result.value, 24.0, rel_tol=1e-9)

    def test_kA_to_A(self):
        """将 kA 转为 A。"""
        result = (2 * kA).convert_to(A)
        assert math.isclose(result.value, 2000.0, rel_tol=1e-9)

    def test_mA_to_A(self):
        """将 mA 转为 A。"""
        result = (500 * mA).convert_to(A)
        assert math.isclose(result.value, 0.5, rel_tol=1e-9)

    def test_incompatible_conversion_raises(self):
        """不兼容量纲转换时应抛出 ValueError。"""
        with self.assertRaises(ValueError):
            (1 * mm).convert_to(s)

    def test_incompatible_conversion_message(self):
        """不兼容转换时应提供可读错误信息。"""
        with self.assertRaisesRegex(ValueError, "Cannot convert"):
            (1 * W).convert_to(m)

    def test_convert_value_function(self):
        """使用 convert_value 辅助函数进行转换。"""
        result = convert_value(5.0, mil, um)
        assert math.isclose(result, 127.0, rel_tol=1e-9)

    def test_degree_to_rad(self):
        """将 degree 转为 rad。"""
        result = (180 * degree).convert_to(rad)
        assert math.isclose(result.value, math.pi, rel_tol=1e-9)

    def test_inch_to_mm(self):
        """将 inch 转为 mm。"""
        result = (1 * inch).convert_to(mm)
        assert math.isclose(result.value, 25.4, rel_tol=1e-9)

    def test_liter_to_cm3(self):
        """将 L 转为 cm3。"""
        result = (1 * L).convert_to(cm3)
        assert math.isclose(result.value, 1000.0, rel_tol=1e-9)

    def test_hpa_to_pa(self):
        """将 hPa 转为 Pa。"""
        result = (1 * hPa).convert_to(Pa)
        assert math.isclose(result.value, 100.0, rel_tol=1e-9)

    def test_ev_to_joule(self):
        """将 eV 转为 J。"""
        result = (1 * eV).convert_to(J)
        assert math.isclose(result.value, 1.602176634e-19, rel_tol=1e-9)

    def test_kv_to_v(self):
        """将 kV 转为 V。"""
        result = (2 * kV).convert_to(V)
        assert math.isclose(result.value, 2000.0, rel_tol=1e-9)

    def test_byte_to_bit(self):
        """将 byte 转为 bit。"""
        result = (1 * byte).convert_to(bit)
        assert math.isclose(result.value, 8.0, rel_tol=1e-9)

    def test_kibi_to_byte(self):
        """按模块约定将 kibi 转为 byte。"""
        result = (1 * kibi).convert_to(byte)
        assert math.isclose(result.value, 128.0, rel_tol=1e-9)


# ---------------------------------------------------------------------------
# .value 属性（已知单位下直接读取数值）
# ---------------------------------------------------------------------------


class TestValueAccess(unittest.TestCase):
    """测试转换前后对 .value 的直接访问。"""

    def test_value_mil(self):
        """直接读取 mil 量的数值。"""
        l3 = 5 * mil
        assert l3.value == 5

    def test_value_um_after_conversion(self):
        """从 mil 转为 um 后读取数值。"""
        l6 = (5 * mil).convert_to(um)
        assert math.isclose(l6.value, 127.0, rel_tol=1e-9)

    def test_value_current(self):
        """直接读取电流量的数值。"""
        assert (5 * A).value == 5

    def test_convert_to_known_unit_then_read(self):
        """两种表示都转为 mm 后应得到相同数值。"""

        l3 = 5 * mil
        l6 = l3.convert_to(um)
        l7 = random.choice([l3, l6])
        # 无论选哪个，转换到 mm 后值应相同
        assert math.isclose(l7.convert_to(mm).value, 0.127, rel_tol=1e-9)


# ---------------------------------------------------------------------------
# Unit 类本身
# ---------------------------------------------------------------------------


class TestUnit(unittest.TestCase):
    """测试 Unit 类接口与单位代数行为。"""

    def test_unit_str(self):
        """返回常见单位的符号字符串。"""
        assert str(mm) == "mm"
        assert str(V) == "V"
        assert str(Hz) == "Hz"

    def test_unit_repr(self):
        """返回包含关键字段的调试表示。"""
        r = repr(mm)
        assert r.startswith("Unit('mm'")
        assert "dimensions=" in r
        assert "factor=" in r

    def test_unit_eq(self):
        """按符号语义比较单位对象。"""
        assert Unit("mm") == Unit("mm")
        assert Unit("mm") != Unit("um")
        assert Unit("um") == Unit("μm")  # 兼容两种微米符号

    def test_unit_get_symbol(self):
        """通过 get_symbol 返回规范单位符号。"""
        assert mm.get_symbol() == "mm"
        assert A.get_symbol() == "A"

    def test_unit_dims(self):
        """暴露简单单位的基础量纲。"""

        assert mm.dims == {"m": Decimal(1)}
        assert A.dims == {"A": Decimal(1)}

    def test_unit_factor(self):
        """暴露相对 SI 的数值缩放因子。"""
        assert math.isclose(mm.factor, 1e-3, rel_tol=1e-9)
        assert math.isclose(um.factor, 1e-6, rel_tol=1e-9)
        assert math.isclose(km.factor, 1e3, rel_tol=1e-9)

    def test_unit_mul(self):
        """单位相乘并验证结果量纲。"""
        area_unit = m * m
        assert area_unit.dims == {"m": Decimal(2)}

    def test_unit_div(self):
        """单位相除并验证结果量纲。"""
        speed_unit = m / s
        assert speed_unit.dims == {"m": Decimal(1), "s": Decimal(-1)}

    def test_unit_pow(self):
        """单位的整数次幂运算。"""
        vol_unit = m**3
        assert vol_unit.dims == {"m": Decimal(3)}

    def test_unit_pow_Decimal(self):
        """单位的分数次幂运算。"""
        sqrt_m = m.pow(1, 2)
        assert sqrt_m.dims == {"m": Decimal(1, 2)}

    def test_unit_pow_zero_denom_raises(self):
        """分数幂分母为 0 时应拒绝并抛错。"""
        with self.assertRaises(ZeroDivisionError):
            m.pow(1, 0)

    def test_unit_inSI(self):
        """将单位表达式转换为 SI 归一化因子形式。"""
        si = mm.inSI()
        assert math.isclose(si.factor, 1.0, rel_tol=1e-9)
        assert si.dims == mm.dims

    def test_unit_simplify(self):
        """在不改变物理意义的前提下简化单位。"""
        simplified = mm.simplify()
        assert simplified.dims == mm.dims
        assert math.isclose(simplified.factor, mm.factor, rel_tol=1e-9)

    def test_unit_decode_encode(self):
        """从符号解码并再编码回符号。"""
        u = Unit.decode("mm")
        assert u == mm
        assert u.encode() == "mm"

    def test_unknown_unit_raises(self):
        """未知单位符号应抛出 ValueError。"""
        with self.assertRaisesRegex(ValueError, "Unknown unit symbol"):
            Unit("foobar")

    def test_unit_dimensionless_one(self):
        """无量纲单位应表示为空量纲。"""
        assert not one.dims

    def test_unit_decode_bar_symbol(self):
        """解码 bar 并验证其与 Pa 量纲一致。"""
        pressure = Unit.decode("bar")
        assert pressure.dims == Pa.dims
        assert math.isclose(pressure.factor, 1e5, rel_tol=1e-9)


# ---------------------------------------------------------------------------
# ComplexQuantity
# ---------------------------------------------------------------------------


class TestComplexQuantity(unittest.TestCase):
    """测试 ComplexQuantity 的特有行为。"""

    def test_complex_value_keeps_unit(self):
        """复数数值及其单位应保持不变。"""
        z = ComplexQuantity(3 + 4j, Ohm)
        assert z.value == 3 + 4j
        assert z.unit == Ohm

    def test_complex_quantity_repr(self):
        """复数量的 repr 应沿用 Quantity 风格。"""
        z = ComplexQuantity(1 - 2j, V)
        assert "ComplexQuantity" not in repr(z)
        assert "Quantity(" in repr(z)


# ---------------------------------------------------------------------------
# 单位量纲测试
# ---------------------------------------------------------------------------


class TestUnitDimensions(unittest.TestCase):
    """测试派生单位运算后的量纲正确性。"""

    def test_pressure_dims_from_force_over_area(self):
        """由力除以面积推导压力量纲。"""
        pressure_unit = N / (m**2)
        assert pressure_unit.dims == Pa.dims

    def test_voltage_dims_from_power_over_current(self):
        """由功率除以电流推导电压量纲。"""
        voltage_unit = W / A
        assert voltage_unit.dims == V.dims

    def test_magnetic_flux_density_dims(self):
        """由磁通除以面积推导磁通密度量纲。"""
        magnetic_flux_density = Wb / (m**2)
        assert magnetic_flux_density.dims == T.dims

    def test_frequency_dims(self):
        """频率应具有时间负一次量纲。"""
        assert Hz.dims == {"s": Decimal(-1)}

    def test_dimensionless_after_cancellation(self):
        """相同量纲约消后应得到无量纲单位。"""
        dimless = m / m
        assert dimless.dims == {}

    def test_compound_unit_scaling_factor(self):
        """转换复合速度单位并验证缩放因子。"""
        speed_unit = km / hour
        si_speed = m / s
        result = convert_value(1.0, speed_unit, si_speed)
        assert math.isclose(result, 1000.0 / 3600.0, rel_tol=1e-9)

    def test_compound_unit_conversion(self):
        """将复合速度单位转换为 SI 并验证数值。"""
        speed = 120 * km / hour
        si_speed = speed.convert_to(m / s)
        assert math.isclose(si_speed.value, 120 * 1000.0 / 3600.0, rel_tol=1e-9)


# ---------------------------------------------------------------------------
# scaling_factor_to_SI
# ---------------------------------------------------------------------------


class TestScalingFactor(unittest.TestCase):
    """测试 scaling_factor_to_SI 在代表性单位上的结果。"""

    def test_mm_to_SI(self):
        """返回 mm 对应的 SI 缩放因子。"""
        assert math.isclose(scaling_factor_to_SI(mm), 1e-3, rel_tol=1e-9)

    def test_km_to_SI(self):
        """返回 km 对应的 SI 缩放因子。"""
        assert math.isclose(scaling_factor_to_SI(km), 1e3, rel_tol=1e-9)

    def test_m_to_SI(self):
        """返回 m 对应的 SI 缩放因子。"""
        assert math.isclose(scaling_factor_to_SI(m), 1.0, rel_tol=1e-9)

    def test_hour_to_SI(self):
        """返回 hour 对应的 SI 缩放因子。"""
        assert math.isclose(scaling_factor_to_SI(hour), 3600.0, rel_tol=1e-9)

    def test_mil_to_SI(self):
        """返回 mil 对应的 SI 缩放因子。"""
        assert math.isclose(scaling_factor_to_SI(mil), 2.54e-5, rel_tol=1e-9)


# ---------------------------------------------------------------------------
# 与 cst.units 行为一致性（演示性用例）
# ---------------------------------------------------------------------------


class TestCstUnitsCompatibility(unittest.TestCase):
    """验证 mzcst_2024.units 的行为与 test_cst_unit.py 中的演示一致。"""

    def test_demo_l4(self):
        """复现演示：mm 与 um 相加应得到 2.003 mm。"""
        # l4 = l1 + l2 => "2.003 mm"
        l1 = 2 * mm
        l2 = 3 * um
        l4 = l1 + l2
        assert str(l4) == "2.003 mm"

    def test_demo_l5(self):
        """复现演示：反向相加时输出单位保持为 um。"""
        l1 = 2 * mm
        l2 = 3 * um
        l5 = l2 + l1
        assert l5.unit == um
        assert math.isclose(l5.value, 2003.0, rel_tol=1e-9)

    def test_demo_u1(self):
        """复现演示：功率除以电流得到电压。"""
        # u1 = p1 / i1 => "4 V"
        p1 = 20 * W
        i1 = 5 * A
        u1 = p1 / i1
        assert u1.unit.dims == V.dims
        assert math.isclose(u1.value, 4.0, rel_tol=1e-9)

    def test_demo_l6(self):
        """复现演示：将 mil 物理量转换为 um。"""
        # l6 = l3.convert_to(um) => "127 um"
        l3 = 5 * mil
        l6 = l3.convert_to(um)
        assert l6.unit == um
        assert math.isclose(l6.value, 127.0, rel_tol=1e-9)

    def test_cst_units_compatibility(self):
        """复现CST 2026中 cst.units 模块的演示用例，验证与 mzcst_2024.units 的兼容性。"""
        # Create quantities with units
        l1: Quantity = 2 * mm
        l2: Quantity = 3 * um
        l3: Quantity = 5 * mil
        p1: Quantity = 20 * W
        i1: Quantity = 5 * A
        assert f"{l1:.0f}" == "2 mm"
        assert f"{l2:.0f}" == "3 μm"
        assert f"{l3:.0f}" == "5 mil"
        assert f"{p1:.0f}" == "20 W"
        assert f"{i1:.0f}" == "5 A"

        # Create quantities with string based unit, only string variants from the Predefined units table can be used.
        alength = 42 * Unit("mm")
        km = Unit("km")
        hour = Unit("hour")
        speed_unit = km / hour
        aspeed = (
            120 * km / hour
        )  # Note that you cannot use "km/h" as it is not one of the predefined units
        apower = 55 * Unit("GW")
        assert f"{alength:.0f}" == "42 mm"
        assert f"{aspeed:.0f}" == "120 km/hour"
        assert f"{apower:.0f}" == "55 GW"

        # Compute derived quantities with automatic unit conversions
        l4 = l1 + l2  # add "mm" and "um" resulting in "mm"
        l5 = l2 + l1  # add "μm" and "mm" resulting in "μm"
        assert f"{l4:.3f}" == "2.003 mm"
        assert f"{l5:.0f}" == "2003 μm"
        u1 = p1 / i1  # divide "W" by "A" resulting in "V"
        assert f"{u1:.0f}" == "4 V"

        # Enforce representation using a specific unit
        l6 = l3.convert_to(um)
        assert f"{l6:.0f}" == "127 μm"

        # Convert to float without unit
        # Warning: Only do this, if the exact unit of the quantity is known.
        #          Use "convert_to" to enforce a specific unit.
        assert math.isclose(l3.value, 5.0, rel_tol=1e-9)
        assert math.isclose(l6.value, 127.0, rel_tol=1e-9)
        assert math.isclose(i1.value, 5.0, rel_tol=1e-9)

        l7 = random.choice([l3, l6])  # result may use either "mil" or "um"
        print(l7.value)  # prints value with unknown/random unit
        print(l7.convert_to(mm).value)  # prints value with known unit
        pass


if __name__ == "__main__":
    # TestCstUnitsCompatibility().test_cst_units_compatibility()
    unittest.main(verbosity=2)
