"""本模块用于定义各种模型实体。"""

# python 标准库
import ast
import enum
import logging
import os
import time
import types

from . import interface
from ._global import Parameter
from .common import NEW_LINE, OPERATION_FAILED, OPERATION_SUCCESS, quoted
from .shape_operations import Solid

_logger = logging.getLogger(__name__)


class Brick(Solid):
    """This object is used to create a new brick shape.

    Attributes:
        name (str): 名称。
        xmin (str): `x`下界。
        xmax (str): `x`上界。
        ymin (str): `y`下界。
        ymax (str): `y`上界。
        zmin (str): `z`下界。
        zmax (str): `z`上界。
        component (str): 所在组件名。
        material (str): 材料名。
    """

    def __init__(
        self,
        name: str,
        xmin: str,
        xmax: str,
        ymin: str,
        ymax: str,
        zmin: str,
        zmax: str,
        component: str,
        material: str,
    ) -> None:
        super().__init__(name, component, material)

        self._xmin: str = xmin
        self._xmax: str = xmax
        self._ymin: str = ymin
        self._ymax: str = ymax
        self._zmin: str = zmin
        self._zmax: str = zmax
        self._history_title = f'define brick: "{self.component}:{self.name}"'

        return

    @property
    def xmin(self) -> str:
        return self._xmin

    @property
    def xmax(self) -> str:
        return self._xmax

    @property
    def ymin(self) -> str:
        return self._ymin

    @property
    def ymax(self) -> str:
        return self._ymax

    @property
    def zmin(self) -> str:
        return self._zmin

    @property
    def zmax(self) -> str:
        return self._zmax

    @property
    def component(self) -> str:
        return self._component

    @property
    def material(self) -> str:
        return self._material

    def __str__(self) -> str:
        l = [
            f"Brick: {self._name}",
            f"xmin: {self._xmin}",
            f"xmax: {self._xmax}",
            f"ymin: {self._ymin}",
            f"ymax: {self._ymax}",
            f"zmin: {self._zmin}",
            f"zmax: {self._zmax}",
            f"Component: {self._component}",
            f"Material: {self._material}",
        ]
        return NEW_LINE.join(l)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}({quoted(self._name)}, {quoted(self._xmin)}, "
            + f"{quoted(self._xmax)}, "
            + f"{quoted(self._ymin)}, {quoted(self._ymax)}, "
            + f"{quoted(self._zmin)}, {quoted(self._zmax)}, "
            + f"{quoted(self._component)}, {quoted(self._material)})"
        )

    def create(self, modeler: "interface.Model3D") -> "Brick":
        """定义立方体。

        Args:
            modeler (interface.Model3D): 建模环境。

        Returns:
            self: 对象自身的引用。

        """

        sCommand = [
            "With Brick",
            ".Reset",
            f'.Name "{self._name}"',
            f'.Component "{self._component}"',
            f'.Material "{self._material}"',
            f'.Xrange "{self._xmin}","{self._xmax}"',
            f'.Yrange "{self._ymin}","{self._ymax}"',
            f'.Zrange "{self._zmin}","{self._zmax}"',
            ".Create",
            "End With",
        ]
        cmd = NEW_LINE.join(sCommand)

        modeler.add_to_history(self._history_title, cmd)
        _logger.info("Brick %s:%s created.", self._component, self._name)
        return self


class AnalyticalFace(Solid):
    """This object is used to create a new analytical face shape.

    Attributes:
        name (str): 实体名称。
        component (str | Component): 实体所在的部件（component）名称。
        material (str | Material): 实体的材料名称。

    """

    u = Parameter("u")
    v = Parameter("v")

    def __init__(
        self,
        name: str,
        component: str,
        material: str,
        law_x: str,
        law_y: str,
        law_z: str,
        range_u: list[str],
        range_v: list[str],
    ):
        super().__init__(name, component, material)
        self._law_x = law_x
        self._law_y = law_y
        self._law_z = law_z
        self._range_u = range_u
        self._range_v = range_v
        return

    @property
    def law_x(self):
        return self._law_x

    @property
    def law_y(self):
        return self._law_y

    @property
    def law_z(self):
        return self._law_z

    @property
    def range_u(self):
        return self._range_u

    @property
    def range_v(self):
        return self._range_v

    def create(self, modeler) -> "AnalyticalFace":
        """定义解析表面。

        Args:
            modeler (interface.Model3D): 建模环境。

        Returns:
            self: 对象自身的引用。

        """

        sCommand = [
            "With AnalyticalFace",
            ".Reset",
            f'.Name "{self.name}"',
            f'.Component "{self.component}"',
            f'.Material "{self.material}"',
            f'.LawX "{self.law_x}"',
            f'.LawY "{self.law_y}"',
            f'.LawZ "{self.law_z}"',
            f'.ParameterRangeU "{self.range_u[0]}", "{self.range_u[1]}"',
            f'.ParameterRangeV "{self.range_v[0]}", "{self.range_v[1]}"',
            ".Create",
            "End With",
        ]
        cmd = NEW_LINE.join(sCommand)
        title = f'define Analytical Face: "{self.component}:{self.name}"'
        modeler.add_to_history(title, cmd)
        _logger.info(
            "Analytical Face %s:%s created.", self.component, self.name
        )
        return self


