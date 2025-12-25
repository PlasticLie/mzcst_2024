import enum
import logging
import typing

from . import interface
from ._global import BaseObject, Parameter
from .common import NEW_LINE, OPERATION_FAILED, OPERATION_SUCCESS, quoted
from .shape_operations import Solid

__all__: list[str] = []

_logger = logging.getLogger(__name__)


class WCS_Type(enum.Enum):
    GLOBAL = enum.auto()
    LOCAL = enum.auto()


class WCS:
    """Defines a working coordinate system which will be the base for the next
    new solids.
    """

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

    #######################################
    # region 类方法
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

    @classmethod
    def activate(
        cls, modeler: "interface.Model3D", c: typing.Literal["local", "global"]
    ) -> None:
        """激活全局或局部坐标系。

        Args:
            modeler (interface.Model3D): 建模环境。
            c (str): 坐标系类型，可选 `"local"` 和 `"global"`。

        Returns:
            type:
        """
        match c:
            case "global":
                modeler.add_to_history(
                    "activate global coordinates",
                    'WCS.ActivateWCS "global"',
                )
            case "local":
                modeler.add_to_history(
                    "activate local coordinates",
                    'WCS.ActivateWCS "local"',
                )
            case _:
                _logger.error("Invalid WCS type.")
        return

    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    #######################################
    # region 属性方法
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

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

    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    #######################################
    # region 特殊方法
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

    def __str__(self):
        s0 = [
            f"Name: {self._name}",
            f"Normal: [{quoted(self._normal_x)}, {quoted(self._normal_y)}, "
            + f"{quoted(self._normal_z)}]",
            f"Origin: [{quoted(self._origin_x)}, {quoted(self._origin_y)}, "
            + f"{quoted(self._origin_z)}]",
            f"U_Vector: [{quoted(self._uVector_x)}, {quoted(self._uVector_y)}, "
            + f"{quoted(self._uVector_z)}]",
        ]

        return ", ".join(s0)

    def __repr__(self):
        return (
            f"WCS({quoted(self._name)}, "
            + f"{quoted(self._normal_x)}, {quoted(self._normal_y)}, {quoted(self._normal_z)}, "
            + f"{quoted(self._origin_x)}, {quoted(self._origin_y)}, {quoted(self._origin_z)}, "
            + f"{quoted(self._uVector_x)}, {quoted(self._uVector_y)}, {quoted(self._uVector_z)})"
        )

    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    def store(self, modeler: "interface.Model3D") -> "WCS":
        """存储坐标系。

        存储坐标系前务必先将其设为当前坐标系。

        Args:
            modeler (interface.Model3D): 当前建模环境

        Returns:
            WCS: self
        """
        modeler.add_to_history(
            f"store wcs: {self._name}", f'WCS.Store "{self._name}"'
        )
        return self

    def rename(self, n: str) -> "WCS":
        """重命名

        Args:
            n (str): 新的名字

        Returns:
            WCS: self
        """
        self._name = n
        return self

    def set_to_current(self, modeler: "interface.Model3D") -> "WCS":
        """设为当前工作坐标系。

        Args:
            modeler (interface.Model3D): 当前建模环境

        Returns:
            WCS: self
        """
        sCommand = [
            "With WCS",
            f'.SetNormal "{self.normal_x}", "{self.normal_y}", "{self.normal_z}"',
            f'.SetOrigin "{self.origin_x}", "{self.origin_y}", "{self.origin_z}"',
            f'.SetUVector "{self.uVector_x}", "{self.uVector_y}", "{self.uVector_z}"',
            "End With",
        ]
        cmd: str = NEW_LINE.join(sCommand)
        modeler.add_to_history(f"set wcs properties: {self.name}", cmd)
        _logger.info("current WCS is set to %s", f"{str(self)}")
        return self


class Pick(BaseObject):
    """Offers a set of tools to find or set specific points, edges or areas.

    Some methods/functions specify the objects that have to be picked by an id
    number. This id number is unique for every object. If not specified
    otherwise, the numbering starts with 0. Please note: If a solid changes such
    that new faces/edges/points are created, the id number might change!

    Some other methods/functions work on existing picks that can be listed by
    the pick lists (Modeling: Picks > Pick Lists   ). In this case, an index is
    passed to the function. This index is 0-based. The first element in the list
    (the pick that was performed the earliest) will be addressed by "0". It is
    also possible to use negative numbers, in that case the list is addressed in
    reverse order: "-1" is the latest picked object (the one with the greatest
    index in the list), "-2" the second to last pick and so on."""

    def __init__(self, vba=None):
        super().__init__(vba=vba)
        return


def pick_face_from_id(
    modeler: "interface.Model3D", shape: Solid, id_: int | str
) -> None:
    """Picks a face of a solid.  The face is specified by the solid that it
    belongs to and an identity number.

    Args:
        modeler (interface.Model3D): 建模环境。
        shape (Solid): 实体对象
        id_ (int | str): 要选取的面的编号。

    Returns:
        None
    """
    sCommand: list[str] = [
        "With Pick",
        f'.PickFaceFromId "{shape.component}:{shape.name}", "{id_}"',
        "End With",
    ]
    modeler.add_to_history("pick face", NEW_LINE.join(sCommand))
    _logger.info("Pick face %d of %s", id_, f"{shape.component}:{shape.name}")
    return


def pick_end_point_from_id(
    modeler: "interface.Model3D", shape: Solid, id_: int
) -> None:
    """Picks the end point of an edge. The edge is specified by the solid that
    it belongs to and an identity number.

    Args:
        modeler (interface.Model3D): 建模环境。
        shape (Solid): 实体对象
        id_ (interface.Model3D): 要选取的面的编号。

    Returns:
        None
    """
    sCommand = [
        "With Pick",
        f'.PickEndpointFromId "{shape.component}:{shape.name}", "{id_}"',
        "End With",
    ]
    modeler.add_to_history(
        f"pick end point {id_} of {shape.component}:{shape.name}",
        NEW_LINE.join(sCommand),
    )
    _logger.info(
        "Pick end point %d of %s", id_, f"{shape.component}:{shape.name}"
    )
    return


def clear_all_picks(modeler: "interface.Model3D") -> None:
    sCommand = [
        "With Pick",
        ".ClearAllPicks",
        "End With",
    ]
    modeler.add_to_history("clear picks", NEW_LINE.join(sCommand))
    _logger.info(OPERATION_SUCCESS, "clear all picks")
    return
