"""
已弃用，只是为了保持兼容性暂时保留。

建模需要的各种命令，未来会按CST帮助内的类别逐步分类到对应的模块中。

"""
import ast
import enum

# python 标准库
import os
import time
import types

# CST 库
import cst  # type:ignore
from cst import interface  # type:ignore

# 自己的库
from .common import NEW_LINE, quoted
from .global_ import Parameter

__all__: list[str] = []


class WCS_Type(enum.Enum):
    GLOBAL = enum.auto()
    LOCAL = enum.auto()


class WCS:
    def __init__(
        self,
        name: str = "",
        nx: str = "0",
        ny: str = "0",
        nz: str = "1",
        ox: str = "0",
        oy: str = "0",
        oz: str = "0",
        ux: str = "1",
        uy: str = "0",
        uz: str = "0",
    ):
        self._name: str = name
        self._normal_x: str = nx
        self._normal_y: str = ny
        self._normal_z: str = nz
        self._origin_x: str = ox
        self._origin_y: str = oy
        self._origin_z: str = oz
        self._uVector_x: str = ux
        self._uVector_y: str = uy
        self._uVector_z: str = uz

        return

    @property
    def name(self) -> str:
        return self._name

    @property
    def normal_x(self) -> str:
        return self._normal_x

    @property
    def normal_y(self) -> str:
        return self._normal_y

    @property
    def normal_z(self) -> str:
        return self._normal_z

    @property
    def origin_x(self) -> str:
        return self._origin_x

    @property
    def origin_y(self) -> str:
        return self._origin_y

    @property
    def origin_z(self) -> str:
        return self._origin_z

    @property
    def uVector_x(self) -> str:
        return self._uVector_x

    @property
    def uVector_y(self) -> str:
        return self._uVector_y

    @property
    def uVector_z(self) -> str:
        return self._uVector_z

    def __str__(self):
        s0 = [
            f"Name: {self._name}"
            f"Normal: {quoted(self._normal_x)}, {quoted(self._normal_y)}, "
            + f"{quoted(self._normal_z)} ",
            f"Origin: {quoted(self._origin_x)}, {quoted(self._origin_y)}, "
            + f"{quoted(self._origin_z)}",
            f"U_Vector: {quoted(self._uVector_x)}, {quoted(self._uVector_y)}, "
            + f"{quoted(self._uVector_z)})",
        ]

        return NEW_LINE.join(s0)

    def __repr__(self):
        return (
            f"{self.__class__.__name__}({quoted(self._name)}, "
            + f"{quoted(self._normal_x)}, {quoted(self._normal_y)}, {quoted(self._normal_z)}, "
            + f"{quoted(self._origin_x)}, {quoted(self._origin_y)}, {quoted(self._origin_z)}, "
            + f"{quoted(self._uVector_x)}, {quoted(self._uVector_y)}, {quoted(self._uVector_z)})"
        )

    def store(self, modeler: "interface.Model3D", name: str) -> "WCS":
        self._name = name
        modeler.add_to_history(
            f"store wcs: {self._name}", f'WCS.Store "{self._name}"'
        )
        return self

    def rename(self, n: str) -> "WCS":

        self._name = n
        return self


class Component:
    def __init__(self, name: str):
        self._name: str = name
        return

    @property
    def name(self) -> str:
        return self._name

    def __repr__(self):
        return f"{self.__class__.__name__}({quoted(self.name)})"

    def create(
        self,
        modeler: "interface.Model3D",
    ) -> "Component":
        sCommand = ["With Component ", f'.New "{self.name}"', "End With"]
        cmd = NEW_LINE.join(sCommand)
        modeler.add_to_history(
            f"new component: {self.name}",
            cmd,
        )
        return self

    def delete(
        self,
        modeler: "interface.Model3D",
    ) -> None:
        sCommand = ["With Component ", f'.Delete "{self.name}"', "End With"]
        cmd = NEW_LINE.join(sCommand)
        modeler.add_to_history(
            f"delete component: {self.name}",
            cmd,
        )
        return


class Solid:
    def __init__(self, name: str, component: str, material: str) -> None:
        self._name: str = name
        self._component: str = component
        self._material: str = material
        return

    @property
    def name(self) -> str:
        return self._name

    @property
    def component(self) -> str:
        return self._component

    @property
    def material(self) -> str:
        return self._material


