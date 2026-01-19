import logging

from .. import interface
from ..common import NEW_LINE, quoted
from ..global_ import BaseObject, Parameter
from ..shape_operations import Solid

_logger = logging.getLogger(__name__)


class Port(BaseObject):
    """Defines a waveguide port object. Waveguide ports are used to feed the
    calculation domain with power and to absorb the returning power. For each
    waveguide port, time signals and S-Parameters will be recorded during a
    solver run. In practice the port can be substituted by a longitudinal
    homogeneous waveguide connected to the structure. You will need at least
    one port (either waveguide port or discrete port) or a plane wave excitation
    source to feed the structure, before starting a solver run.

    Default Settings::

        Label ("")
        NumberOfModes (1)
        AdjustPolarization (False)
        PolarizationAngle (0.0)
        ReferencePlaneDistance (0.0)
        TextSize (50)
        Coordinates ("Free")
        Orientation ("zmin")
        PortOnBound (True)
        ClipPickedPortToBound (False)
        Xrange (0.0, 0.0)
        Yrange (0.0, 0.0)
        Zrange (0.0, 0.0)
    """

    def __init__(
        self, label: str, number: int, *, properties: dict[str, str] = None
    ):
        super().__init__()
        self._label = label
        self._number = number
        self._attributes = properties
        self._history_title = f"define port: {self._number}"
        return

    def create_from_attributes(self, modeler: "interface.Model3D") -> "Port":
        """从属性字典新建端口。

        Args:
            modeler (interface.Model3D): 建模环境。

        Returns:
            self (Solid): self。
        """
        if not self._attributes:
            _logger.error("No valid properties.")
        else:
            scmd1 = [
                "With Port",
                ".Reset",
                f'.Label "{self._label}"',
                f'.PortNumber  "{self._number}"',
            ]
            cmd1 = NEW_LINE.join(scmd1)
            scmd2 = []
            for k, v in self._attributes.items():
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
