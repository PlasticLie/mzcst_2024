"""Module for Mathematical Functions and Constants."""


import logging

from .common import NEW_LINE, OPERATION_FAILED, OPERATION_SUCCESS, quoted
from .global_ import Parameter

_logger = logging.getLogger(__name__)


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


def acos(x: Parameter) -> Parameter:
    """弧度制反余弦函数

    Args:
        x (Parameter): 表达式。

    Returns:
        Parameter: ACos(x)。
    """
    temp: str = "ACos(" + x.name + ")"
    return Parameter(temp)


def acosD(x: Parameter) -> Parameter:
    """角度制反余弦函数

    Args:
        x (Parameter): 表达式。

    Returns:
        Parameter: ACosD(x)。
    """
    temp: str = "ACosD(" + x.name + ")"
    return Parameter(temp)


def asin(x: Parameter) -> Parameter:
    """弧度制反正弦函数

    Args:
        x (Parameter): 表达式。

    Returns:
        Parameter: ASin(x)。
    """
    temp: str = "ASin(" + x.name + ")"
    return Parameter(temp)


def asinD(x: Parameter) -> Parameter:
    """角度制反正弦函数

    Args:
        x (Parameter): 表达式。

    Returns:
        Parameter: ASinD(x)。
    """
    temp: str = "ASinD(" + x.name + ")"
    return Parameter(temp)


def atanD(x: Parameter) -> Parameter:
    """角度制反正切函数

    注：CST没有弧度制反正切函数。

    Args:
        x (Parameter): 表达式。

    Returns:
        Parameter: ATnD(x)。
    """
    temp: str = "ATnD(" + x.name + ")"
    return Parameter(temp)


def atan2(y: Parameter, x: Parameter) -> Parameter:
    """弧度制二元反正切函数，即arctan(y / x)



    Args:
        y (Parameter): 分子。
        x (Parameter): 分母。

    Returns:
        Parameter: ATn2(y, x)。
    """
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
    temp: str = f"ATn2D({y.name}, {x.name})"
    return Parameter(temp)


def sin(x: Parameter) -> Parameter:
    """弧度制正弦函数

    Args:
        x (Parameter): 表达式。

    Returns:
        Parameter: Sin(x)。
    """
    temp: str = "Sin(" + x.name + ")"
    return Parameter(temp)


def sinD(x: Parameter) -> Parameter:
    """角度制正弦函数

    Args:
        x (parameter): 表达式。

    Returns:
        parameter: SinD(x)。
    """
    temp: str = "SinD(" + x.name + ")"
    return Parameter(temp)


def cos(x: Parameter) -> Parameter:
    """弧度制余弦函数

    Args:
        x (Parameter): 表达式。

    Returns:
        Parameter: Cos(x)。
    """
    temp: str = "Cos(" + x.name + ")"
    return Parameter(temp)


def cosD(x: Parameter) -> Parameter:
    """角度制余弦函数

    Args:
        x (parameter): 表达式。

    Returns:
        parameter: CosD(x)。
    """
    temp: str = "CosD(" + x.name + ")"
    return Parameter(temp)


def tan(x: Parameter) -> Parameter:
    """弧度制正切函数

    Args:
        x (Parameter): 表达式。

    Returns:
        Parameter: Tan(x)。
    """
    temp: str = "Tan(" + x.name + ")"
    return Parameter(temp)


def tanD(x: Parameter) -> Parameter:
    """角度制正切函数

    Args:
        x (parameter): 表达式。

    Returns:
        parameter: TanD(x)。
    """
    temp: str = "TanD(" + x.name + ")"
    return Parameter(temp)


def asinh(x: Parameter) -> Parameter:
    """反双曲正弦函数

    Args:
        x (parameter): 表达式。

    Returns:
        parameter: ASinh(x)。
    """
    temp: str = "ASinh(" + x.name + ")"
    return Parameter(temp)


def acosh(x: Parameter) -> Parameter:
    """反双曲余弦函数

    Args:
        x (parameter): 表达式。

    Returns:
        parameter: ACosh(x)。
    """
    temp: str = "ACosh(" + x.name + ")"
    return Parameter(temp)


def sinh(x: Parameter) -> Parameter:
    """双曲正弦函数

    Args:
        x (parameter): 表达式。

    Returns:
        parameter: Sinh(x)。
    """
    temp: str = "Sinh(" + x.name + ")"
    return Parameter(temp)


def cosh(x: Parameter) -> Parameter:
    """双曲余弦函数

    Args:
        x (parameter): 表达式。

    Returns:
        parameter: Cosh(x)。
    """
    temp: str = "Cosh(" + x.name + ")"
    return Parameter(temp)


def sqrt(x: Parameter) -> Parameter:
    """平方根

    Args:
        x (parameter): 表达式。

    Returns:
        parameter: Sqr(x)。
    """
    temp: str = "Sqr(" + x.name + ")"
    return Parameter(temp)


def bracket(x: Parameter | str) -> Parameter:
    """给表达式加括号

    Args:
        x (parameter): 表达式。

    Returns:
        parameter: 加括号后的表达式。
    """
    temp: str = ""
    if isinstance(x, Parameter):
        temp = "(" + x.name + ")"
    elif isinstance(x, str):
        temp = "(" + x + ")"
    return Parameter(temp)


# endregion
# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