class Brick(Solid):
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
            f"xmin: {self.xmin}",
            f"xmax: {self.xmax}",
            f"ymin: {self.ymin}",
            f"ymax: {self.ymax}",
            f"zmin: {self.zmin}",
            f"zmax: {self.zmax}",
            f"Component: {self.component}",
            f"Material: {self.material}",
        ]
        return NEW_LINE.join(l)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}({quoted(self._name)}, {quoted(self.xmin)}, "
            + f"{quoted(self.xmax)}, "
            + f"{quoted(self.ymin)}, {quoted(self.ymax)}, "
            + f"{quoted(self.zmin)}, {quoted(self.zmax)}, "
            + f"{quoted(self.component)}, {quoted(self.material)})"
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
            f'.Name "{self.name}"',
            f'.Component "{self.component}"',
            f'.Material "{self.material}"',
            f'.Xrange "{self.xmin}","{self.xmax}"',
            f'.Yrange "{self.ymin}","{self.ymax}"',
            f'.Zrange "{self.zmin}","{self.zmax}"',
            ".Create",
            "End With",
        ]
        cmd = NEW_LINE.join(sCommand)
        modeler.add_to_history(
            f'define brick: "{self.component}: {self.name}"',
            cmd,
        )
        return self


#######################################
# region 建模环境设置
# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓


def define_units(modeler: "interface.Model3D", u: list[str]) -> None:
    """定义建模单位。

    Args:
        modeler (cst.interface.Model3D): 建模环境。
        u (list[str]): With Unit 指令字符串。
    Returns:
        None:
    """

    cmd: str = NEW_LINE.join(u)
    modeler.add_to_history("define units", cmd)
    return


def define_frequency_range(
    modeler: "interface.Model3D", fmin: Parameter, fmax: Parameter
) -> None:
    """定义频率范围。
    频率单位在define_units中设置。

    Args:
        modeler (cst.interface.Model3D): 建模环境。
        fmin (float): 最小频率。
        fmax (float): 最大频率。
    Returns:
        None:
    """

    modeler.add_to_history(
        "define frequency range",
        f'Solver.FrequencyRange "{fmin.name}","{fmax.name}"',
    )
    return


def define_background(modeler: "interface.Model3D", bg: list[str]) -> None:
    """定义背景材料。

    Args:
        modeler (cst.interface.Model3D): 建模环境。
        u (list[str]): With Background 指令字符串。
    Returns:
        None:
    """

    cmd: str = NEW_LINE.join(bg)
    modeler.add_to_history("define background", cmd)
    return


def define_boundary(modeler: "interface.Model3D", b: list[str]) -> None:
    """定义边界条件。

    Args:
        modeler (cst.interface.Model3D): 建模环境。
        u (Unit): 需要设置的边界条件。
    Returns:
        None:
    """

    cmd: str = NEW_LINE.join(b)
    modeler.add_to_history("define boundary", cmd)
    return


def define_material(modeler: "interface.Model3D", mat: list[str]) -> None:
    """定义材料。

    Args:
        modeler (cst.interface.Model3D): 建模环境。
        mat (Material): 材料属性。

    """

    cmd: str = NEW_LINE.join(mat)
    modeler.add_to_history("define material: " + mat[2], cmd)
    return


def define_port(modeler: "interface.Model3D", p: list[str]) -> None:
    """定义端口。

    Args:
        modeler (cst.interface.Model3D): 建模环境。
        mat (Material): 材料属性。

    """

    cmd: str = NEW_LINE.join(p)
    modeler.add_to_history("define port: ", cmd)
    return


def activate_WCS(modeler: "interface.Model3D", c: str) -> None:
    """激活全局或局部坐标系。

    Args:
        modeler (interface.Model3D): 建模环境。
        c (str): 坐标系类型，可选 "local" 和 "global"。

    Returns:
        type:
    """
    if c == "global":
        modeler.add_to_history(
            "activate global coordinates",
            'WCS.ActivateWCS "global"',
        )
    elif c == "local":
        modeler.add_to_history(
            "activate local coordinates",
            'WCS.ActivateWCS "local"',
        )
    else:
        pass
    # match c:
    #     case "global":
    #         modeler.add_to_history(
    #             "activate global coordinates",
    #             'WCS.ActivateWCS "global"',
    #         )
    #     case "local":
    #         modeler.add_to_history(
    #             "activate local coordinates",
    #             'WCS.ActivateWCS "local"',
    #         )
    #     case _:
    #         pass

    return


