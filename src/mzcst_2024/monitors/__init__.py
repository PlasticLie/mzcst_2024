import logging
import typing as t

from .. import interface
from .._global import BaseObject, Parameter
from ..common import NEW_LINE, quoted
from ..shape_operations import Solid

_logger = logging.getLogger(__name__)


class Monitor(BaseObject):
    """Defines 3D or 2D field monitors. Each monitor stores the field values
    either for a specified frequency or for a set of time samples. There are
    different kinds of monitors: magnetic and electric field or energy monitors
    as well as farfield, power flow and current monitors.

    Parameters
    ----------

        FieldType ("Efield")
        Dimension ("Volume")
        PlaneNormal ("x")
        PlanePosition (0.0)
        Domain ("frequency")
        SamplingStrategy ("Linear")
        Tstart (0.0)
        Tstep (0.0)
        Tend (0.0)
        RepetitionPeriod (0.0)
        UseTend (False)
        TimeAverage (False)
        MaxOrder (1)
        FrequencySamples (1)
        SampleStep (1)
        AutomaticOrder (True)
        TransientFarfield (False)
        UseSubvolume (False)
        ExportFarfieldSource (False)
        EnableNearfieldCalculation (True)
        SetSubVolumeSampling("", "", "")
    """

    def __init__(
        self,
        field_type: t.Literal[
            "Efield",
            "Hfield",
            "Powerflow",
            "Current",
            "Powerloss",
            "Eenergy",
            "Henergy",
            "Farfield",
            "Fieldsource",
            "Spacecharge",
            "Particlecurrentdensity",
        ],
        dimention: t.Literal["plane", "volume"],
        plane_normal: t.Literal["x", "y", "z"] = "x",
        *,
        properties: dict[str, str] = None,
    ):
        super().__init__()
        self._label = field_type
        
        self._attributes = properties
        self._history_title = f"define monitor: {self._number}"
        return

    def create_from_attributes(self, modeler: "interface.Model3D") -> "Solid":
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
                "With Monitor",
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
