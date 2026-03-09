"""Classes for construction faces."""

import enum
import logging
import typing

from . import interface
from .common import NEW_LINE
from .global_ import BaseObject, ParameterLike

_logger = logging.getLogger(__name__)


class Face(BaseObject):
    """Defines a Face object"""

    def __init__(
        self,
        name: str,
        curve_name: str,
        offset: ParameterLike,
        taper_angle: ParameterLike,
        thickness: ParameterLike,
        twist_angle: ParameterLike,
        type_: typing.Literal["PickFace", "ExtrudeCurve", "CoverCurve"],
    ):
        super().__init__()
        self._name = name
        self._curve_name = curve_name
        self._offset = str(offset)
        self._taper_angle = str(taper_angle)
        self._thickness = str(thickness)
        self._twist_angle = str(twist_angle)
        self._type = type_
        return

    def create(self, modeler: "interface.Model3D") -> "Face":
        """Creates the face in the modeler."""
        scmd = [
            "With Face",
            ".Reset",
            f'.Name "{self._name}"',
            f'.Curve "{self._curve_name}"',
            f".Offset {self._offset}",
            f".TaperAngle {self._taper_angle}",
            f".Thickness {self._thickness}",
            f".TwistAngle {self._twist_angle}",
            f'.Type "{self._type}"',
            ".Create",
            "End With",
        ]
        cmd = NEW_LINE.join(scmd)
        self._history.append(f'create face "{self._name}"')
        modeler.add_to_history(self._history[-1], cmd)
        _logger.info(self._history[-1])
        return self
