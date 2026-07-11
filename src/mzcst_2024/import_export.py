"""本模块用于导入和导出模型文件，包括二维和三维模型文件。"""

import logging
import typing
from pathlib import PurePath, PurePosixPath

from . import interface
from .common import NEW_LINE, quoted
from .global_ import BaseObject, CSTPath, Parameter

__all__: list[str] = []

_logger = logging.getLogger(__name__)


class ADSComponentExport(BaseObject):
    """(todo) This command offers the option to create an ADS® parametric component based  on the current project."""

    def __init__(
        self,
        name: str,
    ):
        super().__init__()
        self._name: str = name
        return


class DXF(BaseObject):
    """(todo) This command offers 2D DXF file import. With this feature you can import data from CAD systems which provide the famous DXF file format from Autodesk Inc. as an export option.

    The 2D data is imported relative to the current coordinate system and extruded with a profile height to a 3D solid. Use this import option to import printed circuits or complex microstrip lines.

    If you need to import pure 3D data it is recommended to use the SAT or IGES import.
    """

    def __init__(
        self,
        name: str,
    ):
        super().__init__()
        self._name: str = name
        return


class GDSII(BaseObject):
    """(todo) This command offers GDSII stream file import. With this feature you can import data from any IC package system providing the GDSII stream format.

    The GDSII data is imported relative to the current coordinate system and extruded with a profile height to a 3D solid. Use this import option to import printed circuits or complex microstrip lines.
    """

    def __init__(
        self,
        name: str,
    ):
        super().__init__()
        self._name: str = name
        return


class GERBER(BaseObject):
    """(todo)This command offers GERBER file import (RS274-D, RS274-X). With this feature you can import data from any IC package system providing the GERBER format.

    The GERBER data is imported relative to the current coordinate system and extruded with a profile height to a 3D solid. Use this import option to import the 2D profiles of printed circuits or complex microstrip lines. In case of a standard GERBER file (RS274-D) you need to specify the appropriate aperture file.
    """

    def __init__(
        self,
        name: str,
    ):
        super().__init__()
        self._name: str = name
        return


class SAT(BaseObject):
    """(todo) This command offers SAT file import. With this feature you can import data from any other ACIS based CAD system.

    If possible use this interface for 3D data import instead of IGES / STL import, because this is the programs native format.
    """

    def __init__(
        self,
        name: str,
    ):
        super().__init__()
        self._name: str = name
        return


class STL(BaseObject):
    """(todo) Most of today’s CAD systems offer STL import/export options. In case your CAD system does not support SAT or IGES export you might import structure data via the STL interface. Though STL data export/import is very common, STL data import can take some time and might lead to a very slow meshing process, because every STL triangle will be converted to an ACIS FACE.

    If you have the choice between a high end data format like SAT / IGES and STL – choose the high end format, because further operations on the structure will be much faster.
    """

    def __init__(
        self,
        name: str,
    ):
        super().__init__()
        self._name: str = name
        return


class OBJ(BaseObject):
    """(todo) This object offers you the options for import object files (.obj). OBJ data import can take some time and might lead to a very slow meshing process, because every OBJ triangle will be converted to an ACIS FACE.

    If you have the choice between a high end data format like SAT / IGES and OBJ – choose the high end format, because further operations on the structure will be much faster.
    """

    def __init__(
        self,
        name: str,
    ):
        super().__init__()
        self._name: str = name
        return


class IGES(BaseObject):
    """(todo) Offers the import of IGES files written by many of today’s CAD systems. Because  the ACIS kernel uses the SAT data format, IGES data need to be converted to ACIS data and checked for consistency (so-called healing)."""

    def __init__(
        self,
        name: str,
    ):
        super().__init__()
        self._name: str = name
        return


class VDAFS(BaseObject):
    """(todo) Import CAD data from VDAFS files."""

    def __init__(
        self,
        name: str,
    ):
        super().__init__()
        self._name: str = name
        return


class STEP(BaseObject):
    """(todo) Import Step CAD data."""

    def __init__(
        self,
        name: str,
    ):
        super().__init__()
        self._name: str = name
        return


class AutodeskInventor(BaseObject):
    """(todo) Import CAD data from Autodesk's Inventor CAD system."""

    def __init__(
        self,
        name: str,
    ):
        super().__init__()
        self._name: str = name
        return


class PROE(BaseObject):
    """(todo) Import CAD data from Pro/ENGINEER (PTC) CAD system."""

    def __init__(
        self,
        name: str,
    ):
        super().__init__()
        self._name: str = name
        return


class CATIA(BaseObject):
    """(todo) Import CATIA V4, CATIA V5 and 3DExperience CATIA files."""

    def __init__(
        self,
        name: str,
    ):
        super().__init__()
        self._name: str = name
        return


class CoventorWare(BaseObject):
    """(todo) Import a CoventorWare file."""

    def __init__(
        self,
        name: str,
    ):
        super().__init__()
        self._name: str = name
        return


