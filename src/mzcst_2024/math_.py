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
# region Mathematical Functions
# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓


def acos(x: ParameterLike) -> Parameter:
    """弧度制反余弦函数

    Args:
        x (ParameterLike): 表达式。
    Returns:
        Parameter: ACos(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = "ACos(" + x.name + ")"
    return Parameter(temp)


def acosD(x: ParameterLike) -> Parameter:
    """角度制反余弦函数

    Args:
        x (ParameterLike): 表达式。
    Returns:
        Parameter: ACosD(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = "ACosD(" + x.name + ")"
    return Parameter(temp)


def asin(x: ParameterLike) -> Parameter:
    """弧度制反正弦函数

    Args:
        x (ParameterLike): 表达式。
    Returns:
        Parameter: ASin(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = "ASin(" + x.name + ")"
    return Parameter(temp)


def asinD(x: Parameter) -> Parameter:
    """角度制反正弦函数

    Args:
        x (Parameter): 表达式。

    Returns:
        Parameter: ASinD(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = "ASinD(" + x.name + ")"
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
    temp: str = "ATnD(" + x.name + ")"
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


def sin(x: ParameterLike) -> Parameter:
    """弧度制正弦函数

    Args:
        x (ParameterLike): 表达式。
    Returns:
        Parameter: Sin(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = "Sin(" + x.name + ")"
    return Parameter(temp)


def sinD(x: ParameterLike) -> Parameter:
    """角度制正弦函数

    Args:
        x (ParameterLike): 表达式。
    Returns:
        parameter: SinD(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = "SinD(" + x.name + ")"
    return Parameter(temp)


def cos(x: ParameterLike) -> Parameter:
    """弧度制余弦函数

    Args:
        x (ParameterLike): 表达式。
    Returns:
        Parameter: Cos(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = "Cos(" + x.name + ")"
    return Parameter(temp)


def cosD(x: ParameterLike) -> Parameter:
    """角度制余弦函数

    Args:
        x (ParameterLike): 表达式。
    Returns:
        Parameter: CosD(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = "CosD(" + x.name + ")"
    return Parameter(temp)


def tan(x: ParameterLike) -> Parameter:
    """弧度制正切函数

    Args:
        x (ParameterLike): 表达式。
    Returns:
        Parameter: Tan(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = "Tan(" + x.name + ")"
    return Parameter(temp)


def tanD(x: ParameterLike) -> Parameter:
    """角度制正切函数

    Args:
        x (ParameterLike): 表达式。
    Returns:
        parameter: TanD(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = "TanD(" + x.name + ")"
    return Parameter(temp)


def asinh(x: ParameterLike) -> Parameter:
    """反双曲正弦函数

    Args:
        x (ParameterLike): 表达式。
    Returns:
        parameter: ASinh(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = "ASinh(" + x.name + ")"
    return Parameter(temp)


def acosh(x: ParameterLike) -> Parameter:
    """反双曲余弦函数

    Args:
        x (ParameterLike): 表达式。
    Returns:
        parameter: ACosh(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = "ACosh(" + x.name + ")"
    return Parameter(temp)


def sinh(x: ParameterLike) -> Parameter:
    """双曲正弦函数

    Args:
        x (ParameterLike): 表达式。
    Returns:
        parameter: Sinh(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = "Sinh(" + x.name + ")"
    return Parameter(temp)


def cosh(x: ParameterLike) -> Parameter:
    """双曲余弦函数

    Args:
        x (ParameterLike): 表达式。
    Returns:
        parameter: Cosh(x)。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = "Cosh(" + x.name + ")"
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


def bracket(x: ParameterLike) -> Parameter:
    """给表达式加括号

    Args:
        x (ParameterLike): 表达式。
    Returns:
        parameter: 加括号后的表达式。
    """
    x = Parameter(x) if not isinstance(x, Parameter) else x
    temp: str = ""
    if isinstance(x, Parameter):
        temp = "(" + x.name + ")"
    elif isinstance(x, str):
        temp = "(" + x + ")"
    return Parameter(temp)


# endregion
# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
