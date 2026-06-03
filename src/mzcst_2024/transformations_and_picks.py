import enum
import logging
import typing

from . import interface
from .common import NEW_LINE, OPERATION_FAILED, OPERATION_SUCCESS, quoted
from .global_ import BaseObject, Parameter
from .shape_operations import Solid

__all__: list[str] = []

_logger = logging.getLogger(__name__)


class Align(BaseObject):
    """Offers a set of tools to align solids to other solids or to the working
    coordinate system."""

    def __init__(self, vba=None):
        super().__init__(vba=vba)
        return


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
            f"{self.__class__.__name__}({quoted(self._name)}, "
            + f"{quoted(self._normal_x)}, {quoted(self._normal_y)}, {quoted(self._normal_z)}, "
            + f"{quoted(self._origin_x)}, {quoted(self._origin_y)}, {quoted(self._origin_z)}, "
            + f"{quoted(self._uVector_x)}, {quoted(self._uVector_y)}, {quoted(self._uVector_z)})"
        )

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


_transform_origin_type = typing.Literal["ShapeCenter", "CommonCenter", "Free"]
_transform_object_type = typing.Literal[
    "Anchorpoint",
    "Coil",
    "Currentdistribution",
    "CurrentMonitor",
    "CurrentWire",
    "Face",
    "FFS",
    "HF3DMonitor",
    "Mixed",
    "Port",
    "Probe",
    "Shape",
    "VoltageMonitor",
    "VoltageWire",
    "Voxeldata",
]
_transform_method_type = typing.Literal[
    "Translate",
    "Rotate",
    "Scale",
    "Mirror",
    "Matrix",
    "GlobalToLocal",
    "LocalToGlobal",
]


class BaseTransform(BaseObject):
    """Offers a set of tools that change a solid by transformations."""

    def __init__(self):
        super().__init__()
        self._use_picked_points: bool = False
        self._invert_picked_points: bool = False
        self._multiple_objects: bool = False
        self._group_objects: bool = False
        self._origin: _transform_origin_type = "ShapeCenter"
        self._multiple_selection: bool = False
        self._repetitions: int = 1
        self._touch: bool = False
        self._touch_tolerance: str = "1e-6"
        self._touch_max_iterations: int = 500
        self._touch_heuristic: bool = True
        self._touch_offset: str = "0.0"
        self._what: _transform_object_type = "Shape"
        self._how: _transform_method_type = "Translate"
        return


class Translate(BaseTransform):
    """Moves the object along a given vector.

    Attributes:
        name (str): Name of the transformation.
        vector (list[str]): The translation vector. The three components of the vector have to be given as strings, e.g. ["10", "0", "5"].
        use_picked_points (bool): Whether to use picked points for the translation.
        invert_picked_points (bool): Whether to invert the picked points for the translation.
        multiple_objects (bool): Whether to apply the transformation to multiple objects.
        group_objects (bool): Whether to group the objects after transformation.
        repetitions (int): Number of repetitions of the transformation.
        multiple_selection (bool): Whether to allow multiple selection of objects for the transformation.
        auto_destination (bool): Whether to automatically determine the destination of the transformation.
        what (_transform_object_type): The type of object to be transformed, e.g. "Shape", "Face", etc.
    """

    def __init__(
        self,
        name: str,
        vector: list[str] | None = None,
        use_picked_points: bool = False,
        invert_picked_points: bool = False,
        multiple_objects: bool = False,
        group_objects: bool = False,
        repetitions: int = 1,
        multiple_selection: bool = False,
        auto_destination: bool = True,
        what: _transform_object_type = "Shape",
    ):
        super().__init__()
        self._name: str = name
        self._vector: list[str] = ["0", "0", "0"] if vector is None else vector
        self._use_picked_points: bool = use_picked_points
        self._invert_picked_points: bool = invert_picked_points
        self._multiple_objects: bool = multiple_objects
        self._group_objects: bool = group_objects
        self._repetitions: int = repetitions
        self._multiple_selection: bool = multiple_selection
        self._auto_destination: bool = auto_destination
        self._what: _transform_object_type = what
        self._how: _transform_method_type = "Translate"
        return

    def create(self, modeler: "interface.Model3D") -> "Translate":
        """Creates the transformation.

        Args:
            modeler (interface.Model3D): 当前建模环境

        Returns:
            Translate: self
        """
        sCommand = [
            "With Translate",
            f'    .Name "{self._name}"',
            f'    .Vector "{self._vector[0]}", "{self._vector[1]}", "{self._vector[2]}"',
            f'    .UsePickedPoints "{self._use_picked_points}"',
            f'    .InvertPickedPoints "{self._invert_picked_points}"',
            f'    .MultipleObjects "{self._multiple_objects}"',
            f'    .GroupObjects "{self._group_objects}"',
            f'    .Repetitions "{self._repetitions}"',
            f'    .MultipleSelection "{self._multiple_selection}"',
            f'    .AutoDestination "{self._auto_destination}"',
            f'    .Transform "{self._what}", "{self._how}" ',
            "End With",
        ]
        modeler.add_to_history(
            f"translate: {self._name}", NEW_LINE.join(sCommand)
        )
        _logger.info("Created translate transformation %s", self._name)
        return self


