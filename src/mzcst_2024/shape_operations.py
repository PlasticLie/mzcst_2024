import copy
import enum
import logging
import typing

from . import interface
from ._global import BaseObject, Parameter
from .common import NEW_LINE, OPERATION_FAILED, OPERATION_SUCCESS, quoted
from .component import Component
from .material import Material

_logger = logging.getLogger(__name__)


class Solid(BaseObject):
    """CST所有模型实体的抽象基类。

    Attributes:
        name (str): 实体名称。
        component (str | Component): 实体所在的部件（component）名称。
        material (str | Material): 实体的材料名称。
        vba (list[str], Optional): （可选）构造实体需要的vba代码。
    """

    def __init__(
        self,
        name: str,
        component: str | Component = "",
        material: str | Material = "Vacuum",
        *,
        properties: dict[str, str] = None,
        vba: list[str] = None,
    ) -> None:
        super().__init__(vba=vba)
        self._name: str = name
        self._component: str = str(component)
        self._properties: dict[str, str] = properties

        self._material: str = ""
        if isinstance(material, str):
            self._material = material
        elif isinstance(material, Material):
            self._material = material.name
        self._history: list[str] = [
            f"define solid: {self.component}:{self.name}"
        ]
        self._history_title = f"define solid: {self.full_name}"
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

    @property
    def history(self) -> list[str]:
        return self._history

    @property
    def full_name(self) -> str:
        """返回实体的全名

        Returns:
            str: 实体的全名，形式为`component:name`
        """
        return f"{self.component}:{self.name}"

    def create(
        self, modeler: interface.Model3D  # pylint: disable=unused-argument
    ) -> "Solid":
        """用于给子类定义create函数。"""
        return self

    def create_from_attributes(self, modeler: "interface.Model3D") -> "Solid":
        """从属性字典新建实体。

        Args:
            modeler (interface.Model3D): 建模环境。

        Returns:
            self (Solid): self。
        """
        if not self._properties:
            _logger.error("No valid properties.")
        else:
            scmd1 = [
                "With Extrude",
                ".Reset",
                f'.Name "{self._name}"',
                f'.Component "{self._component}"',
                f'.Material "{self._material}"',
            ]
            cmd1 = NEW_LINE.join(scmd1)
            scmd2 = []
            for k, v in self._properties.items():
                scmd2.append("." + k + " " + v)
            cmd2 = NEW_LINE.join(scmd2)
            scmd3 = [
                ".Create",
                "End With",
            ]
            cmd3 = NEW_LINE.join(scmd3)
            cmd = NEW_LINE.join((cmd1, cmd2, cmd3))
            modeler.add_to_history(self._history_title, cmd)
        return self

    def add(self, modeler: "interface.Model3D", other: "Solid") -> "Solid":
        """This method adds two solids. The added solid will be stored under `solid1` and the second solid will be deleted.

        `Add ( solidname solid1, solidname solid2 )`


        Args:
            modeler (interface.Model3D): 建模环境。
            other (Solid): 另一个实体。

        Returns:
            self: 对象自身的引用。
        """
        title = f"boolean add shapes: {self.component}:{self.name}, {other.component}:{other.name}"
        cmd = f'Solid.Add "{self.component}:{self.name}", "{other.component}:{other.name}"'
        modeler.add_to_history(title, cmd)
        self._history += [title]
        _logger.info(OPERATION_SUCCESS, title)
        return self

    def insert(self, modeler: "interface.Model3D", other: "Solid") -> "Solid":
        """Performs an subtraction between the solids `solid1` and `solid2` (`solid1 - solid2`) but does not delete solid2.

        `Insert ( solidname solid1, solidname solid2 )`

        Args:
            modeler (interface.Model3D): 建模环境。
            other (Solid): 另一个实体。

        Returns:
            self: 对象自身的引用。
        """
        title = f"boolean insert shapes: {self.component}:{self.name}, {other.component}:{other.name}"
        cmd = f'Solid.Insert "{self.component}:{self.name}", "{other.component}:{other.name}"'
        modeler.add_to_history(title, cmd)
        self._history += [title]
        _logger.info(OPERATION_SUCCESS, title)
        return self

    def intersect(
        self, modeler: "interface.Model3D", other: "Solid"
    ) -> "Solid":
        """Performs an intersection on the two solids. The overlapping parts between the two solids remains while the rest will be deleted. The result will be stored in `solid1` while `solid2` will be deleted.

        `Intersect ( solidname solid1, solidname solid2 )`

        Args:
            modeler (interface.Model3D): 建模环境。
            other (Solid): 另一个实体。

        Returns:
            self: 对象自身的引用。
        """
        title = f"boolean intersect shapes: {self.component}:{self.name}, {other.component}:{other.name}"
        cmd = f'Solid.Intersect "{self.component}:{self.name}", "{other.component}:{other.name}"'
        modeler.add_to_history(title, cmd)
        self._history += [title]
        _logger.info(OPERATION_SUCCESS, title)
        return self

    def subtract(self, modeler: "interface.Model3D", other: "Solid") -> "Solid":
        """Performs the operation `solid1 - solid2`. The result will be stored in solid1 while solid2 will be deleted.

        Args:
            modeler (interface.Model3D): 建模环境。
            other (Solid): 另一个实体。

        Returns:
            self: 对象自身的引用。
        """
        title = f"boolean subtract shapes: {self.component}:{self.name}, {other.component}:{other.name}"
        cmd = f'Solid.Subtract "{self.component}:{self.name}", "{other.component}:{other.name}"'
        modeler.add_to_history(title, cmd)
        self._history += [title]
        _logger.info(OPERATION_SUCCESS, title)
        return self

    def merge_materials_of_component(
        self, modeler: "interface.Model3D", name: "Solid"
    ) -> "Solid":
        """This method has not been used in scripts, BE CAREFULL.\n

        The parameter `name` can be a `componentname` or a `solidname`.

        If it is a `componentname` the function will merge all shapes from one component with the same material like the boolean operation add.

        If `name` is a `solidname` all shapes of a component with the same material like the solid `name` will be merged together. The resulting shape is called like `name`.

        Args:
            modeler (interface.Model3D): 建模环境。
            other (Solid): 另一个实体。

        Returns:
            self: 对象自身的引用。
        """
        title = f"merge_materials_of_component: {name}"
        cmd = f'Solid.MergeMaterialsOfComponent "{name}"'
        modeler.add_to_history(title, cmd)
        self._history += [title]
        _logger.info(OPERATION_SUCCESS, title)
        return self