def set_WCS_properties(modeler: "interface.Model3D", w: WCS) -> None:
    sCommand = [
        "With WCS",
        f'.SetNormal "{w.normal_x}", "{w.normal_y}", "{w.normal_z}"',
        f'.SetOrigin "{w.origin_x}", "{w.origin_y}", "{w.origin_z}"',
        f'.SetUVector "{w.uVector_x}", "{w.uVector_y}", "{w.uVector_z}"',
        "End With",
    ]
    cmd: str = NEW_LINE.join(sCommand)
    modeler.add_to_history(f"set wcs properties: {w.name}", cmd)
    return


def store_WCS(modeler: "interface.Model3D", w: WCS) -> None:
    modeler.add_to_history(f"store WCS: {w.name}", f'WCS.Store "{w.name}"')
    return


# endregion
# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

#######################################
# region 建模视图设置
# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓


def show_bounding_box(modeler: "interface.Model3D", show: bool) -> None:
    """模型边界框的显示设置。

    Args:
        self (cst.interface.Model3D): 建模环境。
        show (bool): 显示边框则为。

    """
    if show is True:
        cmd = 'Plot.DrawBox "True"'
    else:
        cmd = 'Plot.DrawBox "False"'
    modeler.add_to_history("switch bounding box", cmd)
    return


# endregion
# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

#######################################
# region 实体建模命令
# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓


def new_component(modeler: "interface.Model3D", c: str) -> None:
    """定义实体分组（component）。

    Args:
        modeler (interface.Model3D): 建模环境。
        c (str): 分组（component）名。

    """
    sCommand = ["With Component ", f'.New "{c}"', "End With"]
    cmd = NEW_LINE.join(sCommand)
    modeler.add_to_history(
        f"new component: {c}",
        cmd,
    )
    return


def define_brick(modeler: "interface.Model3D", b: Brick) -> None:
    """定义立方体。

    Args:
        modeler (interface.Model3D): 建模环境。
        b (Brick): 立方体对象。

    """
    sCommand = [
        "With Brick",
        ".Reset",
        f'.Name "{b.name}"',
        f'.Component "{b.component}"',
        f'.Material "{b.material}"',
        f'.Xrange "{b.xmin}","{b.xmax}"',
        f'.Yrange "{b.ymin}","{b.ymax}"',
        f'.Zrange "{b.zmin}","{b.zmax}"',
        ".Create",
        "End With",
    ]
    cmd = NEW_LINE.join(sCommand)
    modeler.add_to_history(
        f'define brick: "{b.component}: {b.name}"',
        cmd,
    )
    return


def solid_add(modeler: "interface.Model3D", s1: Solid, s2: Solid) -> None:
    title = f"boolean add shapes: {s1.component}:{s1.name}, {s2.component}:{s2.name}"
    cmd = f'Solid.Add "{s1.component}:{s1.name}", "{s2.component}:{s2.name}"'
    modeler.add_to_history(
        title,
        cmd,
    )
    return


# endregion
# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

#######################################
# region 求解器命令
# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓


def change_solver_type(modeler: "interface.Model3D", solver_type: str) -> None:
    """设置求解器类型

    Valid solver types are: "HF Time Domain", "HF Eigenmode", "HF Frequency
    Domain", "HF IntegralEq", "HF Multilayer", "HF Asymptotic", "LF EStatic",
    "LF MStatic", "LF Stationary Current", "LF Frequency Domain", "LF Time
    Domain (MQS)", "PT Tracking", "PT Wakefields", "PT PIC", "Thermal Steady
    State", "Thermal Transient",  "Mechanics".

    Args:
        param1 (type): 第1个参数。

    Returns:
        type:
    """
    modeler.add_to_history(
        "change solver type",
        f'ChangeSolverType "{solver_type}"',
    )
    return


def define_frequency_domain_solver_parameters(
    modeler: "interface.Model3D", slover_settings: list[str]
) -> None:
    cmd: str = NEW_LINE.join(slover_settings)
    modeler.add_to_history(
        "define frequency domain solver parameters",
        cmd,
    )
    return


def define_Floquet_port_boundaries(
    modeler: "interface.Model3D", port_boundaries: list[str]
) -> None:
    cmd: str = NEW_LINE.join(port_boundaries)
    modeler.add_to_history(
        "define Floquet port boundaries",
        cmd,
    )
    return


def start_FDSolver(modeler: "interface.Model3D") -> None:
    sCommand = ["With FDSolver", "   .Start", "End With"]
    cmd = NEW_LINE.join(sCommand)
    modeler.add_to_history(
        "Starts FDSolver",
        cmd,
    )


# endregion
# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