class Rotate(BaseTransform):
    """Rotates the object around one main axis, given the angle and an offset for the rotation axis (origin).

    Attributes
    ----------
    name : str
        Name of the object to be rotated.
    origin : _transform_origin_type, optional
        For scale, rotate and mirror transformations, this method defines,
        whether the origin for the transformation should be the shape center,
        the center of all named shapes (see .AddName), or a free point defined
        by the `.Center` method. by default `"ShapeCenter"`
    center : list[str] | None, optional
        Sets the center for scale, rotate and mirror transformations. The
        working coordinate system will be used, if activated. Only applicable,
        if `.Origin` is set to `"free"`. by default `None`
    angle : list[str] | None, optional
        Sets the rotation angles around the x, y, and z axes, given as a list of
        three strings, e.g. `["90", "0", "0"]`. by default `None`
    multiple_objects : bool, optional
        If switch is True, the new solid will be copied and the original will
        remain untouched. Else (`copy = False`), the original object will be
        deleted. In case of repeated execution by usage of the `.Repetitions`
        method, `copy = True` will result in number new objects plus the
        original object. by default `False`
    group_objects : bool, optional
        If new objects are created during the transformation (`.MultipleObjects`
        enabled), `unite = True` defines that every new object will be a united
        with the original object after the transformation. If `unite = False`
        all new objects will stay separately. by default `False`
    repetitions : int, optional
        Defines the number of repetitions, the transformation will be applied to
        the selected object. by default `1`
    multiple_selection : bool, optional
        This setting specifies whether the transformation should be performed
        only to one solid or to multiple selected objects. If you transform
        multiple objects history entries are created for every shape and if you
        transform by selected points the pick-points will be deleted after an
        operation. This flag prevents the pickpoints from being deleted. If
        there are still solids to transform the flag is 'true' and in the last
        transform block it is 'false' so the pick-points will be deleted.
        by default `False`
    auto_destination : bool, optional
        **Note:** This attribute is not listed in the documentation. This 
        setting specifies whether the transformation should be automatically 
        applied to the destination object. by default `True`
    what : _transform_object_type, optional
        This execute a specified transform onto the given type of objects (named
        via Name and AddName). Note that not all transformations are applicable
        to all types of objects. by default `"Shape"`
    """

    def __init__(
        self,
        name: str,
        origin: _transform_origin_type = "ShapeCenter",
        center: list[str] | None = None,
        angle: list[str] | None = None,
        multiple_objects: bool = False,
        group_objects: bool = False,
        repetitions: int = 1,
        multiple_selection: bool = False,
        auto_destination: bool = True,
        what: _transform_object_type = "Shape",
    ):

        super().__init__()
        self._name: str = name
        self._origin: _transform_origin_type = origin
        self._center: list[str] = ["0", "0", "0"] if center is None else center
        self._angle: list[str] = ["0", "0", "0"] if angle is None else angle
        self._multiple_objects: bool = multiple_objects
        self._group_objects: bool = group_objects
        self._repetitions: int = repetitions
        self._multiple_selection: bool = multiple_selection
        self._auto_destination: bool = auto_destination
        self._what: _transform_object_type = what
        self._how: _transform_method_type = "Rotate"
        return

    def create(self, modeler: "interface.Model3D") -> "Rotate":
        """Creates the transformation.

        Args:
            modeler (interface.Model3D): 当前建模环境

        Returns:
            Rotate: self
        """
        sCommand = [
            "With Rotate",
            f'    .Name "{self._name}"',
            f'    .Origin "{self._origin}"',
            f'    .Center "{self._center[0]}", "{self._center[1]}", "{self._center[2]}"',
            f'    .Angle "{self._angle[0]}", "{self._angle[1]}", "{self._angle[2]}"',
            f'    .MultipleObjects "{self._multiple_objects}"',
            f'    .GroupObjects "{self._group_objects}"',
            f'    .Repetitions "{self._repetitions}"',
            f'    .MultipleSelection "{self._multiple_selection}"',
            f'    .AutoDestination "{self._auto_destination}"',
            f'    .Transform "{self._what}", "{self._how}" ',
            "End With",
        ]
        modeler.add_to_history(f"rotate: {self._name}", NEW_LINE.join(sCommand))
        _logger.info("Created rotate transformation %s", self._name)
        return self


class Scale(BaseTransform):
    """scales the object. The scaling center can be specified as well. For some
    types, only uniform scaling is allowed."""


class Mirror(BaseTransform):
    """mirrors the object on a mirror plane whose normal and offset is given"""


class Matrix(BaseTransform):
    """this applies a general matrix transformation onto a given object. Input
    is a 3 by 3 Matrix and an additional translation vector."""


class LocalToGlobal(BaseTransform):
    """After this transform that consists of translates and rotates internally,
    the position and orientation of the object  in regard to the global
    coordinate system will match its position and rotation that it had to the
    local coordinate system before."""


class GlobalToLocal(BaseTransform):
    """This is the inverse operation to the one above. An object aligned to the
    x-y plane in the origin of the global coordinate system will afterwards be
    aligned to the u-v plane and translated to be in the origin of the local
    coordinate system."""
