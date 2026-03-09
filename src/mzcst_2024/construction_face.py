"""Classes for construction faces."""

import enum
import logging
import typing

from . import interface
from .common import NEW_LINE
from .global_ import BaseObject, ParameterLike


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
