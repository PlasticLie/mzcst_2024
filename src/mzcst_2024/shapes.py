"""本模块用于定义各种模型实体。"""

# python 标准库
import ast
import enum
import logging
import os
import time
import types
import typing

from . import interface
from .common import NEW_LINE, OPERATION_FAILED, OPERATION_SUCCESS, quoted
from .global_ import Parameter
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
        self._history.append(f"define brick: {self._component}:{self._name}")   
        modeler.add_to_history(self._history[-1], cmd)
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


class Cone(Solid):
    """This object is used to create a new cone shape.

    Attributes:
        name (str): 名称。
        component (str): 所在组件名。
        material (str): 材料名。
        axis (str): 轴向，取值为 "X"、"Y" 或 "Z"。
        top_radius (str): 圆锥顶面半径。
        bottom_radius (str): 圆锥底面半径。
        xcenter (str): 圆锥中心在X轴上的坐标。
        ycenter (str): 圆锥中心在Y轴上的坐标。
        zcenter (str): 圆锥中心在Z轴上的坐标。
        xrange (tuple[str, str]): 圆锥在X轴上的范围，格式为 (xmin, xmax)。
        yrange (tuple[str, str]): 圆锥在Y轴上的范围，格式为 (ymin, ymax)。
        zrange (tuple[str, str]): 圆锥在Z轴上的范围，格式为 (zmin, zmax)。
        segments (int): 圆锥的面片数。该设置指定了圆锥的几何形状是以光滑的表面还是以近似的面片来建模。如果该值设置为 "0"，则会创建一个分析（光滑）表示的圆锥。如果该数字设置为大于 2 的其他值，则圆锥的面将由该数量的平面面片近似表示。面片数量越多，圆锥的表示就越好。
    """

    def __init__(
        self,
        name,
        component,
        material,
        axis: typing.Literal["X", "Y", "Z"],
        top_radius: str,
        bottom_radius: str,
        xcenter: str,
        ycenter: str,
        zcenter: str,
        xrange: tuple[str, str],
        yrange: tuple[str, str],
        zrange: tuple[str, str],
        segments: str,
    ):
        super().__init__(name, component, material)
        self._axis = axis
        self._top_radius = top_radius
        self._bottom_radius = bottom_radius
        self._xcenter = xcenter
        self._ycenter = ycenter
        self._zcenter = zcenter
        self._xrange = xrange
        self._yrange = yrange
        self._zrange = zrange
        self._segments = segments
        return

    @property
    def axis(self) -> str:
        return self._axis

    @property
    def top_radius(self) -> str:
        return self._top_radius

    @property
    def bottom_radius(self) -> str:
        return self._bottom_radius

    @property
    def xcenter(self) -> str:
        return self._xcenter

    @property
    def ycenter(self) -> str:
        return self._ycenter

    @property
    def zcenter(self) -> str:
        return self._zcenter

    @property
    def xrange(self) -> tuple[str, str]:
        return self._xrange

    @property
    def yrange(self) -> tuple[str, str]:
        return self._yrange

    @property
    def zrange(self) -> tuple[str, str]:
        return self._zrange

    @property
    def segments(self) -> str:
        """This setting specifies how the cone's geometry is modelled, either as a smooth surface of by a facetted approximation. If this value is set to "0", an analytical (smooth) representation of the cone will be created. If this number is set to another value greater than 2, the cone's face will be approximated by this number of planar facets. The higher the number of segments, the better the representation of the cone will be."""
        return self._segments

    def create(self, modeler: interface.Model3D) -> "Cone":
        """定义圆锥体。

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
            "With Cone ",
            ".Reset ",
            f'.Name "{self._name}" ',
            f'.Component "{self._component}" ',
            f'.Material "{self._material}" ',
            f'.TopRadius "{self._top_radius}" ',
            f'.BottomRadius "{self._bottom_radius}" ',
            f'.Xcenter "{self._xcenter}" ',
            f'.Ycenter "{self._ycenter}" ',
            f'.Zcenter "{self._zcenter}" ',
            f'.Xrange "{self._xrange[0]}", "{self._xrange[1]}" ',
            f'.Yrange "{self._yrange[0]}", "{self._yrange[1]}" ',
            f'.Zrange "{self._zrange[0]}", "{self._zrange[1]}" ',
            f'.Axis "{self._axis}" ',
            f'.Segments "{self._segments}" ',
            ".Create ",
            "End With",
        ]

        cmd = NEW_LINE.join(sCommand)
        self._history.append(f'define cone: "{self.full_name}"')
        modeler.add_to_history(self._history[-1], cmd)
        _logger.info("Cone %s created.", self.full_name)
        return self


class Cylinder(Solid):
    """This object is used to create a new cylinder shape.

    Attributes:
        name (str): 名称。
        r_in (str): 内半径。
        r_out (str): 外半径。
        height (str): 高度。
        component (str): 所在组件名。
        material (str): 材料名。
    """

    def __init__(
        self,
        name: str,
        component: str,
        material: str,
        axis: typing.Literal["X", "Y", "Z"],
        r_in: str,
        r_out: str,
        center_1: str,
        center_2: str,
        range_1: str,
        range_2: str,
        segments: int = 0,
    ) -> None:
        super().__init__(name, component, material)
        self._axis: typing.Literal["X", "Y", "Z"] = axis
        self._r_in: str = r_in
        self._r_out: str = r_out
        self._center_1: str = center_1
        self._center_2: str = center_2
        self._range_1: str = range_1
        self._range_2: str = range_2
        self._segments: int = segments
        
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

    def create(self, modeler: interface.Model3D) -> "Cylinder":
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
                _logger.error("Cylinder axis must be one of 'X', 'Y', or 'Z'.")
                raise ValueError(
                    f"Invalid axis: {self._axis}. Must be 'X', 'Y', or 'Z'."
                )

        sCommand += [
            f'.Segments "{self._segments}" ',
            ".Create ",
            "End With",
        ]

        cmd = NEW_LINE.join(sCommand)
        self._history.append(f'define cylinder: "{self.component}:{self.name}"')
        modeler.add_to_history(self._history[-1], cmd)
        _logger.info("Cylinder %s:%s created.", self._component, self._name)

        return self


class ECylinder(Solid):
    """This object is used to create a new elliptical cylinder shape.

    Attributes:
        name (str): 名称。
        component (str): 所在组件名。
        material (str): 材料名。
        axis (str): 轴向，取值为 "X"、"Y" 或 "Z"。
        x_radius (str): 椭圆在X轴方向的半径。
        y_radius (str): 椭圆在Y轴方向的半径。
        z_radius (str): 椭圆在Z轴方向的半径。
        x_center (str): 椭圆中心在X轴上的坐标。
        y_center (str): 椭圆中心在Y轴上的坐标。
        z_center (str): 椭圆中心在Z轴上的坐标。
        x_range (tuple[str, str]): 椭圆在X轴上的范围，格式为 (xmin, xmax)。
        y_range (tuple[str, str]): 椭圆在Y轴上的范围，格式为 (ymin, ymax)。
        z_range (tuple[str, str]): 椭圆在Z轴上的范围，格式为 (zmin, zmax)。
        segments (str): 椭圆柱的面片数。该设置指定了椭圆柱的几何形状是以光滑的表面还是以近似的面片来建模。如果该值设置为 "0"，则会创建一个分析（光滑）表示的椭圆柱。如果该数字设置为大于 2 的其他值，则椭圆柱的面将由该数量的平面面片近似表示。面片数量越多，椭圆柱的表示就越好。
    """

    def __init__(
        self,
        name,
        component,
        material,
        axis: typing.Literal["X", "Y", "Z"],
        x_radius: str,
        y_radius: str,
        z_radius: str,
        x_center: str,
        y_center: str,
        z_center: str,
        x_range: tuple[str, str],
        y_range: tuple[str, str],
        z_range: tuple[str, str],
        segments: str,
    ):
        super().__init__(name, component, material)
        self._axis = axis
        self._x_radius = x_radius
        self._y_radius = y_radius
        self._z_radius = z_radius
        self._x_center = x_center
        self._y_center = y_center
        self._z_center = z_center
        self._x_range = x_range
        self._y_range = y_range
        self._z_range = z_range
        self._segments = segments
        return

    @property
    def axis(self) -> str:
        return self._axis

    @property
    def x_radius(self) -> str:
        return self._x_radius

    @property
    def y_radius(self) -> str:
        return self._y_radius

    @property
    def z_radius(self) -> str:
        return self._z_radius

    @property
    def x_center(self) -> str:
        return self._x_center

    @property
    def y_center(self) -> str:
        return self._y_center

    @property
    def z_center(self) -> str:
        return self._z_center

    @property
    def x_range(self) -> tuple[str, str]:
        return self._x_range

    @property
    def y_range(self) -> tuple[str, str]:
        return self._y_range

    @property
    def z_range(self) -> tuple[str, str]:
        return self._z_range

    @property
    def segments(self) -> str:
        """This setting specifies how the elliptical cylinder's geometry is modelled, either as a smooth surface of by a facetted approximation. If this value is set to "0", an analytical (smooth) representation of the elliptical cylinder will be created. If this number is set to another value greater than 2, the elliptical cylinder's face will be approximated by this number of planar facets. The higher the number of segments, the better the representation of the elliptical cylinder will be."""
        return self._segments

    def create(self, modeler: interface.Model3D) -> "ECylinder":
        """定义椭圆柱体。

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
            "With ECylinder ",
            ".Reset ",
            f'.Name "{self._name}" ',
            f'.Component "{self._component}" ',
            f'.Material "{self._material}" ',
            f'.Xradius "{self._x_radius}" ',
            f'.Yradius "{self._y_radius}" ',
            f'.Zradius "{self._z_radius}" ',
            f'.Xcenter "{self._x_center}" ',
            f'.Ycenter "{self._y_center}" ',
            f'.Zcenter "{self._z_center}" ',
            f'.Xrange "{self._x_range[0]}", "{self._x_range[1]}" ',
            f'.Yrange "{self._y_range[0]}", "{self._y_range[1]}" ',
            f'.Zrange "{self._z_range[0]}", "{self._z_range[1]}" ',
            f'.Axis "{self._axis}" ',
            f'.Segments "{self._segments}" ',
            ".Create ",
            "End With",
        ]

        cmd = NEW_LINE.join(sCommand)
        self._history.append(f'define elliptical cylinder: "{self.full_name}"')
        modeler.add_to_history(self._history[-1], cmd)
        _logger.info("Elliptical Cylinder %s created.", self.full_name)
        return self


