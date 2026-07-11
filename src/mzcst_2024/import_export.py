"""本模块用于导入和导出模型文件，包括二维和三维模型文件。"""


import logging
import typing
from pathlib import PurePath, PurePosixPath

from . import interface
from .common import NEW_LINE, quoted
from .global_ import BaseObject, CSTPath, Parameter

__all__: list[str] = []

_logger = logging.getLogger(__name__)


class ADSComponentExport (BaseObject):
    """The ADSComponentExport Object lets you export a component to a file.

    Attributes:
        name (str): The name of the component.
        path (str | CSTPath): The path of the component.
        type_ (Literal["normal", "mesh"]): The type of the component.
    """

    def __init__(
        self,
        name: str,
    ):
        super().__init__()
        self._name: str = name
        return