"""用于整个项目的通用对象。"""

import abc
import ast
import logging
import typing

from . import interface
from .common import NEW_LINE, OPERATION_FAILED, OPERATION_SUCCESS, quoted

_logger = logging.getLogger(__name__)
__all__ = [
    "BaseObject",
    "VbaObject",
    "Parameter",
    "Units",
    "change_solver_type",
]


class BaseObject(abc.ABC):
    """围绕With语句块，构建CST脚本中所有的广义对象的抽象基类。

    只支持从VBA代码创建对象。

    Attributes:
        attributes (dict[str, str]): 包含对象属性的字典。
        vba (list[str]): 构造对象的With语句块代码。
    """

    def __init__(
        self,
        *,
        attributes: typing.Optional[dict[str, str]] = None,
        **kwargs,
    ):
        super().__init__()
        if attributes is None:
            attributes = {}
        else:
            self._attributes: dict[str, str] = attributes
        self._history_title: str = "create object: "
        self._kwargs = kwargs
        return

    @property
    def history_title(self) -> str:
        return self._history_title

    @property
    def attributes(self) -> dict[str, str]:
        return self._attributes

    def retitle(self, t: str):
        self._history_title = t
        return self

    # @abc.abstractmethod
    def create_from_attributes(
        self, modeler: "interface.Model3D"
    ) -> "BaseObject":
        """从属性列表新建对象。下面的实现给出了一个通用的范式。

        由于本基类不能直接用于创建实例，所以直接调用本方法不会得到你想要的对象，CST会直
        接报错停止运行。

        请务必在子类中重载该方法。

        Args:
            modeler (interface.Model3D): 建模环境。

        Returns:
            self (BaseObject): self
        """
        pass
        # if not self._attributes:
        #     _logger.error("No valid properties.")
        # else:
        #     scmd1 = [
        #         "With xxx ",
        #         ".Reset ",
        #     ]
        #     cmd1 = NEW_LINE.join(scmd1)
        #     scmd2 = []
        #     for k, v in self._attributes.items():
        #         scmd2.append(f".{k} {v}")
        #     cmd2 = NEW_LINE.join(scmd2)
        #     scmd3 = [
        #         ".Create",
        #         "End With",
        #     ]
        #     cmd3 = NEW_LINE.join(scmd3)
        #     cmd = NEW_LINE.join((cmd1, cmd2, cmd3))
        #     modeler.add_to_history(self._history_title, cmd)
        return self

    # @abc.abstractmethod
    def create_from_kwargs(self, modeler: "interface.Model3D") -> "BaseObject":
        """从关键字参数新建对象。下面的实现给出了一个通用的范式。

        本基类不能直接用于创建实例，直接调用本方法不会得到你想要的对象，CST会直
        接报错停止运行。

        请务必在子类中重载该方法。

        Args:
            modeler (interface.Model3D): 建模环境。

        Returns:
            self (BaseObject): self
        """
        pass
        # if not self._kwargs:
        #     _logger.error("No valid properties.")
        # else:
        #     scmd1 = [
        #         "With xxx ",
        #         ".Reset ",
        #     ]
        #     cmd1 = NEW_LINE.join(scmd1)
        #     scmd2 = []
        #     for k, v in self._kwargs.items():
        #         scmd2.append(f".{k} {v}")
        #     cmd2 = NEW_LINE.join(scmd2)
        #     scmd3 = [
        #         ".Create",
        #         "End With",
        #     ]
        #     cmd3 = NEW_LINE.join(scmd3)
        #     cmd = NEW_LINE.join((cmd1, cmd2, cmd3))
        #     modeler.add_to_history(self._history_title, cmd)
        return self


class VbaObject:
    def __init__(self, code: list[str], *, title: str = "create object:"):
        self._code = code
        self._title = title
        return

    @property
    def code(self) -> list[str]:
        return self._code

    @property
    def title(self) -> str:
        return self._title

    def create(self, modeler: "interface.Model3D") -> "VbaObject":
        """直接执行【完整的vba代码】。
        （注：本方法不会修改vba代码。）

        在CST的历史记录中，标题固定为：create object:。
        建议在子类中根据不同对象的需求重载该方法。

        Args:
            modeler (interface.Model3D): 建模环境。

        Returns:
            self: 对象自身的引用。
        """
        modeler.add_to_history(self._title, NEW_LINE.join(self._code))
        _logger.info(self._title)

        return self


