"""定义绘图有关的类和与其相关的方法。
"""
import logging

from . import interface
from ._global import BaseObject, Parameter
from .common import NEW_LINE, quoted
from .shape_operations import Solid

_logger = logging.getLogger(__name__)


class Plot(BaseObject):
    """Controls the output of the main plot window.

    Default Settings::
        CutPlaneRatio (0.5)
        DrawBox (False)
        InnerSurfaces (True)
        RotationAngle (10.0)
        ShowCutPlane (False)
        SurfaceMesh (False)
        WireFrame (False)
    """

    def __init__(self, *, attributes=None, vba=None):
        super().__init__(attributes=attributes, vba=vba)
        return

    @staticmethod
    def reset_view(modeler: interface.Model3D) -> None:
        reset_view = [
            "With Plot",
            ".DrawBox True",
            '.DrawWorkplane "false"',
            '.RestoreView "Perspective"',
            ".ZoomToStructure",
            "End With",
        ]
        modeler.add_to_history("reset view", NEW_LINE.join(reset_view))
        return
    
    def create_from_attributes(self, modeler):
        """从属性列表新建`Plot`对象。

        Args:
            modeler (interface.Model3D): 建模环境。

        Returns:
            self (BaseObject): self
        """
        if not self._attributes:
            _logger.error("No valid properties.")
        else:
            scmd1 = [
                "With Plot ",
            ]
            cmd1 = NEW_LINE.join(scmd1)
            scmd2 = []
            for k, v in self._attributes.items():
                scmd2.append(f".{k} {v}")
            cmd2 = NEW_LINE.join(scmd2)
            scmd3 = [
                "End With",
            ]
            cmd3 = NEW_LINE.join(scmd3)
            cmd = NEW_LINE.join((cmd1, cmd2, cmd3))
            modeler.add_to_history(self._history_title, cmd)
        return self


class Plot1D(BaseObject):
    def __init__(self, *, attributes=None, vba=None):
        super().__init__(attributes=attributes, vba=vba)
        return


class Plot2D3D(BaseObject):
    def __init__(self, *, attributes=None, vba=None):
        super().__init__(attributes=attributes, vba=vba)
        return


class ScalarPlot2D(BaseObject):
    def __init__(self, *, attributes=None, vba=None):
        super().__init__(attributes=attributes, vba=vba)
        return


class VectorPlot2D(BaseObject):
    def __init__(self, *, attributes=None, vba=None):
        super().__init__(attributes=attributes, vba=vba)
        return


class ScalarPlot3D(BaseObject):
    def __init__(self, *, attributes=None, vba=None):
        super().__init__(attributes=attributes, vba=vba)
        return


class VectorPlot3D(BaseObject):
    def __init__(self, *, attributes=None, vba=None):
        super().__init__(attributes=attributes, vba=vba)
        return


class ColourMapPlot(BaseObject):
    def __init__(self, *, attributes=None, vba=None):
        super().__init__(attributes=attributes, vba=vba)
        return


class FarfieldPlot(BaseObject):
    def __init__(self, *, attributes=None, vba=None):
        super().__init__(attributes=attributes, vba=vba)
        return