class Cylinder(Solid):
    """This object is used to create a new cylinder shape.

    Attributes:
        name (str): 名称。
        r_in (str): 半径。
        r_out (str): 半径。
        height (str): 高度。
        component (str): 所在组件名。
        material (str): 材料名。
    """

    def __init__(
        self,
        name: str,
        component: str,
        material: str,
        axis: str,
        r_in: str,
        r_out: str,
        center_1: str,
        center_2: str,
        range_1: str,
        range_2: str,
        segments: int = 0,
    ) -> None:
        super().__init__(name, component, material)
        self._axis: str = axis
        self._r_in: str = r_in
        self._r_out: str = r_out
        self._center_1: str = center_1
        self._center_2: str = center_2
        self._range_1: str = range_1
        self._range_2: str = range_2
        self._segments: int = segments
        self._history_title = f'define cylinder: "{self.component}:{self.name}"'
        return

    @property
    def r_in(self) -> str:
        return self._r_in

    @property
    def range(self) -> tuple[str, str]:
        return (self._range_1, self._range_2)

    @property
    def center(self) -> tuple[str, str]:
        return (self._center_1, self._center_2)

    @property
    def component(self) -> str:
        return self._component

    @property
    def material(self) -> str:
        return self._material

    @property
    def segments(self) -> int:
        """This setting specifies how the cylinder's geometry is modelled,
        either as a smooth surface of by a facetted approximation. If this value
        is set to "0", an analytical (smooth) representation of the cylinder
        will be created. If this number is set to another value greater than 2,
        the cylinder's face will be approximated by this number of planar facets.
        The higher the number of segments, the better the representation of the
        cylinder will be."""
        return self._segments

    def create(self, modeler):
        """定义圆柱体。

        Parameters
        ----------
        modeler : Model3D
            建模环境。

        Returns
        -------
        self
            自身的引用。
        """
        sCommand = [
            "With Cylinder ",
            ".Reset ",
            f'.Name "{self._name}" ',
            f'.Component "{self._component}" ',
            f'.Material "{self._material}" ',
            f'.OuterRadius "{self._r_out}" ',
            f'.InnerRadius "{self._r_in}" ',
            f'.Axis "{self._axis}" ',
        ]
        match self._axis.upper():
            case "X":
                sCommand += [
                    f'.Xrange "{self._range_1}", "{self._range_2}" ',
                    f'.Ycenter "{self._center_1}" ',
                    f'.Zcenter "{self._center_2}" ',
                ]
            case "Y":
                sCommand += [
                    f'.Yrange "{self._range_1}", "{self._range_2}" ',
                    f'.Xcenter "{self._center_1}" ',
                    f'.Zcenter "{self._center_2}" ',
                ]
            case "Z":
                sCommand += [
                    f'.Zrange "{self._range_1}", "{self._range_2}" ',
                    f'.Xcenter "{self._center_1}" ',
                    f'.Ycenter "{self._center_2}" ',
                ]
            case _:
                _logger.error(
                    "Cylinder axis must be one of 'X', 'Y', or 'Z'."
                )
                raise ValueError(
                    f"Invalid axis: {self._axis}. Must be 'X', 'Y', or 'Z'."
                )

        sCommand += [
            f'.Segments "{self._segments}" ',
            ".Create ",
            "End With",
        ]

        cmd = NEW_LINE.join(sCommand)

        modeler.add_to_history(self._history_title, cmd)
        _logger.info("Cylinder %s:%s created.", self._component, self._name)

        return self
