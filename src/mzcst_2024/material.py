"""定义 `Material` 类和与其相关的方法。"""

import enum
import logging

from . import interface  # type:ignore
from ._global import BaseObject
from .common import NEW_LINE, quoted

__all__: list[str] = []

_logger = logging.getLogger(__name__)


class MaterialType(enum.Enum):
    PEC = enum.auto()
    NORMAL = enum.auto()
    ANISOTROPIC = enum.auto()
    LOSSY_METAL = enum.auto()
    CORRUGATED_WALL = enum.auto()
    OHMIC_SHEET = enum.auto()
    TENSOR_FORMULA = enum.auto()
    NON_LINEAR = enum.auto()


class Material(BaseObject):
    """材料对象

    Attributes:
        name (str): 材料名。
        folder (str): 文件夹。
        properties (dict[str, str]): 材料属性名及对应的值。
        vba (list[str]): 构造材料的完整vba代码。

    Default Settings::

        .Type ("Normal")
        .Colour ("0", "1", "1")
        .Wireframe ("False")
        .Transparency ("0")
        .Epsilon ("1.0")
        .Mu ("1.0")
        .Rho ("0.0")
        .Sigma ("0.0")
        .TanD ("0.0")
        .TanDFreq ("0.0")
        .TanDGiven ("False")
        .TanDModel ("ConstTanD")
        .SigmaM ("0.0")
        .TanDM ("0.0")
        .TanDMFreq ("0.0")
        .TanDMGiven ("False")
        .DispModelEps ("None")
        .DispModelMu ("None")
        .MuInfinity ("1.0")
        .EpsInfinity ("1.0")
        .DispCoeff1Eps ("0.0")
        .DispCoeff2Eps ("0.0")
        .DispCoeff3Eps ("0.0")
        .DispCoeff4Eps ("0.0")
        .DispCoeff1Mu ("0.0")
        .DispCoeff2Mu ("0.0")
        .DispCoeff3Mu ("0.0")
        .DispCoeff4Mu ("0.0")
        .AddDispEpsPole1stOrder ("0.0", "0.0")
        .AddDispEpsPole2ndOrder ("0.0", "0.0", "0.0", "0.0")
    """

    def __init__(
        self,
        name: str,
        folder: str = "",
        *,
        properties: dict[str, str] = None,
        vba: list[str] = None,
    ):
        super().__init__(attributes=properties, vba=vba)
        self._name: str = name
        self._folder: str = folder
        # self._properties: dict[str, str] = properties
        self._history_title = f"define material: {self.full_name}"
        return

    @staticmethod
    def new_folder(modeler: "interface.Model3D", folder_name: str) -> None:
        """新建材料文件夹。

        Args:
            modeler (interface.Model3D): 建模环境。
            folder_name (str): 文件夹名。

        Returns:
            None
        """
        sCommand = ["With Material", f'.NewFolder "{folder_name}"', "End With"]
        cmd = NEW_LINE.join(sCommand)
        modeler.add_to_history(f"new folder: {folder_name}", cmd)
        return

    @staticmethod
    def delete_folder(modeler: "interface.Model3D", folder_name: str) -> None:
        """删除材料文件夹。

        Args:
            modeler (interface.Model3D): 建模环境。
            folder_name (str): 文件夹名。

        Returns:
            None
        """
        sCommand = [
            "With Material",
            f'.DeleteFolder "{folder_name}"',
            "End With",
        ]
        cmd = NEW_LINE.join(sCommand)
        modeler.add_to_history(f"delete folder: {folder_name}", cmd)
        return

    @staticmethod
    def rename_folder(
        modeler: "interface.Model3D", old_name: str, new_name: str
    ) -> None:
        """Changes the name of an existing folder.

        Args:
            modeler (interface.Model3D): _description_
            old_name (str): name of existing folder.
            new_name (str): new name of the folder.
        """
        sCommand = [
            "With Material",
            f'.RenameFolder "{old_name}", "{new_name}"',
            "End With",
        ]
        cmd = NEW_LINE.join(sCommand)
        modeler.add_to_history(f"rename folder: {old_name}", cmd)
        return

    @property
    def name(self) -> str:
        return self._name

    @property
    def folder(self) -> str:
        return self._folder

    @property
    def properties(self) -> dict[str, str]:
        return self._attributes

    @property
    def full_name(self) -> str:
        """返回材料的名称和保存文件夹。

        Returns:
            str: _description_
        """
        if self._folder == "":
            return f"{self._name}"
        return f"{self._folder}/{self._name}"

    # @property
    # def is_created(self) -> bool:
    #     return self._is_created

    # @property
    # def vba(self) -> list[str]:
    #     return self._vba

    def __str__(self):
        return self._name

    def delete(self, modeler: "interface.Model3D") -> "Material":
        sCommand = ["With Material", f'.Delete "{self.name}"', "End With"]
        cmd = NEW_LINE.join(sCommand)
        modeler.add_to_history("delete material", cmd)
        return self

    def rename(self, modeler: "interface.Model3D", new_name: str) -> "Material":
        sCommand = [
            "With Material",
            f'.Rename "{self.name}", "{new_name}"',
            "End With",
        ]
        cmd = NEW_LINE.join(sCommand)
        modeler.add_to_history(f"rename material: {new_name}", cmd)
        self._name = new_name
        return self

    def create(self, modeler: "interface.Model3D") -> "Material":
        """从属性列表新建材料。

        Args:
            modeler (interface.Model3D): 建模环境。

        Returns:
            self (Material): 对象自身的引用。
        """
        if not self._attributes:
            _logger.error("No valid properties.")
        else:
            scmd1 = [
                "With Material ",
                ".Reset ",
                f'.Name "{self.name}"',
                f'.Folder "{self.folder}"',
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


# 自带的材料
PEC_: str = "PEC"
VACUUM_: str = "Vaccum"


PEC = Material("PEC")
VACUUM = Material("Vacuum")

# 常用材料
copper_annealed = Material(
    "Copper (annealed)",
    properties={
        "FrqType": ' "all"',
        "Type": ' "Lossy metal"',
        "SetMaterialUnit": ' "GHz", "mm"',
        "Mu": ' "1.0"',
        "Kappa": ' "5.8e+007"',
        "Rho": ' "8930.0"',
        "ThermalType": ' "Normal"',
        "ThermalConductivity": ' "401.0"',
        "SpecificHeat": ' "390", "J/K/kg"',
        "MetabolicRate": ' "0"',
        "BloodFlow": ' "0"',
        "VoxelConvection": ' "0"',
        "MechanicsType": ' "Isotropic"',
        "YoungsModulus": ' "120"',
        "PoissonsRatio": ' "0.33"',
        "ThermalExpansionRate": ' "17"',
        "Colour": ' "1", "1", "0"',
        "Wireframe": ' "False"',
        "Reflection": ' "False"',
        "Allowoutline": ' "True"',
        "Transparentoutline": ' "False"',
        "Transparency": ' "0"',
    },
)

rogers_RT5880_lossy = Material(
    "Rogers RT5880 (lossy)",
    properties={
        "FrqType": '"all"',
        "Type": '"Normal"',
        "SetMaterialUnit": '"GHz", "mm"',
        "Epsilon": '"2.2"',
        "Mu": '"1.0"',
        "Kappa": '"0.0"',
        "TanD": '"0.0009"',
        "TanDFreq": '"10.0"',
        "TanDGiven": '"True"',
        "TanDModel": '"ConstTanD"',
        "KappaM": '"0.0"',
        "TanDM": '"0.0"',
        "TanDMFreq": ' "0.0"',
        "TanDMGiven": '"False"',
        "TanDMModel": '"ConstKappa"',
        "DispModelEps": '"None"',
        "DispModelMu": '"None"',
        "DispersiveFittingSchemeEps": '"General 1st"',
        "DispersiveFittingSchemeMu": '"General 1st"',
        "UseGeneralDispersionEps": '"False"',
        "UseGeneralDispersionMu": '"False"',
        "Rho": '"0.0"',
        "ThermalType": '"Normal"',
        "ThermalConductivity": '"0.20"',
        "SetActiveMaterial": '"all"',
        "Colour": '"0.94", "0.82", "0.76"',
        "Wireframe": '"False"',
        "Transparency": '"0"',
    },
)


FR4_lossy = Material(
    "FR4 (lossy)",
    properties={
        "FrqType": '"all"',
        "Type": '"Normal"',
        "SetMaterialUnit": '"GHz", "mm"',
        "Epsilon": '"4.3"',
        "Mu": '"1.0"',
        "Kappa": '"0.0"',
        "TanD": '"0.025"',
        "TanDFreq": '"10.0"',
        "TanDGiven": '"True"',
        "TanDModel": '"ConstTanD"',
        "KappaM": '"0.0"',
        "TanDM": '"0.0"',
        "TanDMFreq": '"0.0"',
        "TanDMGiven": '"False"',
        "TanDMModel": '"ConstKappa"',
        "DispModelEps": '"None"',
        "DispModelMu": '"None"',
        "DispersiveFittingSchemeEps": '"General 1st"',
        "DispersiveFittingSchemeMu": '"General 1st"',
        "UseGeneralDispersionEps": '"False"',
        "UseGeneralDispersionMu": '"False"',
        "Rho": '"0.0"',
        "ThermalType": '"Normal"',
        "ThermalConductivity": '"0.3"',
        "SetActiveMaterial": '"all"',
        "Colour": '"0.94", "0.82", "0.76"',
        "Wireframe": '"False"',
        "Transparency": '"0"',
    },
)

F4B_lossy = Material(
    "F4B",
    properties={
        "FrqType": '"all"',
        "Type": '"Normal"',
        "SetMaterialUnit": '"GHz", "mm"',
        "Epsilon": '"2.65"',
        "Mu": '"1.0"',
        "Kappa": '"0.0"',
        "TanD": '"0.0013"',
        "TanDFreq": '"10.0"',
        "TanDGiven": '"True"',
        "TanDModel": '"ConstTanD"',
        "KappaM": '"0.0"',
        "TanDM": '"0.0"',
        "TanDMFreq": ' "0.0"',
        "TanDMGiven": '"False"',
        "TanDMModel": '"ConstKappa"',
        "DispModelEps": '"None"',
        "DispModelMu": '"None"',
        "DispersiveFittingSchemeEps": '"General 1st"',
        "DispersiveFittingSchemeMu": '"General 1st"',
        "UseGeneralDispersionEps": '"False"',
        "UseGeneralDispersionMu": '"False"',
        "Rho": '"0.0"',
        "ThermalType": '"Normal"',
        "ThermalConductivity": '"0.20"',
        "SetActiveMaterial": '"all"',
        "Colour": '"0.94", "0.82", "0.76"',
        "Wireframe": '"False"',
        "Transparency": '"0"',
    },
)

coaxial_dielectric = Material(  # 同轴介质
    "Coaxial dielectric",
    properties={
        "Rho": ' "0.0"',
        "ThermalType": ' "Normal"',
        "ThermalConductivity": ' "0"',
        "HeatCapacity": ' "0"',
        "DynamicViscosity": ' "0"',
        "Emissivity": ' "0"',
        "MetabolicRate": ' "0.0"',
        "VoxelConvection": ' "0.0"',
        "BloodFlow": ' "0"',
        "MechanicsType": ' "Unused"',
        "FrqType ": '"all"',
        "Type": ' "Normal"',
        "Epsilon": ' "2.08"',
        "Mu ": '"1"',
        "Sigma ": '"0"',
        "TanD ": '"0.0"',
        "TanDFreq": ' "0.0"',
        "TanDGiven": ' "False"',
        "TanDModel": ' "ConstTanD"',
        "EnableUserConstTanDModelOrderEps": ' "False"',
        "ConstTanDModelOrderEps": ' "1"',
        "SetElParametricConductivity": ' "False"',
        "ReferenceCoordSystem": ' "Global"',
        "CoordSystemType": ' "Cartesian"',
        "SigmaM": ' "0"',
        "TanDM": ' "0.0"',
        "TanDMFreq": ' "0.0"',
        "TanDMGiven": ' "False"',
        "TanDMModel": ' "ConstTanD"',
        "EnableUserConstTanDModelOrderMu": ' "False"',
        "ConstTanDModelOrderMu": ' "1"',
        "SetMagParametricConductivity ": '"False"',
        "DispModelEps ": ' "None"',
        "DispModelMu ": '"None"',
        "DispersiveFittingSchemeEps": ' "Nth Order"',
        "MaximalOrderNthModelFitEps ": '"10"',
        "ErrorLimitNthModelFitEps": '"0.1"',
        "UseOnlyDataInSimFreqRangeNthModelEps ": '"False"',
        "DispersiveFittingSchemeMu ": '"Nth Order"',
        "MaximalOrderNthModelFitMu": ' "10"',
        "ErrorLimitNthModelFitMu": ' "0.1"',
        "UseOnlyDataInSimFreqRangeNthModelMu": ' "False"',
        "UseGeneralDispersionEps ": '"False"',
        "UseGeneralDispersionMu ": '"False"',
        "NLAnisotropy": ' "False"',
        "NLAStackingFactor": ' "1"',
        "NLADirectionX ": '"1"',
        "NLADirectionY": ' "0"',
        "NLADirectionZ": ' "0"',
        "Colour": ' "0.501961", "1", "0" ',
        "Wireframe": ' "False" ',
        "Reflection": ' "False" ',
        "Allowoutline": ' "True" ',
        "Transparentoutline": ' "False" ',
        "Transparency": ' "0" ',
    },
)