def solid_add(modeler: "interface.Model3D", s1: Solid, s2: Solid) -> None:
    title = f"boolean add shapes: {s1.component}:{s1.name}, {s2.component}:{s2.name}"
    cmd = f'Solid.Add "{s1.component}:{s1.name}", "{s2.component}:{s2.name}"'
    modeler.add_to_history(
        title,
        cmd,
    )
    return


class Shell_key(enum.Enum):
    """The parameter key may have one of the following values:

    Attributes:
        Inside (int): The wall will be created from the original solids surface
        to its inside.
        Outside (int): The wall will be created from the original solids surface
        to its outside.
        Centered (int): The wall will be created around the original solids
        surface.


    """

    Inside = enum.auto()
    Outside = enum.auto()
    Centered = enum.auto()


def advanced_shell(
    modeler: "interface.Model3D",
    solid: Solid,
    key: str,
    thickness: Parameter | float | int,
    # clearpicks: bool = False,
) -> None:
    """这个方法在CST官方帮助里找不到，只有一个与之很接近的`ShellAdvanced`，两者用法很
    接近，除了本方法没有最后的`clearpicks`参数。但还是抄录官方的`ShellAdvanced`帮助如
    下。

    This method hollows out the existing solid. The original solid is
    transformed to a new solid that is made out of the surface of the old one
    with a defined thickness.

    The parameter `clearpicks` indicates if the actual picks are deleted after
    the operation. This is needed for multiple solid operation, because several
    entries are written into the history and only the last one should delete the
    picks. So all `clearpicks` values in the history entries of the multiple
    solid operation should be `false` and the last one should be `true`.

    Args:
        modeler (interface.Model3D): 建模环境。
        solid (Solid): 实体对象。
        key (Shell_key): 造壳方向（可选：`"Inside"`、`"Outside"`、`"Centered"`）。
        thickness (Parameter | float): 壳的厚度。
        clearpicks (bool): 选择的实体在造壳后是否删除。

    Returns:
        None
    """
    if isinstance(thickness, float | int):
        t = Parameter(thickness)
    else:
        t = thickness
    sCommand = [
        "With Solid",
        f'.AdvancedShell  "{solid.component}:{solid.name}", "{key}", "{t.name}"',
        "End With",
    ]
    modeler.add_to_history(
        f"shell object: {solid.component}:{solid.name}",
        NEW_LINE.join(sCommand),
    )
    _logger.info("shell object: %s", f"{solid.component}:{solid.name}")
    return


