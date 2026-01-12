"""本模块用于定义各种曲线。"""

# python 标准库
import logging
import typing

# CST 库
import cst  # type:ignore
from cst import interface  # type:ignore

# 自己的库
from .common import NEW_LINE, OPERATION_FAILED, OPERATION_SUCCESS, quoted
from .global_ import BaseObject, Parameter
from .shape_operations import Solid

_logger = logging.getLogger(__name__)


class Line(BaseObject):
    def __init__(
        self,
        name: str,
        curve: str,
        x1: Parameter,
        y1: Parameter,
        x2: Parameter,
        y2: Parameter,
        
    ):
        super().__init__()
        self._name = name
        self._curve = curve
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        return

    #######################################
    # region 类方法
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    #######################################
    # region 属性方法
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

    @property
    def name(self) -> str:
        return self._name

    @property
    def curve(self) -> str:
        return self._curve

    @property
    def x1(self) -> str:
        return self._x1.name

    @property
    def x2(self) -> str:
        return self._x2.name

    @property
    def y1(self) -> str:
        return self._y1.name

    @property
    def y2(self) -> str:
        return self._y2.name
    
    @property
    def full_name(self) -> str:
        """返回实体的全名

        Returns:
            str: 实体的全名，形式为`curve:name`
        """
        return f"{self.curve}:{self.name}"

    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    #######################################
    # region 特殊方法
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    #######################################
    # region 其他方法
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
    def create(self, modeler: "interface.Model3D") -> "Line":
        """定义线段。

        Args:
            modeler (interface.Model3D): 建模环境。

        Returns:
            self: 对象自身的引用。

        """

        sCommand = [
                "With Line",
            ".Reset ",
            f'.Name "{self.name}" ',
            f'.Curve "{self.curve}" ',
            f'.X1 "{self.x1}" ',
            f'.Y1 "{self.y1}" ',
            f'.X2 "{self.x2}" ',
            f'.Y2 "{self.y2}" ',
            ".Create",
            "End With",
        ]
        cmd = NEW_LINE.join(sCommand)
        title = f'define curve line: "{self.full_name}"'
        modeler.add_to_history(title, cmd)
        _logger.info("curve line %s created.", self.full_name)
        return self

    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
