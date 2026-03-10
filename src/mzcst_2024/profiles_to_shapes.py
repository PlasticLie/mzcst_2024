import ast
import logging
import typing

from . import interface
from .common import NEW_LINE, OPERATION_FAILED, OPERATION_SUCCESS, quoted
from .shape_operations import Solid

_logger = logging.getLogger(__name__)


class Extrude(Solid):
    def __init__(
        self,
        name: str,
        component: str = "",
        material: str = "Vacuum",
        *,
        properties: dict[str, str] = None,
    ):
        super().__init__(name, component, material, properties=properties)

    def create(self, modeler: "interface.Model3D") -> "Extrude":
        """从属性列表新建挤压实体。

        Args:
            modeler (interface.Model3D): 建模环境。

        Returns:
            self (Extrude): self。
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
            self._history.append(f"define extrude: {self._component}:{self._name}")
            modeler.add_to_history(self._history[-1], cmd)
        return self


class Rotate(Solid):
    """Creates a three dimensional solid by rotating  a Profile or a selected face."""

    def __init__(
        self,
        name: str,
        component: str = "",
        material: str = "Vacuum",
        *,
        properties: dict[str, str] = None,
    ):
        super().__init__(name, component, material, properties=properties)
        return

    def create(self, modeler: "interface.Model3D") -> "Rotate":
        """从属性列表新建旋转实体。

        Args:
            modeler (interface.Model3D): 建模环境。

        Returns:
            self (Rotate): self。
        """
        if not self._properties:
            _logger.error("No valid properties.")
        else:
            scmd1 = [
                "With Rotate",
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
            self._history.append(f"define rotate: {self._component}:{self._name}")
            modeler.add_to_history(self._history[-1], cmd)
        return self


class Loft(Solid):
    """Creates a solid that connects two surfaces."""
    def __init__(
        self,
        name: str,
        component: str = "",
        material: str = "Vacuum",
        *,
        properties: dict[str, str] = None,
    ):
        super().__init__(name, component, material, properties=properties)
        
        return

    def create(self, modeler: "interface.Model3D") -> "Loft":
        """从属性列表新建放样实体。

        Args:
            modeler (interface.Model3D): 建模环境。

        Returns:
            self (Loft): self。
        """
        if not self._properties:
            _logger.error("No valid properties.")
        else:
            scmd1 = [
                "With Loft",
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
            self._history.append(f"define loft: {self._component}:{self._name}")
            modeler.add_to_history(self._history[-1], cmd)
        return self

class TraceFromCurve(Solid):
    """This object is used to create a new shape from a curve item. You can cover a previously defined curve item (closed or open) with arbitrary thickness and width. After that operation the curve item will not exist any longer."""

    def __init__(
        self,
        name: str,
        component: str = "",
        material: str = "Vacuum",
        *,
        properties: dict[str, str] = None,
    ):
        super().__init__(name, component, material, properties=properties)
        return

    def create(self, modeler: "interface.Model3D") -> "TraceFromCurve":
        """从属性列表新建曲线挤压实体。

        Args:
            modeler (interface.Model3D): 建模环境。

        Returns:
            self (TraceFromCurve): self。
        """
        if not self._properties:
            _logger.error("No valid properties.")
        else:
            scmd1 = [
                "With TraceFromCurve",
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
            self._history.append(f"define trace from curve: {self._component}:{self._name}")
            modeler.add_to_history(self._history[-1], cmd)
        return self