#######################################
# region General Methods
# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓


def change_solver_type(modeler: "interface.Model3D", solver_type: str) -> None:
    """设置求解器类型

    Valid solver types are: "HF Time Domain", "HF Eigenmode", "HF Frequency
    Domain", "HF IntegralEq", "HF Multilayer", "HF Asymptotic", "LF EStatic",
    "LF MStatic", "LF Stationary Current", "LF Frequency Domain", "LF Time
    Domain (MQS)", "PT Tracking", "PT Wakefields", "PT PIC", "Thermal Steady
    State", "Thermal Transient",  "Mechanics".

    Args:
        solver_type (str): 求解器类型。

    Returns:
        None:
    """
    modeler.add_to_history(
        f"change solver type to {solver_type}",
        f'ChangeSolverType "{solver_type}"',
    )
    return


# endregion
# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑


#######################################
# region Parameter Handling
# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

ConvertableToParameter = typing.Union[str, int, float]
ConvertableToExpression = typing.Union[str, int, float]

class Parameter(BaseObject):
    """创建和管理CST内部的参数

    Attributes:
        name (str): 变量名。
        expression (str): 表达式。
        value (float): 变量值。
    """

    def __init__(
        self,
        name: ConvertableToParameter,
        expression: ConvertableToExpression = "",
        description: str = "",
    ) -> None:
        super().__init__()
        self._name: str = str(name)

        if expression == "":
            self._expression: str = self._name
        else:
            self._expression = str(expression)

        self._description: str = description
        return

    # 属性方法

    @property
    def name(self) -> str:
        return self._name

    @property
    def expression(self) -> str:
        return self._expression

    @property
    def value(self) -> float:
        """表达式的值

        Returns
        -------
        float
            如果表达式是整数或浮点数，那么返回其数值，否则抛出异常后返回NaN
        """

        v: float = 0.0
        try:
            v = float(self.expression)
        except ValueError:
            v = float("nan")
        return v

    @property
    def description(self) -> str:
        return self._description

    def __repr__(self) -> str:

        return f"Parameter({quoted(self.name)}, {quoted(self.expression)}, {quoted(self.description)})"

    def __str__(self) -> str:
        return self.name

    def __format__(self, format_spec: str):
        return super().__format__(format_spec)

    def __add__(self, other: "Parameter") -> "Parameter":
        if isinstance(other, Parameter):
            temp = f"({self.name} + {other.name})"
        else:
            temp = f"({self.name} + {other})"
        return Parameter(temp)

    def __sub__(self, other: "Parameter") -> "Parameter":
        if isinstance(other, Parameter):
            temp = f"({self.name} - {other.name})"
        else:
            temp = f"({self.name} - {other})"
        return Parameter(temp)

    def __mul__(self, other: "Parameter") -> "Parameter":
        if isinstance(other, Parameter):
            temp = f"({self.name} * {other.name})"
        else:
            temp = f"({self.name} * {other})"

        return Parameter(temp)

    def __truediv__(self, other: "Parameter") -> "Parameter":
        if isinstance(other, Parameter):
            temp = f"({self.name} / {other.name})"
        else:
            temp = f"({self.name} / {other})"
        return Parameter(temp)

    def __abs__(self) -> "Parameter":
        temp: str = "Abs(" + self.name + ")"
        return Parameter(temp)

    def __pos__(self) -> "Parameter":
        temp = f"(+{self.name})"
        return Parameter(temp)

    def __neg__(self) -> "Parameter":
        temp = f"(-{self.name})"
        return Parameter(temp)

    def __pow__(self, power: "Parameter") -> "Parameter":
        temp = f"({self.name} ^ {power.name})"
        return Parameter(temp)

    def rename(self, n: str) -> "Parameter":
        """重命名参数。

        Args:
            n (str): 新名字。

        Returns:
            self (Parameter): 对象自身的引用。
        """
        self._name = n
        return self

    def re_describe(self, description: str) -> "Parameter":
        """重写参数的描述信息。

        Args:
            description (str): 新的描述信息。

        Returns:
            self (Parameter): 对象自身的引用。
        """
        self._description = description
        return self

    def bracket(self) -> "Parameter":
        """（还没实现好）
        给参数的表达式加括号。

        Args:
            None

        Returns:
            self (Parameter): 对象自身的引用。
        """
        self._expression = "(" + self._expression + ")"
        return self

    def store(self, modeler: "interface.Model3D") -> "Parameter":
        """将变量存储到CST中。

        Args:
            modeler (interface.Model3D): 建模环境。

        Returns:
            self (Parameter): 对象自身的引用。
        """
        modeler.add_to_history(
            f"Store parameter: {self.name}",
            'MakeSureParameterExists("'
            + self.name
            + '", "'
            + self.expression
            + '")',
        )
        if self.description != "":
            modeler.add_to_history(
                f"Set parameter description: {self.name}",
                f'SetParameterDescription("{self.name}","{self.description}")',
                timeout=1,
            )
        return self

    def delete(self, modeler: "interface.Model3D") -> "Parameter":
        """从建模环境删除变量。

        Args:
            modeler (interface.Model3D): 建模环境。

        Returns:
            self (Parameter): 对象自身的引用。
        """
        modeler.add_to_history(
            f"Delete parameter: {self.name}",
            f'DeleteParameter("{self.name}")',
        )

        return self

    def isnumber(self) -> bool:
        """判断参数是否为纯数值。

        Returns:
            bool: 是数值就返回`True`，否则返回`False`。
        """
        r: bool = False
        try:
            float(self.name)
            r = True
        except ValueError:
            r = False
        return r


