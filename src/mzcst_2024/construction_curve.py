"""Classes for construction curves."""

import logging
import typing

from . import interface
from .common import NEW_LINE
from .global_ import BaseObject, ParameterLike

_logger = logging.getLogger(__name__)


class Curve(BaseObject):
    """This object is used to apply operations on curves and curve items."""

    def __init__(
        self,
        name: str,
    ):
        super().__init__()
        self._name: str = name
        return

    @property
    def name(self) -> str:
        return self._name

    def create(self, modeler: interface.Model3D) -> "Curve":
        """Creates a new curve with the given name.

        Args:
            modeler (interface.Model3D): The modeler interface used to interact with the 3D model.

        Returns:
            Curve: The created Curve object.
        """
        cmd = f'Curve.NewCurve "{self._name}"'
        self._history.append(f'create curve "{self._name}"')
        modeler.add_to_history(self._history[-1], cmd)
        _logger.info(self._history[-1])
        return self

    def rename(self, modeler: interface.Model3D, new_name: str) -> "Curve":
        """Changes the name of an existing curve.

        Args:
            modeler (interface.Model3D): The modeler interface used to interact with the 3D model.
            new_name (str): The new name of the curve.

        Returns:
            The Curve object itself.
        """
        self._history.append(f'rename curve "{self._name}" to "{new_name}"')
        _logger.info(self._history[-1])
        cmd = f'Curve.RenameCurve "{self._name}", "{new_name}"'
        modeler.add_to_history(self._history[-1], cmd)
        self._name = new_name
        return self

    def delete(self, modeler: interface.Model3D) -> "Curve":
        """Deletes an existing curve.

        Args:
            modeler (interface.Model3D): The modeler interface used to interact with the 3D model.

        Returns:
            The Curve object itself.
        """
        self._history.append(f'delete curve "{self._name}"')
        _logger.info(self._history[-1])
        cmd = f'Curve.DeleteCurve "{self._name}"'
        modeler.add_to_history(self._history[-1], cmd)
        return self


class AnalyticalCurve(BaseObject):
    """This object is used to create a new analytical curve item."""

    def __init__(
        self,
        name: str,
        curve_name: str,
        law_x: ParameterLike,
        law_y: ParameterLike,
        law_z: ParameterLike,
        parameter_range: tuple[ParameterLike, ParameterLike],
    ):
        super().__init__()
        self._name: str = name
        self._curve_name: str = curve_name
        self._law_x: str = law_x if isinstance(law_x, str) else str(law_x)
        self._law_y: str = law_y if isinstance(law_y, str) else str(law_y)
        self._law_z: str = law_z if isinstance(law_z, str) else str(law_z)
        self._parameter_range: tuple[str, str] = (
            str(parameter_range[0]),
            str(parameter_range[1]),
        )
        return

    @property
    def name(self) -> str:
        return self._name

    @property
    def curve_name(self) -> str:
        return self._curve_name

    @property
    def parameter_range(self) -> tuple[str, str]:
        return self._parameter_range

    def create(self, modeler: interface.Model3D) -> "AnalyticalCurve":
        """Creates a new analytical curve item with the given properties.

        Args:
            modeler (interface.Model3D): The modeler interface used to interact with the 3D model.

        Returns:
            AnalyticalCurve: The created AnalyticalCurve object.
        """
        scmd = [
            "With AnalyticalCurve",
            ".Reset",
            f'.Name "{self._name}"',
            f'.Curve "{self._curve_name}"',
            f'.LawX "{self._law_x}"',
            f'.LawY "{self._law_y}"',
            f'.LawZ "{self._law_z}"',
            f'.ParameterRange "{self._parameter_range[0]}", "{self._parameter_range[1]}"',
            ".Create",
            "End With",
        ]
        cmd = NEW_LINE.join(scmd)
        self._history.append(f'create analytical curve item "{self._name}"')
        modeler.add_to_history(self._history[-1], cmd)
        _logger.info(self._history[-1])
        return self


class Arc(BaseObject):
    def __init__(
        self,
        name: str,
        curve_name: str,
        orientation: typing.Literal[
            "Clockwise", "CounterClockwise"
        ] = "Clockwise",
        xcenter: ParameterLike = 0,
        ycenter: ParameterLike = 0,
        x1: ParameterLike = 0,
        y1: ParameterLike = 0,
        x2: ParameterLike = 0,
        y2: ParameterLike = 0,
        angle: ParameterLike = 90,
        use_angle: bool = False,
        segments: ParameterLike = 0,
    ):
        super().__init__()
        self._name = name
        self._curve_name = curve_name
        self._orientation = orientation
        self._xcenter = str(xcenter)
        self._ycenter = str(ycenter)
        self._x1 = str(x1)
        self._y1 = str(y1)
        self._x2 = str(x2)
        self._y2 = str(y2)
        self._angle = str(angle)
        self._use_angle = use_angle
        self._segments = (
            segments if isinstance(segments, str) else str(segments)
        )
        return

    def create(self, modeler: interface.Model3D) -> "Arc":
        scmd = [
            "With Arc",
            ".Reset",
            f'.Name "{self._name}"',
            f'.Curve "{self._curve_name}"',
            f'.Orientation "{self._orientation}"',
            f'.XCenter "{self._xcenter}"',
            f'.YCenter "{self._ycenter}"',
            f'.X1 "{self._x1}"',
            f'.Y1 "{self._y1}"',
            f'.X2 "{self._x2}"',
            f'.Y2 "{self._y2}"',
            f'.Angle "{self._angle}"',
            f".UseAngle {self._use_angle}",
            f".Segments {self._segments}",
            ".Create",
            "End With",
        ]
        cmd = NEW_LINE.join(scmd)
        self._history.append(f'create arc item "{self._name}"')
        modeler.add_to_history(self._history[-1], cmd)
        _logger.info(self._history[-1])
        return self
