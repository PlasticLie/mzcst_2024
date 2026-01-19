"""定义 `Group` 类和与其相关的方法。
"""

import logging
import typing

from . import interface
from .common import NEW_LINE, quoted
from .global_ import BaseObject, Parameter

__all__: list[str] = []

_logger = logging.getLogger(__name__)


class Group(BaseObject):
    """The Group Object lets you define or change the groups. Solids can be
    assigned to groups in order to facilitate changing the properties of
    multiple solids.
    """

    def __init__(self, name: str, vba=None):
        super().__init__(vba=vba)
        self._name = name
        return

    @property
    def name(self) -> str:
        return self._name
