"""Module for Mathematical Functions and Constants."""

import logging

from .common import NEW_LINE, OPERATION_FAILED, OPERATION_SUCCESS, quoted
from .global_ import Parameter

_logger = logging.getLogger(__name__)

ParameterLike = Parameter | int | float | str

#######################################
# region Constants
# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

pi = Parameter("Pi")
eps_0 = Parameter("Eps0")
mu_0 = Parameter("Mu0")
c_0 = Parameter("CLight")
e_0 = Parameter("ChargeElementary")
m_electron = Parameter("MassElectron")
m_proton = Parameter("MassProton")
k_boltzmann = Parameter("ConstantBoltzmann")
true = Parameter("True")
false = Parameter("False")

# endregion
# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑


#######################################
# region 反三角函数
# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓


def acos(x: ParameterLike) -> Parameter:
    """弧度制反余弦函数

    Args:
        x (ParameterLike): 表达式。
    Returns:
        Parameter: ACos(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = f"ACos({x.name})"
    return Parameter(temp)


def acosD(x: ParameterLike) -> Parameter:
    """角度制反余弦函数

    Args:
        x (ParameterLike): 表达式。
    Returns:
        Parameter: ACosD(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = f"ACosD({x.name})"
    return Parameter(temp)


def asin(x: ParameterLike) -> Parameter:
    """弧度制反正弦函数

    Args:
        x (ParameterLike): 表达式。
    Returns:
        Parameter: ASin(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = f"ASin({x.name})"
    return Parameter(temp)


def asinD(x: Parameter) -> Parameter:
    """角度制反正弦函数

    Args:
        x (Parameter): 表达式。

    Returns:
        Parameter: ASinD(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = f"ASinD({x.name})"
    return Parameter(temp)


def atanD(x: ParameterLike) -> Parameter:
    """角度制反正切函数

    注：CST没有弧度制反正切函数。

    Args:
        x (ParameterLike): 表达式。

    Returns:
        Parameter: ATnD(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = f"ATnD({x.name})"
    return Parameter(temp)


def atan2(y: ParameterLike, x: ParameterLike) -> Parameter:
    """弧度制二元反正切函数，即arctan(y / x)

    Args:
        y (ParameterLike): 分子。
        x (ParameterLike): 分母。
    Returns:
        Parameter: ATn2(y, x)。
    """
    y = Parameter(y) if not isinstance(y, Parameter) else y
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = f"ATn2({y.name}, {x.name})"
    return Parameter(temp)


def atan2D(y: Parameter, x: Parameter) -> Parameter:
    """角度制二元反正切函数，即arctanD(y / x)

    Args:
        y (Parameter): 分子。
        x (Parameter): 分母。

    Returns:
        Parameter: ATn2D(y, x)。
    """
    y = Parameter(y) if not isinstance(y, Parameter) else y
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = f"ATn2D({y.name}, {x.name})"
    return Parameter(temp)


# endregion
# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

#######################################
# region 三角函数
# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓


def sin(x: ParameterLike) -> Parameter:
    """弧度制正弦函数

    Args:
        x (ParameterLike): 表达式。
    Returns:
        Parameter: Sin(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = f"Sin({x.name})"
    return Parameter(temp)


def sinD(x: ParameterLike) -> Parameter:
    """角度制正弦函数

    Args:
        x (ParameterLike): 表达式。
    Returns:
        parameter: SinD(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = f"SinD({x.name})"
    return Parameter(temp)


def cos(x: ParameterLike) -> Parameter:
    """弧度制余弦函数

    Args:
        x (ParameterLike): 表达式。
    Returns:
        Parameter: Cos(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = f"Cos({x.name})"
    return Parameter(temp)


def cosD(x: ParameterLike) -> Parameter:
    """角度制余弦函数

    Args:
        x (ParameterLike): 表达式。
    Returns:
        Parameter: CosD(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = f"CosD({x.name})"
    return Parameter(temp)


def tan(x: ParameterLike) -> Parameter:
    """弧度制正切函数

    Args:
        x (ParameterLike): 表达式。
    Returns:
        Parameter: Tan(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = f"Tan({x.name})"
    return Parameter(temp)


def tanD(x: ParameterLike) -> Parameter:
    """角度制正切函数

    Args:
        x (ParameterLike): 表达式。
    Returns:
        parameter: TanD(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = f"TanD({x.name})"
    return Parameter(temp)


# endregion
# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑


#######################################
# region 反双曲函数
# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓


def asinh(x: ParameterLike) -> Parameter:
    """反双曲正弦函数

    Args:
        x (ParameterLike): 表达式。
    Returns:
        parameter: ASinh(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = f"ASinh({x.name})"
    return Parameter(temp)


def acosh(x: ParameterLike) -> Parameter:
    """反双曲余弦函数

    Args:
        x (ParameterLike): 表达式。
    Returns:
        parameter: ACosh(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = f"ACosh({x.name})"
    return Parameter(temp)


# endregion
# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑


#######################################
# region 双曲函数
# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓


def sinh(x: ParameterLike) -> Parameter:
    """双曲正弦函数

    Args:
        x (ParameterLike): 表达式。
    Returns:
        parameter: Sinh(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = f"Sinh({x.name})"
    return Parameter(temp)


def cosh(x: ParameterLike) -> Parameter:
    """双曲余弦函数

    Args:
        x (ParameterLike): 表达式。
    Returns:
        parameter: Cosh(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = f"Cosh({x.name})"
    return Parameter(temp)


# endregion
# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

#######################################
# region 逻辑函数
# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓


def not_(x: ParameterLike) -> Parameter:
    """逻辑非函数

    Args:
        x (ParameterLike): 表达式。
    Returns:
        parameter: NOT(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = f"NOT({x.name})"
    return Parameter(temp)


def eql(x: ParameterLike, y: ParameterLike) -> Parameter:
    """逻辑等于函数

    Args:
        x (ParameterLike): 表达式1。
        y (ParameterLike): 表达式2。
    Returns:
        parameter: EQL(x, y)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    y = Parameter(y) if not isinstance(y, Parameter) else y
    temp: str = f"EQL({x.name}, {y.name})"
    return Parameter(temp)


def eql_float(
    x: ParameterLike, y: ParameterLike, tol: ParameterLike
) -> Parameter:
    """逻辑等于函数（浮点数比较，带容差）

    Args:
        x (ParameterLike): 表达式1。
        y (ParameterLike): 表达式2。
        tol (ParameterLike): 容差。
    Returns:
        parameter: EQL(x, y, tol)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    y = Parameter(y) if not isinstance(y, Parameter) else y
    tol = Parameter(tol) if not isinstance(tol, Parameter) else tol
    temp: str = f"EQL({x.name}, {y.name}, {tol.name})"
    return Parameter(temp)


def neq(x: ParameterLike, y: ParameterLike) -> Parameter:
    """逻辑不等于函数

    Args:
        x (ParameterLike): 表达式1。
        y (ParameterLike): 表达式2。
    Returns:
        parameter: NEQ(x, y)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    y = Parameter(y) if not isinstance(y, Parameter) else y
    temp: str = f"NEQ({x.name}, {y.name})"
    return Parameter(temp)


def lss(x: ParameterLike, y: ParameterLike) -> Parameter:
    """逻辑小于函数

    Args:
        x (ParameterLike): 表达式1。
        y (ParameterLike): 表达式2。
    Returns:
        parameter: LSS(x, y)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    y = Parameter(y) if not isinstance(y, Parameter) else y
    temp: str = f"LSS({x.name}, {y.name})"
    return Parameter(temp)


def gtr(x: ParameterLike, y: ParameterLike) -> Parameter:
    """逻辑大于函数

    Args:
        x (ParameterLike): 表达式1。
        y (ParameterLike): 表达式2。
    Returns:
        parameter: GTR(x, y)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    y = Parameter(y) if not isinstance(y, Parameter) else y
    temp: str = f"GTR({x.name}, {y.name})"
    return Parameter(temp)


def leq(x: ParameterLike, y: ParameterLike) -> Parameter:
    """逻辑小于等于函数

    Args:
        x (ParameterLike): 表达式1。
        y (ParameterLike): 表达式2。
    Returns:
        parameter: LEQ(x, y)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    y = Parameter(y) if not isinstance(y, Parameter) else y
    temp: str = f"LEQ({x.name}, {y.name})"
    return Parameter(temp)


def geq(x: ParameterLike, y: ParameterLike) -> Parameter:
    """逻辑大于等于函数
    Args:
        x (ParameterLike): 表达式1。
        y (ParameterLike): 表达式2。
    Returns:
        parameter: GEQ(x, y)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    y = Parameter(y) if not isinstance(y, Parameter) else y
    temp: str = f"GEQ({x.name}, {y.name})"
    return Parameter(temp)


def llf(
    cond: ParameterLike, val_true: ParameterLike, val_false: ParameterLike
) -> Parameter:
    """逻辑条件函数

    Args:
        cond (ParameterLike): 条件表达式。
        val_true (ParameterLike): 条件为真时的值。
        val_false (ParameterLike): 条件为假时的值。
    Returns:
        parameter: LLF(cond, val_true, val_false)。
    """
    cond = Parameter(cond) if not isinstance(cond, Parameter) else cond
    val_true = (
        Parameter(val_true) if not isinstance(val_true, Parameter) else val_true
    )
    val_false = (
        Parameter(val_false)
        if not isinstance(val_false, Parameter)
        else val_false
    )
    temp: str = f"LLF({cond.name}, {val_true.name}, {val_false.name})"
    return Parameter(temp)


# endregion
# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

#######################################
# region 其他函数
# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓


def fmod(x: ParameterLike, y: ParameterLike) -> Parameter:
    """取模函数

    Args:
        x (ParameterLike): 被除数表达式。
        y (ParameterLike): 除数表达式。
    Returns:
        parameter: FMod(x, y)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    y = Parameter(y) if not isinstance(y, Parameter) else y
    temp: str = f"FMod({x.name}, {y.name})"
    return Parameter(temp)


def re(x: ParameterLike) -> Parameter:
    """实部函数

    Args:
        x (ParameterLike): 表达式。
    Returns:
        parameter: Re(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = f"Re({x.name})"
    return Parameter(temp)


def im(x: ParameterLike, phase: ParameterLike | None = None) -> Parameter:
    """虚部函数。接收一个参数时，返回Im(x)，计算输入表达式的值的虚部；接收两个参数时，返回Im(x, phase)，x为幅值，phase为相位，以x和phase构造的复数计算其虚部。

    Args:
        x (ParameterLike): 表达式。
        phase (ParameterLike | None): 可选参数，表示虚部的相位。
    Returns:
        parameter: Im(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    if phase is not None:
        phase = Parameter(phase) if not isinstance(phase, Parameter) else phase
        temp: str = f"Im({x.name}, {phase.name})"
    else:
        temp: str = f"Im({x.name})"
    return Parameter(temp)


def real(x: ParameterLike) -> Parameter:
    """实部函数

    Args:
        x (ParameterLike): 表达式。
    Returns:
        parameter: Real(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = f"Real({x.name})"
    return Parameter(temp)


def imag(x: ParameterLike) -> Parameter:
    """虚部函数

    Args:
        x (ParameterLike): 表达式。
    Returns:
        parameter: Imag(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = f"Imag({x.name})"
    return Parameter(temp)


def abs_(x: ParameterLike) -> Parameter:
    """绝对值函数

    Args:
        x (ParameterLike): 表达式。
    Returns:
        parameter: Abs(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = f"Abs({x.name})"
    return Parameter(temp)


def mag(x: ParameterLike) -> Parameter:
    """模函数

    Args:
        x (ParameterLike): 表达式。
    Returns:
        parameter: Mag(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = f"Mag({x.name})"
    return Parameter(temp)


def mag_db10(x: ParameterLike) -> Parameter:
    """模的分贝函数（10倍）

    Args:
        x (ParameterLike): 表达式。
    Returns:
        parameter: MagdB10(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = f"MagdB10({x.name})"
    return Parameter(temp)


def mag_db20(x: ParameterLike) -> Parameter:
    """模的分贝函数（20倍）

    Args:
        x (ParameterLike): 表达式。
    Returns:
        parameter: MagdB20(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = f"MagdB20({x.name})"
    return Parameter(temp)


def arc(x: ParameterLike) -> Parameter:
    """幅角函数（弧度制）

    Args:
        x (ParameterLike): 表达式。
    Returns:
        parameter: Arc(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = f"Arc({x.name})"
    return Parameter(temp)


def phase(x: ParameterLike) -> Parameter:
    """幅角函数（弧度制）

    Args:
        x (ParameterLike): 表达式。
    Returns:
        parameter: Ph(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = f"Ph({x.name})"
    return Parameter(temp)


def arcD(x: ParameterLike) -> Parameter:
    """幅角函数（角度制）

    Args:
        x (ParameterLike): 表达式。
    Returns:
        parameter: ArcD(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = f"ArcD({x.name})"
    return Parameter(temp)


def phaseD(x: ParameterLike) -> Parameter:
    """幅角函数（角度制）

    Args:
        x (ParameterLike): 表达式。
    Returns:
        parameter: PhD(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = f"PhD({x.name})"
    return Parameter(temp)


def uarc(x: ParameterLike, threshold: ParameterLike) -> Parameter:
    """非包裹幅角函数（弧度制）

    Args:
        x (ParameterLike): 表达式。
        threshold (ParameterLike): 非包裹阈值。
    Returns:
        parameter: UArc(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = f"UArc({x.name}, {threshold})"
    return Parameter(temp)


def uarcD(x: ParameterLike, threshold: ParameterLike) -> Parameter:
    """非包裹幅角函数（角度制）

    Args:
        x (ParameterLike): 表达式。
        threshold (ParameterLike): 非包裹阈值。
    Returns:
        parameter: UArcD(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = f"UArcD({x.name}, {threshold})"
    return Parameter(temp)


def uphD(x: ParameterLike, threshold: ParameterLike) -> Parameter:
    """非包裹幅角函数（角度制）

    Args:
        x (ParameterLike): 表达式。
        threshold (ParameterLike): 非包裹阈值。
    Returns:
        parameter: UPhD(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = f"UPhD({x.name}, {threshold})"
    return Parameter(temp)


def exp(x: ParameterLike) -> Parameter:
    """指数函数

    Args:
        x (ParameterLike): 表达式。
    Returns:
        parameter: Exp(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = f"Exp({x.name})"
    return Parameter(temp)


def log(x: ParameterLike) -> Parameter:
    """自然对数函数

    Args:
        x (ParameterLike): 表达式。
    Returns:
        parameter: Log(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = f"Log({x.name})"
    return Parameter(temp)


def ln(x: ParameterLike) -> Parameter:
    """自然对数函数

    Args:
        x (ParameterLike): 表达式。
    Returns:
        parameter: Ln(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = f"Ln({x.name})"
    return Parameter(temp)


def log10(x: ParameterLike) -> Parameter:
    """以10为底的对数函数

    Args:
        x (ParameterLike): 表达式。
    Returns:
        parameter: Log10(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = f"(Log({x.name}) / Log(10))"
    return Parameter(temp)


def sqrt(x: ParameterLike) -> Parameter:
    """平方根

    Args:
        x (ParameterLike): 表达式。
    Returns:
        parameter: Sqr(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = "Sqr(" + x.name + ")"
    return Parameter(temp)


def min_(x: ParameterLike) -> Parameter:
    """取最小值函数

    Args:
        x (ParameterLike): 表达式。
    Returns:
        parameter: Min(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = f"Min({x.name})"
    return Parameter(temp)


def max_(x: ParameterLike) -> Parameter:
    """取最大值函数

    Args:
        x (ParameterLike): 表达式。
    Returns:
        parameter: Max(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = f"Max({x.name})"
    return Parameter(temp)


def mean(x: ParameterLike) -> Parameter:
    """取平均值函数

    Args:
        x (ParameterLike): 表达式。
    Returns:
        parameter: Mean(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = f"Mean({x.name})"
    return Parameter(temp)


def minmag(x: ParameterLike) -> Parameter:
    """取模最小值函数

    Args:
        x (ParameterLike): 表达式。
    Returns:
        parameter: MinMag(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = f"MinMag({x.name})"
    return Parameter(temp)


def maxmag(x: ParameterLike) -> Parameter:
    """取模最大值函数

    Args:
        x (ParameterLike): 表达式。
    Returns:
        parameter: MaxMag(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = f"MaxMag({x.name})"
    return Parameter(temp)


def meanmag(x: ParameterLike) -> Parameter:
    """取模平均值函数

    Args:
        x (ParameterLike): 表达式。
    Returns:
        parameter: MeanMag(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = f"MeanMag({x.name})"
    return Parameter(temp)


def abscissa(x: ParameterLike) -> Parameter:
    """取横坐标函数

    Return the x values of A. This can be used, for example, to include frequency as a parameter in the mathematical expression.

    Args:
        x (ParameterLike): 表达式。
    Returns:
        parameter: Abscissa(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = f"Abscissa({x.name})"
    return Parameter(temp)


def x_axis(x: ParameterLike) -> Parameter:
    """取横坐标函数

    Return the x values of A. This can be used, for example, to include frequency as a parameter in the mathematical expression.

    Args:
        x (ParameterLike): 表达式。
    Returns:
        parameter: X_Axis(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = f"XAxis({x.name})"
    return Parameter(temp)


def sign(x: ParameterLike) -> Parameter:
    """符号函数

    Args:
        x (ParameterLike): 表达式。
    Returns:
        parameter: Sgn(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = f"Sgn({x.name})"
    return Parameter(temp)


def unit_step(x: ParameterLike) -> Parameter:
    """单位阶跃函数

    Return the Heaviside step function of A (0 if A < 0, ½ if A = 0, and 1 if A > 0)

    Args:
        x (ParameterLike): 表达式。
    Returns:
        parameter: UnitStep(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = f"UnitStep({x.name})"
    return Parameter(temp)


def derivative(x: ParameterLike, order: ParameterLike) -> Parameter:
    """导数函数

    Return the derivative of A with respect to the x-axis variable.

    Args:
        x (ParameterLike): 表达式。
        order (ParameterLike): 导数阶数。
    Returns:
        parameter: Derivative(x, order)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    order = Parameter(order) if not isinstance(order, Parameter) else order
    temp: str = f"Derivative({x.name}, {order.name})"
    return Parameter(temp)


def integral(x: ParameterLike) -> Parameter:
    """积分函数

    Return the integral of A, calculated along all available x values. The result is a single number.

    Args:
        x (ParameterLike): 表达式。
    Returns:
        parameter: Integ(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = f"Integ({x.name})"
    return Parameter(temp)


def cumulative_integral(x: ParameterLike) -> Parameter:
    """累积积分函数

    Return the cumulative integral of A: For each x value x’, return the integral from the lowest x value x0 to x’. x’ assumes all values between x0 and the highest x value x1.

    Args:
        x (ParameterLike): 表达式。
    Returns:
        parameter: CumInteg(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = f"CumInteg({x.name})"
    return Parameter(temp)


# endregion
# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑


def bracket(x: ParameterLike) -> Parameter:
    """给表达式加括号。
    使用已有的数学函数和运算符时会自动加括号，此函数用于给没有括号的表达式加括号。

    Args:
        x (ParameterLike): 表达式。
    Returns:
        parameter: 加括号后的表达式。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = ""
    if isinstance(x, Parameter):
        temp = f"({x.name})"
    else:
        temp = f"({x})"
    return Parameter(temp)