def thicken_sheet_advanced(
    modeler: "interface.Model3D",
    solid: Solid,
    key: typing.Literal["Inside", "Outside", "Centered"],
    thickness: Parameter | float | int,
    clear_picks: bool = False,
) -> None:
    """This method thickens an existing sheet body with the given thickness
    thickness. Thus, the original sheet body is transformed to a solid body.

    The parameter clearpicks indicates if the actual picks are deleted after the
    operation. This is needed for multiple solid operation, because several
    entries are written into the history and only the last one should delete the
    picks. So all clearpicks values in the history entries of the multiple solid
    operation should be false and the last one should be true.

    Args:
        modeler (interface.Model3D): 建模环境。
        solid (Solid): 实体对象。
        key (Shell_key): 造壳方向（可选：`"Inside"`、`"Outside"`、`"Centered"`）。
        thickness (Parameter | float): 壳的厚度。
        clear_picks (bool): 选择的实体在造壳后是否删除。

    Returns:
        None:
    """
    if isinstance(thickness, float | int):
        t = Parameter(thickness)
    else:
        t = thickness
    sCommand = [
        "With Solid",
        f'.ThickenSheetAdvanced "{solid.component}:{solid.name}", "{key}", "{t.name}", {clear_picks}',
        "End With",
    ]
    modeler.add_to_history(
        f"thicken sheet: {solid.component}:{solid.name}",
        NEW_LINE.join(sCommand),
    )
    _logger.info("thicken sheet: %s", f"{solid.component}:{solid.name}")
    return


class _BaseBend(BaseObject):
    def __init__(self, vba=None):
        super().__init__(vba=vba)
        self._param_sweep_and_optimizer_checks_result = False
        return


class BendShape(_BaseBend):
    def __init__(self, sheet: Solid, solid: Solid, faces: str, vba=None):
        super().__init__(vba)
        self._sheet: Solid = sheet
        self._solid: Solid = solid
        self._faces: str = faces
        return

    @property
    def sheet(self) -> str:
        return self._sheet.full_name

    @property
    def solid(self) -> str:
        return self._solid.full_name

    @property
    def faces(self) -> str:
        return self._faces

    def define(self, modeler: "interface.Model3D") -> "BendShape":
        """定义弯曲。

        Args:
            modeler (interface.Model3D): 建模环境。

        Returns:
            self: 对象自身的引用。

        """
        title = f'bend: selected sheets, {self.solid}"'
        sCommand = [
            "With Bending ",
            ".Reset ",
            '.Version "10" ',
            f'.Sheet "{self.sheet}" ',
            f'.Solid "{self.solid}" ',
            f'.Faces "{self.faces}" ',
            ".Bend ",
            "End With",
        ]
        cmd = NEW_LINE.join(sCommand)

        modeler.add_to_history(title, cmd)
        _logger.info("Bend sheet: %s to %s", self.sheet, self.solid)
        return self