class Sphere(Solid):
    """This object is used to create a new sphere shape.

    Attributes:
        name (str): 名称。
        component (str): 所在组件名。
        material (str): 材料名。
        axis (typing.Literal["X", "Y", "Z"]): 轴向，取值为 "X"、"Y" 或 "Z"。
        center_radius (str): 球的半径。
        top_radius (str): 球顶面半径。
        bottom_radius (str): 球底面半径。
        center (tuple[str, str, str]): 球心坐标，格式为 (x_center, y_center, z_center)。
        segments (str): 球的面片数。该设置指定了球的几何形状是以光滑的表面还是以近似的面片来建模。如果该值设置为 "0"，则会创建一个分析（光滑）表示的球。如果该数字设置为大于 2 的其他值，则球的面将由该数量的平面面片近似表示。面片数量越多，球的表示就越好。
    """

    def __init__(
        self,
        name,
        component,
        material,
        axis: typing.Literal["X", "Y", "Z"],
        center_radius: str,
        top_radius: str,
        bottom_radius: str,
        center: tuple[str, str, str],
        segments: str,
    ):
        super().__init__(name, component, material)
        self._axis = axis
        self._center_radius = center_radius
        self._top_radius = top_radius
        self._bottom_radius = bottom_radius
        self._center = center
        self._segments = segments
        return

    @property
    def axis(self) -> str:
        return self._axis

    @property
    def center_radius(self) -> str:
        return self._center_radius

    @property
    def top_radius(self) -> str:
        return self._top_radius

    @property
    def bottom_radius(self) -> str:
        return self._bottom_radius

    @property
    def center(self) -> tuple[str, str, str]:
        return self._center

    @property
    def segments(self) -> str:
        """This setting specifies how the sphere's geometry is modelled, either as a smooth surface of by a facetted approximation. If this value is set to "0", an analytical (smooth) representation of the sphere will be created. If this number is set to another value greater than 2, the sphere's face will be approximated by this number of planar facets. The higher the number of segments, the better the representation of the sphere will be."""
        return self._segments

    def create(self, modeler: interface.Model3D) -> "Sphere":
        """定义球体。

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
            "With Sphere ",
            ".Reset ",
            f'.Name "{self._name}" ',
            f'.Component "{self._component}" ',
            f'.Material "{self._material}" ',
            f'.Axis "{self._axis}" ',
            f'.CenterRadius "{self._center_radius}" ',
            f'.TopRadius "{self._top_radius}" ',
            f'.BottomRadius "{self._bottom_radius}" ',
            f'.Center "{self._center[0]}", "{self._center[1]}", "{self._center[2]}" ',
            f'.Segments "{self._segments}" ',
            ".Create ",
            "End With",
        ]
        cmd = NEW_LINE.join(sCommand)
        self._history.append(f'define sphere: "{self.full_name}"')
        modeler.add_to_history(self._history[-1], cmd)
        _logger.info("Sphere %s created.", self.full_name)
        return self


class Torus(Solid):
    """This object is used to create a new torus shape.

    Attributes:
        name (str): 名称。
        component (str): 所在组件名。
        material (str): 材料名。
        axis (typing.Literal["X", "Y", "Z"]): 轴向，取值为 "X"、"Y" 或 "Z"。
        outer_radius (str): 圆环的外半径。
        inner_radius (str): 圆环的内半径。
        x_center (str): 圆环中心在X轴上的坐标。
        y_center (str): 圆环中心在Y轴上的坐标。
        z_center (str): 圆环中心在Z轴上的坐标。
        segments (str): 圆环的面片数。该设置指定了圆环的几何形状是以光滑的表面还是以近似的面片来建模。如果该值设置为 "0"，则会创建一个分析（光滑）表示的圆环。如果该数字设置为大于 2 的其他值，则圆环的面将由该数量的平面面片近似表示。面片数量越多，圆环的表示就越好。
    """

    def __init__(
        self,
        name,
        component,
        material,
        axis: typing.Literal["X", "Y", "Z"],
        outer_radius: str,
        inner_radius: str,
        x_center: str,
        y_center: str,
        z_center: str,
        segments: str,
    ):
        super().__init__(name, component, material)
        self._axis = axis
        self._outer_radius = outer_radius
        self._inner_radius = inner_radius
        self._x_center = x_center
        self._y_center = y_center
        self._z_center = z_center
        self._segments = segments
        return

    @property
    def axis(self) -> str:
        return self._axis

    @property
    def outer_radius(self) -> str:
        return self._outer_radius

    @property
    def inner_radius(self) -> str:
        return self._inner_radius

    @property
    def x_center(self) -> str:
        return self._x_center

    @property
    def y_center(self) -> str:
        return self._y_center

    @property
    def z_center(self) -> str:
        return self._z_center

    @property
    def segments(self) -> str:
        """This setting specifies how the torus's geometry is modelled, either as a smooth surface of by a facetted approximation. If this value is set to "0", an analytical (smooth) representation of the torus will be created. If this number is set to another value greater than 2, the torus's face will be approximated by this number of planar facets. The higher the number of segments, the better the representation of the torus will be."""
        return self._segments

    def create(self, modeler: interface.Model3D) -> "Torus":
        """定义圆环体。

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
            "With Torus ",
            ".Reset ",
            f'.Name "{self._name}" ',
            f'.Component "{self._component}" ',
            f'.Material "{self._material}" ',
            f'.Axis "{self._axis}" ',
            f'.OuterRadius "{self._outer_radius}" ',
            f'.InnerRadius "{self._inner_radius}" ',
            f'.Xcenter "{self._x_center}" ',
            f'.Ycenter "{self._y_center}" ',
            f'.Zcenter "{self._z_center}" ',
            f'.Segments "{self._segments}" ',
            ".Create ",
            "End With",
        ]
        cmd = NEW_LINE.join(sCommand)
        self._history.append(f'define torus: "{self.full_name}"')
        modeler.add_to_history(self._history[-1], cmd)
        _logger.info("Torus %s created.", self.full_name)
        return self


class Wire:
    """[todo] This object is used to create a new wire shape."""

    def __init__(
        self,
        name: str,
        folder: str,
        type_: typing.Literal["Bondwire", "Curvewire"],
    ):
        self._name = name
        self._folder = folder
        self._type = type_
        return