# endregion
# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑


class Units(BaseObject):
    """设定CST建模环境的单位，可选项见下文。单位字符串区分大小写。

    Offers functions concerning the units of the current project.

    Attributes:
        length (str): 长度单位(默认为 mm, 可选: nm, um, mm, cm, m, mil, in, ft)。
        time (str): 时间单位(默认为 ns, 可选: fs, ps, ns, us, ms, s)。
        frequency (str): 频率单位(默认为 GHz, 可选: Hz, kHz, MHz, GHz, THz, PHz)。
        temperture (str): 温度单位(默认为 degC, 可选: degC, K, degF)。
    """

    def __init__(
        self,
        length: str = "mm",
        time: str = "ns",
        frequency: str = "GHz",
        temperture: str = "degC",
    ):
        super().__init__()
        self._length: str = length
        self._time: str = time
        self._frequency: str = frequency
        self._temperture: str = temperture
        return

    @property
    def length(self) -> str:
        return self._length

    @property
    def time(self) -> str:
        return self._time

    @property
    def frequency(self) -> str:
        return self._frequency

    @property
    def temperture(self) -> str:
        return self._temperture

    def __str__(self) -> str:
        define_unit: list[str] = [
            "With Units",
            f'.Length "{self.length}"',
            f'.Frequency "{self.frequency}"',
            f'.Time "{self.time}"',
            f'.Temperature "{self.temperture}"',
            "End With",
        ]
        cmd: str = NEW_LINE.join(define_unit)
        return cmd

    def __repr__(self) -> str:
        s: str = ", ".join(
            [
                f"Unit({quoted(self.length)}",
                f"{quoted(self.time)}",
                f"{quoted(self.frequency)}",
                f"{quoted(self.temperture)}",
            ]
        )
        return s

    def define(self, modeler: "interface.Model3D") -> "Units":
        """定义模型单位。

        Args:
            modeler (interface.Model3D): 建模环境。

        Returns:
            self (Parameter): 对象自身的引用。
        """
        define_unit: list[str] = [
            "With Units",
            f'.Geometry "{self.length}"',
            f'.Frequency "{self.frequency}"',
            f'.Time "{self.time}"',
            f'.Temperature "{self.temperture}"',
            "End With",
        ]
        cmd: str = NEW_LINE.join(define_unit)
        modeler.add_to_history("define units", cmd)
        return self


if __name__ == "__main__":
    print("hello")
    pass