class HumanModel(BaseObject):
    """(todo) This command offers the import of voxel data sets.

    The voxel data materials (except the air material) override any other material defined at the same location. If there is no other material defined besides the air material of the voxel data, the default background material is used.
    """

    def __init__(
        self,
        name: str,
    ):
        super().__init__()
        self._name: str = name
        return


class TOUCHSTONE(BaseObject):
    """(todo) This command offers TOUCHSTONE file compatible export for the S-parameters. The extensions of the exported files names are specified by ”.sNp” where N stands for the number of ports in your model (e.g. ”.s3p”).

    The TOUCHSTONE file contains a fixed reference impedance. During the export process, usually the S-parameters will be automatically normed to this impedance, if necessary. In some rare cases it may also be useful to export the S-parameters as they are (without renorming), but nevertheless specifying a reference impedance in the TOUCHSTONE file.
    """

    def __init__(
        self,
        name: str,
    ):
        super().__init__()
        self._name: str = name
        return


class ASCIIExport(BaseObject):
    """(todo) Export result data as an ASCII file."""

    def __init__(
        self,
        name: str,
    ):
        super().__init__()
        self._name: str = name
        return


class NASTRAN(BaseObject):
    """(todo) Import a NASTRAN file."""

    def __init__(
        self,
        name: str,
    ):
        super().__init__()
        self._name: str = name
        return


class Mecadtron(BaseObject):
    """(todo) Import a Mecadtron file."""

    def __init__(
        self,
        name: str,
    ):
        super().__init__()
        self._name: str = name
        return


class LayoutDB(BaseObject):
    """(todo) This object is used to conduct the import of PCB models from 3rd-party EDA tools. To work correctly, the command methods must be executed in the order shown below."""

    def __init__(
        self,
        name: str,
    ):
        super().__init__()
        self._name: str = name
        return


class ImportEDADefaults(BaseObject):
    """(todo) This object is used to specify the defaults settings to be used by the EDA import upon first import.

    For further details, see the documentation of the EDA import dialog.
    """

    def __init__(
        self,
        name: str,
    ):
        super().__init__()
        self._name: str = name
        return


class NFSFile(BaseObject):
    """(todo) The NFS file format allows the imprint of equivalent surface fields on a box or even on single planes. This format is especially designed for scan data and is able to handle an equidistant as well as a non-equidistant sampled spatial distribution of field data.

    The format is based on the IEC® Technical Report IEC/TR 61967-1-1.



    In order to describe surface fields on a rectangular box surface, each face and field component has to be defined  in a single XML-file and a corresponding DAT-file.

    The XML-file contains all meta-data such as field type, field components (Ex, Ey, Ez, Hx, Hy, Hz ), frequencies, and a reference to the DAT-file.

    The DAT-file contains the actual field data values in the following ASCII pattern:



    `x0 y0 z0 Re(freq1) Im(freq1) Re(freq2) Im(freq2) Re(freq3) Im(freq3) ...`

    `x1 y0 z0 Re(freq1) Im(freq1) Re(freq2) Im(freq2) Re(freq3) Im(freq3) ...`

    `x0 y1 z0 Re(freq1) Im(freq1) Re(freq2) Im(freq2) Re(freq3) Im(freq3) ...`

    `...`



    Where (`x_i`, `y_i`, `z_i`) describe point positions of a cartesian grid and Re(freq1) / Im(freq2) the real / imaginary part of the field value at frequency freq1 and position (x_i, y_i, z_i). Example files for the supported types of the NFS format for the CST Microwave Studio transient solver can be found here. A detailed description of the file syntax can be found in  IEC® Technical Report IEC/TR 61967-1-1.
    """

    def __init__(
        self,
        name: str,
    ):
        super().__init__()
        self._name: str = name
        return


class LiveLink(BaseObject):
    """(todo) This object is used to manage the synchronization of parameters with an external application like used for the parametric imports. Currently the object can not be used to create a parametric import."""

    def __init__(
        self,
        name: str,
    ):
        super().__init__()
        self._name: str = name
        return


class SolidWorks(BaseObject):
    """(todo) Import part file or an entire assembly from SolidWorks."""

    def __init__(
        self,
        name: str,
    ):
        super().__init__()
        self._name: str = name
        return


class SolidEdge(BaseObject):
    """(todo) Import part file or an entire assembly from Solid Edge."""

    def __init__(
        self,
        name: str,
    ):
        super().__init__()
        self._name: str = name
        return


class SiemensNX(BaseObject):
    """(todo) Import part file or an entire assembly from Siemens PLM software."""

    def __init__(
        self,
        name: str,
    ):
        super().__init__()
        self._name: str = name
        return


class Parasolid(BaseObject):
    """(todo) Import Parasolid CAD data."""

    def __init__(
        self,
        name: str,
    ):
        super().__init__()
        self._name: str = name
        return


class MeshImport(BaseObject):
    """(todo) Import Abacus and Nastran files."""

    def __init__(
        self,
        name: str,
    ):
        super().__init__()
        self._name: str = name
        return
