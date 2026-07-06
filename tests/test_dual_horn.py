import dataclasses
import logging
import math
import os
import sys
import time
import typing

import matplotlib.figure
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

import mzcst_2024 as mz

# 自己的库
from mzcst_2024 import common, component, interface, material
from mzcst_2024 import profiles_to_shapes as p2s
from mzcst_2024 import shape_operations as so
from mzcst_2024 import solver
from mzcst_2024 import transformations_and_picks as tp
from mzcst_2024.common import time_decorator
from mzcst_2024.global_ import Parameter
from mzcst_2024.math_ import bracket
from mzcst_2024.plot import Plot
from mzcst_2024.shape_operations import Solid
from mzcst_2024.shapes import AnalyticalFace, Brick
from mzcst_2024.sources_and_ports.hf import Port
from mzcst_2024.transformations_and_picks import WCS
from mzcst_2024.utils import surfaces, waveguides
from mzcst_2024.utils.unit_cells import JerusalemCross
from mzcst_2024.utils.waveguides import WR90


@dataclasses.dataclass
class TestWR90:
    """测试WR90波导的创建。"""

    current_time: str = common.current_time_string()

    timestamps: list[float] = dataclasses.field(default_factory=list)

    # settings for saving files and logging
    # file_name_prefix = os.path.splitext(os.path.basename(__file__))[0].replace(
    #     "_", "-"
    # )
    file_name_prefix: str = "svl-PLA"
    file_name_prefix_unit_cell: str = "svl-PLA-unit-cell"
    CURRENT_PATH: str = os.path.dirname(os.path.abspath(__file__))
    PARENT_PATH: str = os.path.dirname(CURRENT_PATH)
    RESULT_PATH: str = os.path.join(CURRENT_PATH, "results")
    PROJECT_ABSOLUTE_PATH: str = r"D:\CST-2024-local\fss-PLA-local"

    SAVE_CSV: dict[str, bool] = dataclasses.field(
        default_factory=lambda: {"x": False, "y": False, "all": False}
    )  # 是否保存csv

    logger = logging.getLogger(__name__)
    LOG_PATH: str = os.path.join(PROJECT_ABSOLUTE_PATH, "00-logs")
    LOG_LEVEL = logging.INFO
    FMT = "%(asctime)s.%(msecs)-3d %(name)s - %(levelname)s - %(message)s"
    DATEFMT = r"%Y-%m-%d %H:%M:%S"
    LOG_FORMATTER = logging.Formatter(FMT, DATEFMT)

    @property
    def LOG_FILE_NAME(self) -> str:
        return f"{self.file_name_prefix}-{self.current_time}.log"

    @property
    def LOG_FILE_FULL_PATH(self) -> str:
        return os.path.join(self.LOG_PATH, self.LOG_FILE_NAME)

    # settings for modeling
    # 是否建模
    BUILD_MODEL: bool = True
    SAVE_BEFORE_RUNNING: bool = True  # 是否在求解前保存一次，以防万一
    # 如果求解前不保存，则无视RUN_SOLVER和RUN_PARAMETER_SWEEP的设置，不运行求解器
    RUN_SOLVER: bool = True  # 是否运行求解器
    RUN_PARAMETER_SWEEP: bool = False
    BUILD_SHELL: bool = True  # 是否建模壳体

    @property
    def cst_file_name(self) -> str:
        return f"dual-WR90-{self.current_time}.cst"

    def test_waveguide_performance(self):

        time_all_start: float = time.perf_counter()
        self.timestamps.append(time_all_start)

        filename: str = self.cst_file_name
        fullname: str = os.path.join(self.PROJECT_ABSOLUTE_PATH, filename)
        self.logger.info('Project full path: "%s"', fullname)
        os.startfile(self.PROJECT_ABSOLUTE_PATH)
        design_env = interface.DesignEnvironment()
        proj = design_env.new_mws()
        m3d = proj.model3d
        self.timestamps.append(time.perf_counter())
        self.logger.info(
            "CST started: %s",
            common.time_to_string(self.timestamps[-1] - self.timestamps[-2]),
        )

        fcenter = Parameter("fcenter", "10", "频带中心(GHz)").store(m3d)
        f_test_band = Parameter("f_test_band", "8", "测试频带(GHz)").store(m3d)
        fmin = Parameter(
            "fmin", f"{fcenter - f_test_band / 2}", "频带下限(GHz)"
        ).store(m3d)
        fmax = Parameter(
            "fmax", f"{fcenter + f_test_band / 2}", "频带上限(GHz)"
        ).store(m3d)
        wavelength = (
            (mz.math_.c0 / fcenter / Parameter("1e6"))
            .rename("wavelength")
            .redescribe("中心频率波长")
            .store(m3d)
        )
        theta = Parameter("theta", "0", "入射俯仰角").store(m3d)
        phi = Parameter("phi", "0", "入射方位角").store(m3d)

        horn_gap = (25 * wavelength).rename("horn_gap").store(m3d)

        self.timestamps.append(time.perf_counter())
        self.logger.info(
            "Parameters defined: %s",
            common.time_to_string(self.timestamps[-1] - self.timestamps[-2]),
        )

        copper_annealed = material.Material(
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
        ).create(m3d)

        self.timestamps.append(time.perf_counter())
        self.logger.info(
            "Materials defined: %s, start modeling...",
            common.time_to_string(self.timestamps[-1] - self.timestamps[-2]),
        )

        WCS.activate(m3d, "local")
        horn_up_WCS = (
            WCS(
                "horn_up_WCS",  # 坐标系名称
                "0",  # normal_x
                "0",  # normal_y
                "-1",  # normal_z
                "0",  # origin_x
                "0",  # origin_y
                f"{horn_gap}",  # origin_z
                "1",  # uVector_x
                "0",  # uVector_y
                "0",  # uVector_z
            )
            .set_to_current(m3d)
            .store(m3d)
        )

        port_up = Port(
            "",
            1,
            properties={
                "NumberOfModes": '"1"',
                "AdjustPolarization": '"False"',
                "PolarizationAngle": ' "0.0"',
                "ReferencePlaneDistance": '"0"',
                "TextSize": ' "50"',
                "Coordinates": '"Picks"',
                "Orientation": '"zmax"',
                "PortOnBound": '"True"',
                "ClipPickedPortToBound": ' "False"',
            },
        )

        horn_up = WR90("horn_up", port_up).create_waveguide(m3d)

        self.timestamps.append(time.perf_counter())
        self.logger.info(
            "horn up finished: %s",
            common.time_to_string(self.timestamps[-1] - self.timestamps[-2]),
        )

        horn_down_WCS = (
            WCS(
                "horn_down_WCS",  # 坐标系名称
                "0",  # normal_x
                "0",  # normal_y
                "1",  # normal_z
                "0",  # origin_x
                "0",  # origin_y
                f"{- horn_gap}",  # origin_z
                "1",  # uVector_x
                "0",  # uVector_y
                "0",  # uVector_z
            )
            .set_to_current(m3d)
            .store(m3d)
        )

        port_down = Port(
            "",
            2,
            properties={
                "NumberOfModes": '"1"',
                "AdjustPolarization": '"False"',
                "PolarizationAngle": ' "0.0"',
                "ReferencePlaneDistance": '"0"',
                "TextSize": ' "50"',
                "Coordinates": '"Picks"',
                "Orientation": '"zmin"',
                "PortOnBound": '"True"',
                "ClipPickedPortToBound": ' "False"',
            },
        )

        horn_down = WR90("horn_down", port_down).create_waveguide(m3d)

        self.timestamps.append(time.perf_counter())
        self.logger.info(
            "horn down finished: %s",
            common.time_to_string(self.timestamps[-1] - self.timestamps[-2]),
        )

        WCS.activate(m3d, "global")
        Plot.reset_view(m3d)

        bg = solver.Background(
            attributes={"Type": '"normal"'}
        ).create_from_attributes(m3d)

        bd = solver.Boundary(
            attributes={
                "Xmin": ' "expanded open"',
                "Xmax": ' "expanded open"',
                "Ymin": ' "expanded open"',
                "Ymax": ' "expanded open"',
                "Zmin": ' "expanded open"',
                "Zmax": ' "expanded open"',
                "Xsymmetry": ' "none"',
                "Ysymmetry": ' "none"',
                "Zsymmetry": ' "none"',
                "ApplyInAllDirections": ' "False"',
                "OpenAddSpaceFactor": ' "0.5"',
            }
        ).create_from_attributes(m3d)

        Plot.reset_view(m3d)

        mesh_setting = mz.global_.VbaObject(
            [
                "With Mesh ",
                '     .MeshType "PBA" ',
                '     .SetCreator "High Frequency"',
                "End With ",
                "With MeshSettings ",
                '     .SetMeshType "Hex" ',
                '     .Set "Version", 1%',
                "     'MAX CELL - WAVELENGTH REFINEMENT ",
                '     .Set "StepsPerWaveNear", "10" ',
                '     .Set "StepsPerWaveFar", "5" ',
                '     .Set "WavelengthRefinementSameAsNear", "0" ',
                "     'MAX CELL - GEOMETRY REFINEMENT ",
                '     .Set "StepsPerBoxNear", "15" ',
                '     .Set "StepsPerBoxFar", "1" ',
                '     .Set "MaxStepNear", "0" ',
                '     .Set "MaxStepFar", "0" ',
                '     .Set "ModelBoxDescrNear", "maxedge" ',
                '     .Set "ModelBoxDescrFar", "maxedge" ',
                '     .Set "UseMaxStepAbsolute", "0" ',
                '     .Set "GeometryRefinementSameAsNear", "0" ',
                "     'MIN CELL ",
                '     .Set "UseRatioLimitGeometry", "1" ',
                '     .Set "RatioLimitGeometry", "15" ',
                '     .Set "MinStepGeometryX", "0" ',
                '     .Set "MinStepGeometryY", "0" ',
                '     .Set "MinStepGeometryZ", "0" ',
                '     .Set "UseSameMinStepGeometryXYZ", "1" ',
                "End With ",
                "With MeshSettings ",
                '     .Set "PlaneMergeVersion", "2" ',
                "End With ",
                "With MeshSettings ",
                '     .SetMeshType "Hex" ',
                '     .Set "FaceRefinementType", "NONE" ',
                '     .Set "FaceRefinementRatio", "2" ',
                '     .Set "FaceRefinementStep", "0" ',
                '     .Set "FaceRefinementNSteps", "2" ',
                '     .Set "EllipseRefinementType", "NONE" ',
                '     .Set "EllipseRefinementRatio", "2" ',
                '     .Set "EllipseRefinementStep", "0" ',
                '     .Set "EllipseRefinementNSteps", "2" ',
                '     .Set "FaceRefinementBufferLines", "3" ',
                '     .Set "EdgeRefinementType", "RATIO" ',
                '     .Set "EdgeRefinementRatio", "2" ',
                '     .Set "EdgeRefinementStep", "0" ',
                '     .Set "EdgeRefinementBufferLines", "3" ',
                '     .Set "RefineEdgeMaterialGlobal", "0" ',
                '     .Set "RefineAxialEdgeGlobal", "0" ',
                '     .Set "BufferLinesNear", "3" ',
                '     .Set "UseDielectrics", "1" ',
                '     .Set "EquilibrateOn", "1" ',
                '     .Set "Equilibrate", "1.5" ',
                '     .Set "IgnoreThinPanelMaterial", "0" ',
                "End With ",
                "With MeshSettings ",
                '     .SetMeshType "Hex" ',
                '     .Set "SnapToAxialEdges", "1"',
                '     .Set "SnapToPlanes", "1"',
                '     .Set "SnapToSpheres", "1"',
                '     .Set "SnapToEllipses", "1"',
                '     .Set "SnapToCylinders", "1"',
                '     .Set "SnapToCylinderCenters", "1"',
                '     .Set "SnapToEllipseCenters", "1"',
                '     .Set "SnapToTori", "1"',
                "End With ",
                "With Mesh ",
                '     .ConnectivityCheck "True"',
                '     .UsePecEdgeModel "True" ',
                '     .PointAccEnhancement "0" ',
                '     .TSTVersion "0"',
                '\t  .PBAVersion "2024061424" ',
                '     .SetCADProcessingMethod "MultiThread22", "-1" ',
                '     .SetGPUForMatrixCalculationDisabled "False" ',
                "End With",
            ],
            title="set mesh properties (Hexahedral)",
        )

        units = mz.global_.Units().define(m3d)
        solver.hf.define_frequency_range(m3d, fmin, fmax)
        mz.global_.change_solver_type(m3d, "HF Time Domain")

        solver.hf.SolverHF(
            attributes={
                "Method": ' "Hexahedral"',
                "CalculationType": ' "TD-S"',
                "StimulationPort": ' "All"',
                "StimulationMode": '"All"',
                "SteadyStateLimit": ' "-40"',
                "MeshAdaption": ' "False"',
                "AutoNormImpedance": '"False"',
                "NormingImpedance": '"50"',
                "CalculateModesOnly": '"False"',
                "SParaSymmetry": '"False"',
                "StoreTDResultsInCache": '"False"',
                "RunDiscretizerOnly": '"False"',
                "FullDeembedding": ' "False"',
                "SuperimposePLWExcitation": ' "False"',
                "UseSensitivityAnalysis": ' "False"',
                # 以下是硬件加速设置
                "UseParallelization": ' "True"',  #  开启多线程
                "MaximumNumberOfThreads": ' "64"',  # 设置使用的CPU核心数
                "MaximumNumberOfCPUDevices": ' "2"',  # 设置使用的CPU设备数
                "RemoteCalculation": ' "False"',
                "UseDistributedComputing": ' "True"',  # 开启分布式计算
                "MaxNumberOfDistributedComputingPorts": ' "64"',
                "DistributeMatrixCalculation": ' "True"',
                "MPIParallelization": ' "False"',
                "AutomaticMPI": ' "False"',
                "ConsiderOnly0D1DResultsForMPI": ' "False"',
                "HardwareAcceleration": ' "True"',  # 开启硬件加速
                "MaximumNumberOfGPUs": ' "1"',  # 设置使用的GPU数
            }
        ).create_from_attributes(m3d)

        mz.global_.use_distributed_computing_for_parameters(m3d, True)
        mz.global_.max_number_of_distributed_computing_parameters(m3d, 64)
        mz.global_.use_distributed_computing_memory_setting(m3d, True)
        mz.global_.min_distributed_computing_memory_limit(m3d, 4)
        mz.global_.only_consider_0D_1D_results_for_DC(m3d, False)

        self.timestamps.append(time.perf_counter())
        self.logger.info(
            "settings finished: %s",
            common.time_to_string(self.timestamps[-1] - self.timestamps[-2]),
        )

        parameter_sweep_setup = mz.solver.ParameterSweep(
            m3d, "Transient"
        ).add_sequence("incident angle sweep")
        parameter_sweep_setup.sequence[0].add_parameter_step_width(
            theta, "0", "40", "10"
        )

        if self.SAVE_BEFORE_RUNNING:
            proj.save(fullname)

            if self.RUN_SOLVER:
                m3d.start_solver()
                # while not m3d.solver_finished:
                #     logger.info("solver is running: %s", f"{m3d.solver_info}")
                #     time.sleep(60)
                # proj.save()
                # logger.info("save after solve: %s", fullname)

            if self.RUN_PARAMETER_SWEEP:
                parameter_sweep_setup.start()
                # while not m3d.solver_finished:
                #     logger.info("solver is running: %s", f"{m3d.solver_info}")
                #     time.sleep(60)
                # proj.save()
                # logger.info("save after parameter sweep: %s", fullname)

        time_all_end = time.perf_counter()
        time_all_interval = time_all_end - time_all_start
        self.logger.info(
            "Total run time: %s", common.time_to_string(time_all_interval)
        )

        # endregion
        # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑


