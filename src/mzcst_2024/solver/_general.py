"""通用绘图对象。"""

import dataclasses
import logging
import typing

from .. import interface
from ..common import NEW_LINE, quoted
from ..global_ import BaseObject, Parameter, ParameterLike
from ..shape_operations import Solid

_logger = logging.getLogger(__name__)


class Background(BaseObject):
    """The background object defines the kind of material that surrounds your
    structure. And defines its volume. By default the volume is defined by the
    maximum distances of your structure.

    Attributes:
        Type (str):
            Sets the material type used for the background.

            `Type` can have one of the following values ->

            `"normal"` (Not conducting, with relative permittivity epsilon and
            relative permeability mu);

            `"pec"` (Perfect electric conducting material).
        Epsilon (str):
            Defines the electric permittivity of the background material.
        Mu (str):
            Defines the permeability of the background material.
        ElConductivity (str):
            Defines the electric conductivity of the background material. This
            value is considered only for Low Frequency simulations.
        XminSpace (str):
            Adds space to the lower or upper x, y or z boundary of the current
            calculation volume respectively.
        XmaxSpace (str):
            same as `XminSpace`.
        YminSpace (str):
            same as `XminSpace`.
        YmaxSpace (str):
            same as `XminSpace`.
        ZminSpace (str):
            same as `XminSpace`.
        ZmaxSpace (str):
            same as `XminSpace`.
        ThermalType (str):
            Sets the material type used for the background. `ThermalType` can
            have one of the following values: `"normal"` (Not thermal
            conducting, with relative permittivity epsilon and relative
            permeability mu.); `"ptc"` (Perfect thermal conducting material).
        ThermalConductivity (str): Thermal conductivity is a property of
            materials that expresses the heat flux f (`W/m2`) that will flow
            through the material if a certain temperature gradient DT (`K/m`)
            exists over the material. The unit for value is `W/K/m`.
        ApplyInAllDirections (bool):
            Is at the moment used for the background dialog to identify if the
            xmin value should be applied in all directions.



    Default Settings::
        Type ("pec")
        Epsilon (1.0)
        Mu (1.0)
        XminSpace (0.0)
        XmaxSpace (0.0)
        YminSpace (0.0)
        YmaxSpace (0.0)
        ZminSpace (0.0)
        ZmaxSpace (0.0)
        ThermalType ("normal")
        ThermalConductivity (0.0)
        ApplyInAllDirections (False)
    """

    def __init__(self, *, attributes: dict[str, str] = None):
        super().__init__(attributes=attributes)

        return

    def create_from_attributes(self, modeler) -> "Background":
        """从属性列表设置背景属性。

        Args:
            modeler (interface.Model3D): 建模环境。

        Returns:
            self (Background): self
        """
        if not self._attributes:
            _logger.error("No valid properties.")
        else:
            scmd1 = [
                "With Background  ",
                ".ResetBackground ",
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
            self._history.append("define background")
            modeler.add_to_history(self._history[-1], cmd)
        return self


class Boundary(BaseObject):
    """Represents the boundary condition of the calculation domain for each
    boundary plane. You may either have a magnetic, electric or an open boundary
    condition.

    Attributes:
        Xmin (str):
            `Xmin (enum boundaryType)`.
            `Xmin`, `Xmax`, `Ymin`, `Ymax`, `Zmin` and `Zmax` specifiy the
            boundary conditions for the lower or upper x, y or z calculation
            domain boundary respectively.
            `boundaryType` can have one of the following values ->
            `"electric"` Electric boundary condition (Etan = 0)
            `"magnetic"` Magnetic boundary condition (Htan = 0)
            `"tangential"` All tangential field components for all sorts of
            fields are zero.
            `"normal"` All normal field components for all sorts of  fields are
            zero.
            `"open"` Simulates the open space.
            `"expanded open"` Same as "open" but adds some extra space to the
            calculation domain.
            `"periodic"` Simulates a periodic expansion of the calculation
            domain.
            `"conducting wall"` This boundary behaves like a wall of lossy metal
            material.
            `"unit cell"` Simulates a unit cell structure.
        Xmax (str): see `Xmin`.
        Ymin (str): see `Xmin`.
        Ymax (str): see `Xmin`.
        Zmin (str): see `Xmin`.
        Zmax (str): see `Xmin`.

        Xsymmetry (str):
            `Xsymmetry (enum symmetryType)`.
            `Xsymmetry`, `Ysymmetry` and `Zsymmetry` define if the structure is
            electrically or magnetically symmetric regarding the origin of the
            x, y or z-axis respectively.
            `symmetryType` can have one of the following values ↓↓↓
            `"electric"` All tangential E-fields are considered zero at the
            symmetry plane.
            `"magnetic"` All tangential H-fields are considered zero at the
            symmetry plane.
            `"none"` No symmetry.
        Ysymmetry (str): see `Xsymmetry`.
        Zsymmetry (str): see `Xsymmetry`.

        ApplyInAllDirections (str):
            `ApplyInAllDirections (bool switch)`.
            Is used by the background dialog to identify if the `Xmin` value
            should be applied in all the other directions.

        XminPotentialType (str):
            `XminPotentialType (enum type)`.
            Specifies the potential type of the lower and upper boundaries. The
            setting of a potential value is only enabled if the type of the
            boundary is set to "normal" or "electric". The potential type can
            have one of the following values ->
            `"none"` No potential is considered on the corresponding boundary.
            `"fixed"` On the boundaries a fixed potential can be defined by use
            of the corresponding Potential methods (see below).
            `"floating"` The potential is defined as floating on the
            corresponding boundary.
        XmaxPotentialType (str): see `XminPotentialType`.
        YminPotentialType (str): see `XminPotentialType`.
        YmaxPotentialType (str): see `XminPotentialType`.
        ZminPotentialType (str): see `XminPotentialType`.
        ZmaxPotentialType (str): see `XminPotentialType`.

        XminPotential (str):
            `XminPotential (double potvalue)`.
            Specifies the potential values of the lower and upper boundaries.
            The setting of a potential value has only an effect if the type of
            the boundary is set to "normal" or "electric" and the corresponding
            `PotentialType` is set to "fixed".
        YminPotential (str): see `XminPotential`.
        ZminPotential (str): see `XminPotential`.
        XmaxPotential (str): see `XminPotential`.
        YmaxPotential (str): see `XminPotential`.
        ZmaxPotential (str):see `XminPotential`.

        XminThermal (str):
            `XminThermal (enum ThermalBoundaryType)`.
            `thermalBoundaryType` can have one of the following values ->
            `"isothermal"` Boundary condition with constant temperature
            (T=const). This boundary type can carry a temperature definition.
            `"adiabatic"` Boundary condition without any heat-flow through the
            boundary (dT / dN = 0).
            `"open"` Simulates the open space.
            `"expanded open"` Same as ”open” but adds some extra space to the
            calculation domain.
        XmaxThermal (str): see `XminThermal`.
        YminThermal (str): see `XminThermal`.
        YmaxThermal (str): see `XminThermal`.
        ZminThermal (str): see `XminThermal`.
        ZmaxThermal (str): see `XminThermal`.

        XsymmetryThermal (str):
            `XsymmetryThermal (enum ThermalSymmetryType)`.
            `thermalSymmetryType` can have one of the following values ->
            "isothermal" Symmetry condition with constant temperature at the symmetry plane (T=const).
            "adiabatic" Symmetry condition without any heat-flow through the symmetry plane (dT / dN = 0).
            "none" No symmetry.
            ”expanded open” Same as ”open” but adds some extra space to the calculation domain.
        YsymmetryThermal (str): see `XsymmetryThermal`.
        ZsymmetryThermal (str): see `XsymmetryThermal`.

        XminTemperature (str):
            `XminTemperatureType (enum type)`.
            Specifies the temperature values of the lower and upper boundaries.
            This settings has only an effect if the type of the corresponding
            `TemperatureType` is set to "fixed".
        XmaxTemperature (str): see `XminTemperature`.
        YminTemperature (str): see `XminTemperature`.
        YmaxTemperature (str): see `XminTemperature`.
        ZminTemperature (str): see `XminTemperature`.
        ZmaxTemperature (str): see `XminTemperature`.

        Layer (str):
            `Layer (int numLayers)`.
            Specifies the number of PML layers. Usually 4 layers are sufficient.
        MinimumLinesDistance (str):
            `MinimumLinesDistance (double value)`.
            Specifies the minimum distance from the PML boundary to the
            structure to be modeled. The distance is determined by the absolute
            number of grid lines.
        MinimumDistanceType (str):
            `MinimumDistanceReferenceFrequencyType (enum {"Center", "Centernmonitors", "User"} type)`.
            Selecting the Fraction option activates the geometrical domain
            enlargement computed as a fraction of the wavelength. With the
            Absolute option the distance is directly given in geometrical user
            units. To this purpose use the SetAbsoluteDistance command.
        SetAbsoluteDistance  (str):
            `SetAbsoluteDistance (double value)`.
            Specifies the absolute distance to enlarge the simulation domain.
            To be used selecting the Absolute option with the command
            `MinimumDistanceType`.
        MinimumDistanceReferenceFrequencyType (str):
            `MinimumDistanceReferenceFrequencyType (enum {"Center", "Centernmonitors", "User"} type)`.
            The command determines the reference frequency where the wavelength
            has to be computed. The command should be used jointly with the
            MinimumDistanceType command activating the Fraction option.
            `"Center"` means that the reference frequency is the mid simulation
            frequency, in formula (FMin+FMax)/2.
            The second choice `"Centernmonitors"` computes the reference frequency
            as the minimum non zero frequency selected among the center
            frequency and the user defined relevant  monitor frequencies.
            The third possibility is `"User"`, which enables to specify directly
            the frequency with the companion FrequencyForMinimumDistance command.
        MinimumDistancePerWavelength (str):
            `MinimumDistancePerWavelength (double value)`.
            Specifies the minimum distance from the PML boundary to the
            structure to be modeled. The distance is determined relatively to
            the wavelength, either in respect to the center frequency, center
            and monitor frequencies or to a user defined frequency value. See
            also the `MinimumDistanceReferenceFrequencyType` command.
        FrequencyForMinimumDistance (str):
            `FrequencyForMinimumDistance (double value)`.
            Specifies the frequency which represents the reference value for the
            `MinimumDistancePerWavelength` method.

        XPeriodicShift (float):
            `XPeriodicShift (double value)`.
            Enables to define a phase shift value for a periodic boundary
            condition. Please note that the phase shift only applies to the
            frequency domain solver and the eigenmode solver. The settings are
            ignored by the transient solver.
        YPeriodicShift (float): see `XPeriodicShift`.
        ZPeriodicShift (float): see `XPeriodicShift`.

        PeriodicUseConstantAngles (bool):
            `PeriodicUseConstantAngles (bool bFlag)`
            In contrast to the definition of a constant phase shift between two
            opposite periodic boundaries (using the `XPeriodicShift`,
            `YPeriodicShift` or `ZPeriodicShift` methods) it is also possible to
            define an incident angle value of the normal propagation direction
            of a virtual plane wave entering the calculation domain. The angle
            can be defined in a spherical coordinate system using the
            `SetPeriodicBoundaryAngles` method. In fact this procedure also
            realizes a phase shift between the periodic boundaries, however,
            this time it depends on the current frequency sample. You can
            activate (bFlag = True) or deactivate (bFlag = False) this option
            using the present method.

        SetPeriodicBoundaryAngles (str):
            `SetPeriodicBoundaryAngles (double theta, double phi)`
            Defines the angle in a spherical coordinate system using theta and
            phi values for the calculation of phase shifts between periodic
            boundaries. The z-axis corresponds to that of the global coordinate
            system.

            Please note that this method is only relevant for the frequency
            domain solver and in case that the `PeriodicUseConstantAngles`
            method is activated or unit cell boundaries are used.
        SetPeriodicBoundaryAnglesDirection (str):
            `SetPeriodicBoundaryAnglesDirection (enum direction)`.
            `direction` defines whether the scan angle defined with
            `SetPeriodicBoundaryAngles` refers to an inward or outward (with
            respect to the radial unit vector in the spherical coordinate
            system) propagating plane wave, and can have one of the following
            values ->
            `”outward”` The phase is set for an outward traveling plane wave.
            Floquet modes should be excited at Zmin.
            `”inward”` The phase is set for an inward traveling plane wave.
            Floquet modes should be excited at Zmax.


        UnitCellDs1 (str):
            `UnitCellDs1 (double value)`.
            These two methods specify the distances between two neighboring unit
            cells in two different coordinate directions, whereby the first axis
            (UnitCellDs1) is always aligned to the x-axis of the global
            coordinate system. The spatial relation between these two axes is
            defined by the `UnitCellAngle` method.
        UnitCellDs2 (str): see `UnitCellDs1`.

        UnitCellAngle (str):
            `UnitCellAngle (double value)`.
            Specifies the spatial relation between the two axes defined by the
            methods `UnitCellDs1` and `UnitCellDs2`.
            Please note, that the hexahedral frequency domain solver needs a
            value of 90 degree for this value.
        UnitCellOrigin (str):
            `UnitCellOrigin  ( double posx, double posy )`.
            Allows to shift the origin of the unit cell and thereby the
            calculation domain for the frequency domain solver with tetrahedral
            mesh. The values may range from zero to one, where the default zero
            lets the center of the bounding box and the center of the unit cell
            coincide, while a value of one moves the origin by half the size of
            the unit cell lattice in the corresponding direction.
        UnitCellFitToBoundingBox (str):
            `UnitCellFitToBoundingBox  ( bool bFlag )`.
            If this method is activated, the structure model will be repeated at
            its bounding box borders, neglecting any settings of the methods
            `UnitCellDs1`, `UnitCellDs2` and `UnitCellAngle`.


    """

    def __init__(
        self,
        *,
        attributes=None,
        vba=None,
    ):
        super().__init__(attributes=attributes, vba=vba)
        return

    def create_from_attributes(self, modeler: interface.Model3D) -> "Boundary":
        """从属性字典定义边界条件。下面的实现给出了一个通用的范式。

        Args:
            modeler (interface.Model3D): 建模环境。

        Returns:
            self (BaseObject): self
        """
        if not self._attributes:
            _logger.error("No valid properties.")
        else:
            scmd1 = [
                "With Boundary ",
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
            self._history.append("define boundary")
            modeler.add_to_history(self._history[-1], cmd)
        return self


class LayerStacking(BaseObject):
    """The `layerstacking` object can be used to define one or more background
    items to the project. The specified layers differ in thickness and material
    and are aligned at the borders of the bounding box.

    Attributes:
        param1 (type): 1st attribute.
    """


class Optimizer(BaseObject):
    """With the optimizer object you may start an optimization run. For the
    optimization you have to define a set of parameters that will be changed by
    the optimizer and at least one goal function that is tried to be optimized.
    The kind of goal function depends on the chosen solver type.

    Attributes:
        param1 (type): 1st attribute.
    """


_parameter_sweep_type = typing.Literal[
    # group 1
    "Transient",
    "Calculate port modes only",
    "Eigenmode",
    "Frequency",
    "TLM",
    "Asymptotic",
    # group 2
    "E-Static",
    "Electroquasistatic",
    "Transient Electroquasistatic",
    "M-Static",
    "Transient Magnetoquasistatic",
    "J-Static",
    "Low Frequency",
    # group 3
    "Thermal",
    "Transient Thermal",
    "Structural Mechanics",
    # group 4
    "PIC",
    "Particle Tracking",
]


@dataclasses.dataclass
class ParameterSamples:
    sequence_name: str
    parameter_name: str
    from_value: str
    to_value: str
    steps: str
    logarithmic_sweep: str


@dataclasses.dataclass
class ParameterStepWidth:
    sequence_name: str
    parameter_name: str
    from_value: str
    to_value: str
    width: str


@dataclasses.dataclass
class ParameterArbitraryPoints:
    sequence_name: str
    parameter_name: str
    points: str


class ParameterSweep(BaseObject):
    """Allows to automatically perform several simulations with varying
    parameters.

    Attributes:
        param1 (type): 1st attribute.
    """

    def __init__(
        self,
        modeler: interface.Model3D,
        simulation_type: _parameter_sweep_type,
    ):
        super().__init__()
        self._modeler = modeler
        self._simulation_type = simulation_type
        self._sequence: list[str] = []
        self._parameter_samples: list[ParameterSamples] = []
        self._parameter_step_width: list[ParameterStepWidth] = []
        self._parameter_arbitrary_points: list[ParameterArbitraryPoints] = []
        return

    @property
    def sequence(self) -> list[str]:
        """The sequence of parameter values to be swept. The format of the
        individual entries depends on the type of the parameter sweep and the
        solver type. Please refer to the CST documentation for more details.

        Returns:
            list[str]: The sequence of parameter values to be swept.
        """
        return self._sequence

    def add_sequence(
        self, sequence_name: str | None = None
    ) -> "ParameterSweep":
        """Defines a new simulation sequence. In a sequence several different
        sets of parameters with different values can be defined. These sets are
        then taken by the parameter sweep to recreate the structure and
        automatically simulate it for each set."""
        if sequence_name is None:
            sequence_name = f"Sequence {len(self._sequence) + 1}"
        self._sequence.append(sequence_name)
        self._modeler.add_to_history(
            f"add sequence {sequence_name}",
            f'ParameterSweep.AddSequence "{sequence_name}"',
        )
        _logger.info(
            "%s",
            f"Added sequence {sequence_name}.",
        )
        return self

    def add_parameter_samples(
        self,
        sequence_name: str,
        parameter_name: str | Parameter,
        from_value: ParameterLike,
        to_value: ParameterLike,
        steps: ParameterLike,
        logarithmic_sweep: bool = False,
    ) -> "ParameterSweep":
        """Defines a set of parameter samples for a given sequence.

        Parameters:
            sequence_name (str): The name of the sequence to which the parameter samples should be added.
            parameter_name (str | Parameter): The name of the parameter for which the samples should be defined.
            from_value (ParameterLike): The starting value of the parameter sweep.
            to_value (ParameterLike): The ending value of the parameter sweep.
            steps (ParameterLike): The number of steps in the parameter sweep.
            logarithmic_sweep (bool): Whether to use a logarithmic scale for the sweep.
        """
        if sequence_name not in self._sequence:
            raise ValueError(
                f"Sequence {sequence_name} does not exist. Please add it first."
            )
        self._parameter_samples.append(
            ParameterSamples(
                sequence_name=sequence_name,
                parameter_name=f"{parameter_name}",
                from_value=f"{from_value}",
                to_value=f"{to_value}",
                steps=f"{steps}",
                logarithmic_sweep=f"{logarithmic_sweep}",
            )
        )
        self._modeler.add_to_history(
            f"add parameter samples for {parameter_name} in {sequence_name}",
            f'ParameterSweep.AddParameter_Samples "{sequence_name}", "{parameter_name}", "{from_value}", "{to_value}", "{steps}", "{logarithmic_sweep}"',
        )
        _logger.info(
            "%s",
            f"Added parameter samples for {parameter_name} in {sequence_name}.",
        )
        return self

    def add_parameter_step_width(
        self,
        sequence_name: str,
        parameter_name: str | Parameter,
        from_value: ParameterLike,
        to_value: ParameterLike,
        width: ParameterLike,
    ) -> "ParameterSweep":
        """Adds a parameter to a sequence.

        Parameters:
            sequence_name (str): The name of the sequence to which the parameter step width should be added.
            parameter_name (str | Parameter): The name of the parameter for which the step width should be defined.
            from_value (ParameterLike): Specify the lower bound of the parameter variation.
            to_value (ParameterLike): Specify  the upper bound of the parameter variation.
            width (ParameterLike):  Specify the width between the samples for the parameter variation.
        """
        if sequence_name not in self._sequence:
            raise ValueError(
                f"Sequence {sequence_name} does not exist. Please add it first."
            )
        self._parameter_step_width.append(
            ParameterStepWidth(
                sequence_name=sequence_name,
                parameter_name=f"{parameter_name}",
                from_value=f"{from_value}",
                to_value=f"{to_value}",
                width=f"{width}",
            )
        )
        self._modeler.add_to_history(
            f"add parameter step width for {parameter_name} in {sequence_name}",
            f'ParameterSweep.AddParameter_StepWidth "{sequence_name}", "{parameter_name}", "{from_value}", "{to_value}", "{width}"',
        )
        _logger.info(
            "%s",
            f"Added parameter step width for {parameter_name} in {sequence_name}.",
        )
        return self

    def add_parameter_arbitary_points(
        self,
        sequence_name: str,
        parameter_name: str | Parameter,
        points: str,
    ) -> "ParameterSweep":
        """Defines a set of parameter samples for a given sequence.
        Parameters:
            sequence_name (str): The name of the sequence to which the parameter samples should be added.
            parameter_name (str | Parameter): The name of the parameter for which the samples should be defined.
            points (str): Specify the value of the sample. Use semicolon as a separator to specify multiple values. e.g. `2 ; 3 ; 3.1 ; 3.2 ; 3.3`
        """
        if sequence_name not in self._sequence:
            raise ValueError(
                f"Sequence {sequence_name} does not exist. Please add it first."
            )
        self._parameter_arbitrary_points.append(
            ParameterArbitraryPoints(
                sequence_name=sequence_name,
                parameter_name=f"{parameter_name}",
                points=f"{points}",
            )
        )
        self._modeler.add_to_history(
            f"add parameter arbitrary points for {parameter_name} in {sequence_name}",
            f'ParameterSweep.AddParameter_ArbitraryPoints "{sequence_name}", "{parameter_name}", "{points}"',
        )
        _logger.info(
            "%s",
            f"Added parameter arbitrary points for {parameter_name} in {sequence_name}.",
        )
        return self

    def delete_parameter(
        self, sequence_name: str, parameter_name: str | Parameter
    ) -> "ParameterSweep":
        """Deletes a parameter from a sequence.

        Parameters:
            sequence_name (str): The name of the sequence from which the parameter should be deleted.
            parameter_name (str | Parameter): The name of the parameter to be deleted.
        """
        self._parameter_samples = [
            ps
            for ps in self._parameter_samples
            if not (
                ps["sequence_name"] == sequence_name
                and ps["parameter_name"] == f"{parameter_name}"
            )
        ]
        self._parameter_step_width = [
            psw
            for psw in self._parameter_step_width
            if not (
                psw["sequence_name"] == sequence_name
                and psw["parameter_name"] == f"{parameter_name}"
            )
        ]
        self._parameter_arbitrary_points = [
            pap
            for pap in self._parameter_arbitrary_points
            if not (
                pap["sequence_name"] == sequence_name
                and pap["parameter_name"] == f"{parameter_name}"
            )
        ]
        self._modeler.add_to_history(
            f"delete parameter {parameter_name} from {sequence_name}",
            f'ParameterSweep.DeleteParameter "{sequence_name}", "{parameter_name}"',
        )
        _logger.info(
            "%s",
            f"Deleted parameter {parameter_name} from {sequence_name}.",
        )
        return self

    def start(self) -> "ParameterSweep":
        """Starts the parameter sweep."""
        self._modeler.add_to_history(
            "start parameter sweep",
            "ParameterSweep.Start",
        )
        _logger.info(
            "%s",
            "Started parameter sweep.",
        )
        return self

    def use_distributed_computing(self, use: bool) -> "ParameterSweep":
        """Enables or disables the use of distributed computing for the parameter sweep.

        Parameters:
            use (bool): Whether to use distributed computing. Default is True.
        """
        self._modeler.add_to_history(
            f"{'enable' if use else 'disable'} distributed computing for parameter sweep",
            f'ParameterSweep.UseDistributedComputing "{use}"',
        )
        _logger.info(
            "%s",
            f"{'Enabled' if use else 'Disabled'} distributed computing for parameter sweep.",
        )
        return self


class SolverParameter(BaseObject):
    """This object controls the model simplification settings for a specific solver.

    Attributes:
        param1 (type): 1st attribute.
    """

    def __init__(self, *, attributes=None, vba=None):
        super().__init__(attributes=attributes, vba=vba)
        return


class ADSCosimulation(BaseObject):
    """In addition to its tight integration into the CST Design Environment, CST
    Microwave Studio also features strong interfaces to Keysight ADS®. Besides
    the ”static” link option offering the possibility to use pre-computed
    S-parameter data in ADS circuit simulations, the ”co-simulation” alternative
    enables ADS to launch CST Microwave Studio in order to automatically
    calculate required data. All information is then stored together with the
    CST Microwave Studio model in order to avoid unnecessary repetitions of
    lengthy EM simulations.

    Please note that this advanced interface requires ADS 2005A or above and
    needs CST Microwave Studio and ADS being installed on the same computer. CST
    Microwave Studio manages an ADS Design Kit which contains a dynamically
    extended list of EM simulation components. Once the ADS Design Kit is
    installed, the library based on CST Microwave Studio models will be
    accessible through the ADS library browser.

    For more detailed information about this and the installation of the ADS
    Design Kit please refer to the CST Studio Suite - Getting Started manual or
    the ADS documentation which is located in the CST Microwave Studio global
    macro directory in the subfolder "ADS\\DesignKit".

    Attributes:
        param1 (type): 1st attribute.
    """

    def __init__(self, *, attributes=None, vba=None):
        super().__init__(attributes=attributes, vba=vba)
        return


class SimuliaCSE(BaseObject):
    """This object offers the possibility to run a co-simulation using Simulia
    Co-Simulation Engine (CSE).

    Attributes:
        param1 (type): 1st attribute.
    """

    def __init__(self, *, attributes=None, vba=None):
        super().__init__(attributes=attributes, vba=vba)
        return