@dataclasses.dataclass
class TestWaveguideHornAntenna:
    """测试WR90波导的创建。"""

    current_time: str = common.current_time_string()

    timestamps: list[float] = dataclasses.field(default_factory=list)

    # settings for saving files and logging
    # file_name_prefix = os.path.splitext(os.path.basename(__file__))[0].replace(
    #     "_", "-"
    # )
    file_name_prefix: str = "svl-PLA"
    file_name_prefix_unit_cell: str = "svl-PLA-unit-cell"
    CURRENT_PATH: str = os.path.dirname(os.path.abspath(__file__))
    PARENT_PATH: str = os.path.dirname(CURRENT_PATH)
    RESULT_PATH: str = os.path.join(CURRENT_PATH, "results")
    PROJECT_ABSOLUTE_PATH: str = r"D:\CST-2024-local\fss-PLA-local"

    SAVE_CSV: dict[str, bool] = dataclasses.field(
        default_factory=lambda: {"x": False, "y": False, "all": False}
    )  # 是否保存csv

    logger = logging.getLogger(__name__)
    LOG_PATH: str = os.path.join(PROJECT_ABSOLUTE_PATH, "00-logs")
    LOG_LEVEL = logging.INFO
    FMT = "%(asctime)s.%(msecs)-3d %(name)s - %(levelname)s - %(message)s"
    DATEFMT = r"%Y-%m-%d %H:%M:%S"
    LOG_FORMATTER = logging.Formatter(FMT, DATEFMT)

    @property
    def LOG_FILE_NAME(self) -> str:
        return f"{self.file_name_prefix}-{self.current_time}.log"

    @property
    def LOG_FILE_FULL_PATH(self) -> str:
        return os.path.join(self.LOG_PATH, self.LOG_FILE_NAME)

    # settings for modeling
    # 是否建模
    BUILD_MODEL: bool = True
    SAVE_BEFORE_RUNNING: bool = True  # 是否在求解前保存一次，以防万一
    # 如果求解前不保存，则无视RUN_SOLVER和RUN_PARAMETER_SWEEP的设置，不运行求解器
    RUN_SOLVER: bool = True  # 是否运行求解器
    RUN_PARAMETER_SWEEP: bool = False
    BUILD_SHELL: bool = True  # 是否建模壳体

    horn_type = waveguides.RWHA187_10

    @property
    def cst_file_name(self) -> str:
        return f"dual-{self.horn_type.__name__}-{self.current_time}.cst"

    # 求解设置
    f_center = 5
    f_test_band = 4

    def test_waveguide_performance(self):

        time_all_start: float = time.perf_counter()
        self.timestamps.append(time_all_start)

        filename: str = self.cst_file_name
        fullname: str = os.path.join(self.PROJECT_ABSOLUTE_PATH, filename)
        self.logger.info('Project full path: "%s"', fullname)
        os.startfile(self.PROJECT_ABSOLUTE_PATH)
        design_env = interface.DesignEnvironment()
        proj = design_env.new_mws()
        m3d = proj.model3d
        self.timestamps.append(time.perf_counter())
        self.logger.info(
            "CST started: %s",
            common.time_to_string(self.timestamps[-1] - self.timestamps[-2]),
        )

        fcenter = Parameter(
            "fcenter", f"{self.f_center}", "频带中心(GHz)"
        ).store(m3d)
        f_test_band = Parameter(
            "f_test_band", f"{self.f_test_band}", "测试频带(GHz)"
        ).store(m3d)
        fmin = Parameter(
            "fmin", f"{fcenter - f_test_band / 2}", "频带下限(GHz)"
        ).store(m3d)
        fmax = Parameter(
            "fmax", f"{fcenter + f_test_band / 2}", "频带上限(GHz)"
        ).store(m3d)
        wavelength = (
            (mz.math_.c0 / fcenter / Parameter("1e6"))
            .rename("wavelength")
            .redescribe("中心频率波长")
            .store(m3d)
        )
        theta = Parameter("theta", "0", "入射俯仰角").store(m3d)
        phi = Parameter("phi", "0", "入射方位角").store(m3d)

        horn_gap = (0 * wavelength).rename("horn_gap").store(m3d)

        self.timestamps.append(time.perf_counter())
        self.logger.info(
            "Parameters defined: %s",
            common.time_to_string(self.timestamps[-1] - self.timestamps[-2]),
        )

        copper_annealed = material.Material(
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
        ).create(m3d)

        self.timestamps.append(time.perf_counter())
        self.logger.info(
            "Materials defined: %s, start modeling...",
            common.time_to_string(self.timestamps[-1] - self.timestamps[-2]),
        )

        WCS.activate(m3d, "local")
        horn_up_WCS = (
            WCS(
                "horn_up_WCS",  # 坐标系名称
                "0",  # normal_x
                "0",  # normal_y
                "-1",  # normal_z
                "0",  # origin_x
                "0",  # origin_y
                f"{self.horn_type.total_length + horn_gap}",  # origin_z
                "1",  # uVector_x
                "0",  # uVector_y
                "0",  # uVector_z
            )
            .set_to_current(m3d)
            .store(m3d)
        )

        port_up = Port(
            "",
            1,
            properties={
                "NumberOfModes": '"1"',
                "AdjustPolarization": '"False"',
                "PolarizationAngle": ' "0.0"',
                "ReferencePlaneDistance": '"0"',
                "TextSize": ' "50"',
                "Coordinates": '"Picks"',
                "Orientation": '"zmax"',
                "PortOnBound": '"True"',
                "ClipPickedPortToBound": ' "False"',
            },
        )

        horn_up = self.horn_type("horn_up", port_up).create_waveguide(m3d)

        self.timestamps.append(time.perf_counter())
        self.logger.info(
            "horn up finished: %s",
            common.time_to_string(self.timestamps[-1] - self.timestamps[-2]),
        )

        horn_down_WCS = (
            WCS(
                "horn_down_WCS",  # 坐标系名称
                "0",  # normal_x
                "0",  # normal_y
                "1",  # normal_z
                "0",  # origin_x
                "0",  # origin_y
                f"{- self.horn_type.total_length - horn_gap}",  # origin_z
                "1",  # uVector_x
                "0",  # uVector_y
                "0",  # uVector_z
            )
            .set_to_current(m3d)
            .store(m3d)
        )

        port_down = Port(
            "",
            2,
            properties={
                "NumberOfModes": '"1"',
                "AdjustPolarization": '"False"',
                "PolarizationAngle": ' "0.0"',
                "ReferencePlaneDistance": '"0"',
                "TextSize": ' "50"',
                "Coordinates": '"Picks"',
                "Orientation": '"zmin"',
                "PortOnBound": '"True"',
                "ClipPickedPortToBound": ' "False"',
            },
        )

        horn_down = self.horn_type("horn_down", port_down).create_waveguide(m3d)

        self.timestamps.append(time.perf_counter())
        self.logger.info(
            "horn down finished: %s",
            common.time_to_string(self.timestamps[-1] - self.timestamps[-2]),
        )

        WCS.activate(m3d, "global")
        Plot.reset_view(m3d)

        bg = solver.Background(
            attributes={"Type": '"normal"'}
        ).create_from_attributes(m3d)

        bd = solver.Boundary(
            attributes={
                "Xmin": ' "expanded open"',
                "Xmax": ' "expanded open"',
                "Ymin": ' "expanded open"',
                "Ymax": ' "expanded open"',
                "Zmin": ' "expanded open"',
                "Zmax": ' "expanded open"',
                "Xsymmetry": ' "none"',
                "Ysymmetry": ' "none"',
                "Zsymmetry": ' "none"',
                "ApplyInAllDirections": ' "False"',
                "OpenAddSpaceFactor": ' "0.5"',
            }
        ).create_from_attributes(m3d)

        Plot.reset_view(m3d)

        mesh_setting = mz.global_.VbaObject(
            [
                "With Mesh ",
                '     .MeshType "PBA" ',
                '     .SetCreator "High Frequency"',
                "End With ",
                "With MeshSettings ",
                '     .SetMeshType "Hex" ',
                '     .Set "Version", 1%',
                "     'MAX CELL - WAVELENGTH REFINEMENT ",
                '     .Set "StepsPerWaveNear", "10" ',
                '     .Set "StepsPerWaveFar", "5" ',
                '     .Set "WavelengthRefinementSameAsNear", "0" ',
                "     'MAX CELL - GEOMETRY REFINEMENT ",
                '     .Set "StepsPerBoxNear", "15" ',
                '     .Set "StepsPerBoxFar", "1" ',
                '     .Set "MaxStepNear", "0" ',
                '     .Set "MaxStepFar", "0" ',
                '     .Set "ModelBoxDescrNear", "maxedge" ',
                '     .Set "ModelBoxDescrFar", "maxedge" ',
                '     .Set "UseMaxStepAbsolute", "0" ',
                '     .Set "GeometryRefinementSameAsNear", "0" ',
                "     'MIN CELL ",
                '     .Set "UseRatioLimitGeometry", "1" ',
                '     .Set "RatioLimitGeometry", "15" ',
                '     .Set "MinStepGeometryX", "0" ',
                '     .Set "MinStepGeometryY", "0" ',
                '     .Set "MinStepGeometryZ", "0" ',
                '     .Set "UseSameMinStepGeometryXYZ", "1" ',
                "End With ",
                "With MeshSettings ",
                '     .Set "PlaneMergeVersion", "2" ',
                "End With ",
                "With MeshSettings ",
                '     .SetMeshType "Hex" ',
                '     .Set "FaceRefinementType", "NONE" ',
                '     .Set "FaceRefinementRatio", "2" ',
                '     .Set "FaceRefinementStep", "0" ',
                '     .Set "FaceRefinementNSteps", "2" ',
                '     .Set "EllipseRefinementType", "NONE" ',
                '     .Set "EllipseRefinementRatio", "2" ',
                '     .Set "EllipseRefinementStep", "0" ',
                '     .Set "EllipseRefinementNSteps", "2" ',
                '     .Set "FaceRefinementBufferLines", "3" ',
                '     .Set "EdgeRefinementType", "RATIO" ',
                '     .Set "EdgeRefinementRatio", "2" ',
                '     .Set "EdgeRefinementStep", "0" ',
                '     .Set "EdgeRefinementBufferLines", "3" ',
                '     .Set "RefineEdgeMaterialGlobal", "0" ',
                '     .Set "RefineAxialEdgeGlobal", "0" ',
                '     .Set "BufferLinesNear", "3" ',
                '     .Set "UseDielectrics", "1" ',
                '     .Set "EquilibrateOn", "1" ',
                '     .Set "Equilibrate", "1.5" ',
                '     .Set "IgnoreThinPanelMaterial", "0" ',
                "End With ",
                "With MeshSettings ",
                '     .SetMeshType "Hex" ',
                '     .Set "SnapToAxialEdges", "1"',
                '     .Set "SnapToPlanes", "1"',
                '     .Set "SnapToSpheres", "1"',
                '     .Set "SnapToEllipses", "1"',
                '     .Set "SnapToCylinders", "1"',
                '     .Set "SnapToCylinderCenters", "1"',
                '     .Set "SnapToEllipseCenters", "1"',
                '     .Set "SnapToTori", "1"',
                "End With ",
                "With Mesh ",
                '     .ConnectivityCheck "True"',
                '     .UsePecEdgeModel "True" ',
                '     .PointAccEnhancement "0" ',
                '     .TSTVersion "0"',
                '\t  .PBAVersion "2024061424" ',
                '     .SetCADProcessingMethod "MultiThread22", "-1" ',
                '     .SetGPUForMatrixCalculationDisabled "False" ',
                "End With",
            ],
            title="set mesh properties (Hexahedral)",
        )

        units = mz.global_.Units().define(m3d)
        solver.hf.define_frequency_range(m3d, fmin, fmax)
        mz.global_.change_solver_type(m3d, "HF Time Domain")

        solver.hf.SolverHF(
            attributes={
                "Method": ' "Hexahedral"',
                "CalculationType": ' "TD-S"',
                "StimulationPort": ' "All"',
                "StimulationMode": '"All"',
                "SteadyStateLimit": ' "-40"',
                "MeshAdaption": ' "False"',
                "AutoNormImpedance": '"False"',
                "NormingImpedance": '"50"',
                "CalculateModesOnly": '"False"',
                "SParaSymmetry": '"False"',
                "StoreTDResultsInCache": '"False"',
                "RunDiscretizerOnly": '"False"',
                "FullDeembedding": ' "False"',
                "SuperimposePLWExcitation": ' "False"',
                "UseSensitivityAnalysis": ' "False"',
                # 以下是硬件加速设置
                "UseParallelization": ' "True"',  #  开启多线程
                "MaximumNumberOfThreads": ' "64"',  # 设置使用的CPU核心数
                "MaximumNumberOfCPUDevices": ' "2"',  # 设置使用的CPU设备数
                "RemoteCalculation": ' "False"',
                "UseDistributedComputing": ' "True"',  # 开启分布式计算
                "MaxNumberOfDistributedComputingPorts": ' "64"',
                "DistributeMatrixCalculation": ' "True"',
                "MPIParallelization": ' "False"',
                "AutomaticMPI": ' "False"',
                "ConsiderOnly0D1DResultsForMPI": ' "False"',
                "HardwareAcceleration": ' "True"',  # 开启硬件加速
                "MaximumNumberOfGPUs": ' "1"',  # 设置使用的GPU数
            }
        ).create_from_attributes(m3d)

        mz.global_.use_distributed_computing_for_parameters(m3d, True)
        mz.global_.max_number_of_distributed_computing_parameters(m3d, 64)
        mz.global_.use_distributed_computing_memory_setting(m3d, True)
        mz.global_.min_distributed_computing_memory_limit(m3d, 4)
        mz.global_.only_consider_0D_1D_results_for_DC(m3d, False)

        self.timestamps.append(time.perf_counter())
        self.logger.info(
            "settings finished: %s",
            common.time_to_string(self.timestamps[-1] - self.timestamps[-2]),
        )

        parameter_sweep_setup = mz.solver.ParameterSweep(
            m3d, "Transient"
        ).add_sequence("incident angle sweep")
        parameter_sweep_setup.sequence[0].add_parameter_step_width(
            theta, "0", "40", "10"
        )

        if self.SAVE_BEFORE_RUNNING:
            proj.save(fullname)

            if self.RUN_SOLVER:
                m3d.start_solver()
                # while not m3d.solver_finished:
                #     logger.info("solver is running: %s", f"{m3d.solver_info}")
                #     time.sleep(60)
                # proj.save()
                # logger.info("save after solve: %s", fullname)

            if self.RUN_PARAMETER_SWEEP:
                parameter_sweep_setup.start()
                # while not m3d.solver_finished:
                #     logger.info("solver is running: %s", f"{m3d.solver_info}")
                #     time.sleep(60)
                # proj.save()
                # logger.info("save after parameter sweep: %s", fullname)

        time_all_end = time.perf_counter()
        time_all_interval = time_all_end - time_all_start
        self.logger.info(
            "Total run time: %s", common.time_to_string(time_all_interval)
        )

        # endregion
        # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑


class TestRWHA159_20(TestWaveguideHornAntenna):
    """测试RWHA159-20波导的创建。"""

    horn_type = waveguides.RWHA159_20
    f_center = 5
    f_test_band = 4


class TestRWHA159_15(TestWaveguideHornAntenna):
    """测试RWHA159-15波导的创建。"""

    horn_type = waveguides.RWHA159_15
    f_center = 5
    f_test_band = 4


class TestRWHA159_10(TestWaveguideHornAntenna):
    """测试RWHA159-10波导的创建。"""

    horn_type = waveguides.RWHA159_10
    f_center = 5
    f_test_band = 4

class TestPEWAN090_20(TestWaveguideHornAntenna):
    """测试PEWAN090-20波导的创建。"""

    horn_type = waveguides.PEWAN090_20
    f_center = 10
    f_test_band = 4

class TestRWHA187_10(TestWaveguideHornAntenna):
    """测试RWHA187-10波导的创建。"""

    horn_type = waveguides.RWHA187_10
    f_center = 5
    f_test_band = 4

if __name__ == "__main__":
    test = TestRWHA187_10()
    test.test_waveguide_performance()
