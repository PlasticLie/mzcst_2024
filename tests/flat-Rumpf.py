"""参照论文(Valle, 2023)复现其中的椭圆抛物面共形FSS。

Cesar L. VALLE, Gilbert T. CARRANZA, Raymond C. RUMPF. Conformal Frequency
Selective Surfaces for Arbitrary Curvature[J]. IEEE Transactions on Antennas and
Propagation, 2023,71(1): 612-620.

https://ieeexplore.ieee.org/document/9933174/
"""

import logging
import math
import os
import sys
import time

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

import mzcst_2024 as mz
from mzcst_2024 import _global, common, component, interface, material
from mzcst_2024 import profiles_to_shapes as p2s
from mzcst_2024 import shape_operations as so
from mzcst_2024 import solver
from mzcst_2024 import transformations_and_picks as tp
from mzcst_2024._global import Parameter
from mzcst_2024.common import NEW_LINE, OPERATION_FAILED, OPERATION_SUCCESS, quoted
from mzcst_2024.math_ import bracket
from mzcst_2024.plot import Plot
from mzcst_2024.shape_operations import Solid
from mzcst_2024.shapes import AnalyticalFace, Brick
from mzcst_2024.sources_and_ports.hf import Port
from mzcst_2024.transformations_and_picks import WCS
from mzcst_2024.utils import unit_cells

if __name__ == "__main__":
    #######################################
    # region 开始计时
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

    time_all_start: float = time.time()
    current_time: str = common.current_time_string()

    CURRENT_PATH: str = os.path.dirname(
        os.path.abspath(__file__)
    )  # 获取当前py文件所在文件夹
    PARENT_PATH: str = os.path.dirname(CURRENT_PATH)

    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    #######################################
    # region 日志设置
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

    LOG_PATH: str = os.path.join(PARENT_PATH, "logs")
    LOG_FILE_NAME: str = "flat-Rumpf-demo-" + current_time + ".log"
    LOG_LEVEL = logging.INFO
    FMT = "%(asctime)s.%(msecs)-3d %(name)s - %(levelname)s - %(message)s"
    DATEFMT = r"%Y-%m-%d %H:%M:%S"
    LOG_FORMATTER = logging.Formatter(FMT, DATEFMT)
    common.create_folder(LOG_PATH)
    logging.basicConfig(
        format=FMT, datefmt=DATEFMT, level=LOG_LEVEL, force=True
    )
    root_logger = logging.getLogger()
    root_logger.setLevel(LOG_LEVEL)
    logger = logging.getLogger(__name__)
    logger.setLevel(LOG_LEVEL)
    file_handler = logging.FileHandler(os.path.join(LOG_PATH, LOG_FILE_NAME))
    file_handler.setFormatter(LOG_FORMATTER)
    file_handler.setLevel(LOG_LEVEL)
    root_logger.addHandler(file_handler)
    logger.info("Start logging.")

    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    #######################################
    # region 仿真环境
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

    # PROJECT_PATH: str = "cst_projects"
    # create_folder(PROJECT_PATH)
    # PROJECT_ABSOLUTE_PATH: str = os.path.join(PARENT_PATH, PROJECT_PATH)
    PROJECT_ABSOLUTE_PATH: str = r"D:\CST-2024-local\fss-rumpf-local"
    filename: str = "flat-demo-" + current_time + ".cst"
    fullname: str = os.path.join(PROJECT_ABSOLUTE_PATH, filename)
    logger.info('Project full path: "%s"', fullname)
    design_env: interface.DesignEnvironment = interface.DesignEnvironment()
    proj: "interface.Project" = design_env.new_mws()
    m3d: "interface.Model3D" = proj.model3d
    logger.info("CST started.")

    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    #######################################
    # region CST参数
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

    # 单元
    eps_sub: Parameter = Parameter("eps_sub", "2.25", "基板介电常数").store(m3d)
    fmin: Parameter = Parameter("fmin", "8.2", "频带下限(GHz)").store(m3d)
    fmax: Parameter = Parameter("fmax", "12.4", "频带上限(GHz)").store(m3d)
    fcenter = (bracket(fmin + fmax) / Parameter(2)).rename("fcenter").store(m3d)
    wavelength = (
        (Parameter("3e8") / fcenter / Parameter("1e6"))
        .rename("wavelength")
        .re_describe("中心频率波长")
        .store(m3d)
    )
    theta: Parameter = Parameter("theta", "0", "入射俯仰角").store(m3d)
    phi: Parameter = Parameter("phi", "0", "入射方位角").store(m3d)
    l_sub: Parameter = Parameter("l_sub", "9.95").store(m3d)
    w_sub: Parameter = Parameter("w_sub", "l_sub").store(m3d)
    h_sub: Parameter = Parameter("h_sub", "3.16").store(m3d)
    l_cross: Parameter = Parameter("l_cross", "2.32").store(m3d)
    w_cross: Parameter = Parameter("w_cross", "1").store(m3d)
    l_hat: Parameter = Parameter("h_hat", "4.5").store(m3d)
    w_hat: Parameter = Parameter("w_hat", "0.9").store(m3d)
    h_trace = Parameter("h_trace", "0.035", "铜厚").store(m3d)
    l_unit: Parameter = (
        (Parameter(2) * bracket(w_hat + l_cross) + w_cross)
        .rename("l_unit")
        .re_describe("十字结构的长度")
        .store(m3d)
    )
    w_unit: Parameter = (
        (Parameter(2) * bracket(w_hat + l_cross) + w_cross)
        .rename("w_unit")
        .re_describe("十字结构的宽度")
        .store(m3d)
    )
    center_x = Parameter("center_x", f"{l_sub.name} / 2").store(m3d)
    center_y = Parameter("center_y", f"{w_sub.name} / 2").store(m3d)

    unit_base_x = Parameter("unit_base_x", center_x.name).store(m3d)
    unit_base_y = Parameter("unit_base_y", center_y.name).store(m3d)

    # 喇叭天线
    taper_angle = Parameter("taper_angle", "11.2").store(m3d)
    horn_length = Parameter("horn_length", "218.16").store(m3d)
    wall_thickness = Parameter("wall_thickness", "3.78").store(m3d)
    waveguide_width = Parameter("waveguide_width", "37.38").store(m3d)
    waveguide_height = Parameter("waveguide_height", "16.38").store(m3d)
    # horn_gap = Parameter("horn_gap", "100").store(m3d)
    horn_gap = (Parameter(15) * wavelength).rename("horn_gap").store(m3d)

    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    #######################################
    # region 材料定义
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
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

    rogers_RT5880_lossy = material.Material(
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
    ).create(m3d)

    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    #######################################
    # region CST建模
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

    ARRAY_SIZE = (50,50)  # (row, col)
    WCS.activate(m3d, "local")
    unit_WCS: list[WCS] = []
    unit_cells: list = []
    unit_count = 0
    for row in range(ARRAY_SIZE[0]):
        for col in range(ARRAY_SIZE[1]):
            unit_WCS.append(
                WCS(
                    "unit_wcs" + "_" + str(row) + "_" + str(col),  # 坐标系名称
                    "0",  # normal_x
                    "0",  # normal_y
                    "1",  # normal_z
                    (l_sub * Parameter(row)).name,  # origin_x
                    (w_sub * Parameter(col)).name,  # origin_y
                    "0",  # origin_z
                    "1",  # uVector_x
                    "0",  # uVector_y
                    "0",  # uVector_z
                )
                .set_to_current(m3d)
                .store(m3d)
            )
            unit_comp: str = "unit" + "_" + str(row) + "_" + str(col)
            substrate_comp: str = "substrate"
            sub = Brick(
                "substrate",  # 实体名
                "0",  # xmin
                l_sub.name,  # xmax
                "0",  # ymin
                w_sub.name,  # ymax
                "0",  # zmin
                h_sub.name,  # zmax
                unit_comp + "/" + substrate_comp,  # 分组名
                rogers_RT5880_lossy.name,  # 材料名
            ).create(m3d)

            TRACE_COMP: str = "traces"
            traces_info: list[list[str]] = [
                [
                    "trace_0",  # 横向十字
                    (
                        unit_base_x - bracket(l_unit / Parameter("2"))
                    ).name,  # xmin
                    (
                        unit_base_x + bracket(l_unit / Parameter("2"))
                    ).name,  # xmax
                    (
                        unit_base_y - bracket(w_cross / Parameter("2"))
                    ).name,  # ymin
                    (
                        unit_base_y + bracket(w_cross / Parameter("2"))
                    ).name,  # ymax
                    h_sub.name,  # zmin
                    (h_sub + h_trace).name,  # zmax
                    unit_comp + "/" + TRACE_COMP,  # 分组名
                    copper_annealed.name,  # 材料名
                ],
                [
                    "trace_1",  # 纵向十字
                    (
                        unit_base_x - bracket(w_cross / Parameter("2"))
                    ).name,  # xmin
                    (
                        unit_base_x + bracket(w_cross / Parameter("2"))
                    ).name,  # xmax
                    (
                        unit_base_y - bracket(l_unit / Parameter("2"))
                    ).name,  # ymin
                    (
                        unit_base_y + bracket(l_unit / Parameter("2"))
                    ).name,  # ymax
                    h_sub.name,  # zmin
                    (h_sub + h_trace).name,  # zmax
                    unit_comp + "/" + TRACE_COMP,  # 分组名
                    copper_annealed.name,  # 材料名
                ],
                [
                    "trace_2",  # 下部帽子
                    (
                        unit_base_x
                        - center_x
                        + bracket(l_sub - l_hat) / Parameter("2")
                    ).name,  # xmin
                    (
                        unit_base_x
                        - center_x
                        + bracket(l_sub - l_hat) / Parameter("2")
                        + l_hat
                    ).name,  # xmax
                    (
                        unit_base_y
                        - center_y
                        + bracket(w_sub - w_unit) / Parameter("2")
                    ).name,  # ymin
                    (
                        unit_base_y
                        - center_y
                        + bracket(w_sub - w_unit) / Parameter("2")
                        + w_hat
                    ).name,  # ymax
                    h_sub.name,  # zmin
                    (h_sub + h_trace).name,  # zmax
                    unit_comp + "/" + TRACE_COMP,  # 分组名
                    copper_annealed.name,  # 材料名
                ],
                [
                    "trace_3",  # 上部帽子
                    (
                        unit_base_x
                        - center_x
                        + bracket(l_sub - l_hat) / Parameter("2")
                    ).name,  # xmin
                    (
                        unit_base_x
                        - center_x
                        + bracket(l_sub - l_hat) / Parameter("2")
                        + l_hat
                    ).name,  # xmax
                    (
                        unit_base_y
                        - center_y
                        + bracket(w_sub + w_unit) / Parameter("2")
                        - w_hat
                    ).name,  # ymin
                    (
                        unit_base_y
                        - center_y
                        + bracket(w_sub + w_unit) / Parameter("2")
                    ).name,  # ymax
                    h_sub.name,  # zmin
                    (h_sub + h_trace).name,  # zmax
                    unit_comp + "/" + TRACE_COMP,  # 分组名
                    copper_annealed.name,  # 材料名
                ],
                [
                    "trace_4",  # 左侧帽子
                    (
                        unit_base_x
                        - center_x
                        + bracket(l_sub - l_unit) / Parameter("2")
                    ).name,  # xmin
                    (
                        unit_base_x
                        - center_x
                        + bracket(l_sub - l_unit) / Parameter("2")
                        + w_cross
                    ).name,  # xmax
                    (
                        unit_base_y
                        - center_y
                        + bracket(w_sub - l_hat) / Parameter("2")
                    ).name,  # ymin
                    (
                        unit_base_y
                        - center_y
                        + bracket(w_sub - l_hat) / Parameter("2")
                        + l_hat
                    ).name,  # ymax
                    h_sub.name,  # zmin
                    (h_sub + h_trace).name,  # zmax
                    unit_comp + "/" + TRACE_COMP,  # 分组名
                    copper_annealed.name,  # 材料名
                ],
                [
                    "trace_5",  # 右侧帽子
                    (
                        unit_base_x
                        - center_x
                        + bracket(l_sub + l_unit) / Parameter(2)
                        - w_cross
                    ).name,  # xmin
                    (
                        unit_base_x
                        - center_x
                        + bracket(l_sub + l_unit) / Parameter(2)
                    ).name,  # xmax
                    (
                        unit_base_y
                        - center_y
                        + bracket(w_sub - l_hat) / Parameter("2")
                    ).name,  # ymin
                    (
                        unit_base_y
                        - center_y
                        + bracket(w_sub - l_hat) / Parameter("2")
                        + l_hat
                    ).name,  # ymax
                    h_sub.name,  # zmin
                    (h_sub + h_trace).name,  # zmax
                    unit_comp + "/" + TRACE_COMP,  # 分组名
                    copper_annealed.name,  # 材料名
                ],
            ]
            traces: list[Brick] = []
            for j in range(len(traces_info)):
                traces.append(Brick(*traces_info[j]).create(m3d))

            for j in range(len(traces_info) - 1, 0, -1):
                traces[j - 1].add(m3d, traces[j])

            # 画两条辅助线帮助debug
            # guideline_length = float(l_sub.expression)
            # curves.Line(
            #     f"line_x_{i}",
            #     f"curve_{i}",
            #     Parameter(0),
            #     Parameter(0),
            #     Parameter(guideline_length),
            #     Parameter(0),
            # ).create(m3d)
            # curves.Line(
            #     f"line_y_{i}",
            #     f"curve_{i}",
            #     Parameter(0),
            #     Parameter(0),
            #     Parameter(0),
            #     Parameter(guideline_length),
            # ).create(m3d)

            unit_count += 1
            if unit_count >= 1:
                pass
                # break

            Plot.reset_view(m3d)
            pass  # 占位行，用于调试，循环在此结束。

    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    #######################################
    # region 上方喇叭天线建模
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
    horn_up_WCS = (
        WCS(
            "horn_up_WCS",  # 坐标系名称
            "0",  # normal_x
            "0",  # normal_y
            "-1",  # normal_z
            (l_sub * Parameter(ARRAY_SIZE[0] / 2)).name,  # origin_x
            (w_sub * Parameter(ARRAY_SIZE[1] / 2)).name,  # origin_y
            (waveguide_height + horn_length + horn_gap).name,  # origin_z
            "1",  # uVector_x
            "0",  # uVector_y
            "0",  # uVector_z
        )
        .set_to_current(m3d)
        .store(m3d)
    )
    horn_up_comp = "horn_up"

    solid1 = Brick(
        "solid1",  # 实体名
        (waveguide_width / Parameter(-2)).name,  # xmin
        (waveguide_width / Parameter(2)).name,  # xmax
        (waveguide_height / Parameter(-2)).name,  # ymin
        (waveguide_height / Parameter(2)).name,  # ymax
        "0",  # zmin
        "10.92",  # zmax
        horn_up_comp,  # 分组名
        material.PEC_,  # 材料名
    ).create(m3d)

    # 选择顶面
    tp.pick_face_from_id(m3d, solid1, 1)

    solid2 = p2s.Extrude(
        "solid2",
        horn_up_comp,
        "PEC",
        properties={
            "Mode": ' "Picks"',
            "Height": ' "horn_length"',
            "Twist": ' "0.0"',
            "Taper": ' "taper_angle"',
            "UsePicksForHeight": ' "False"',
            "DeleteBaseFaceSolid": ' "False"',
            "ClearPickedFace": ' "True"',
        },
    ).create_from_attributes(m3d)
    solid1.add(m3d, solid2)

    # pick face
    tp.pick_face_from_id(m3d, solid1, 5)
    tp.pick_face_from_id(m3d, solid1, 8)
    so.advanced_shell(m3d, solid1, "Outside", wall_thickness)

    # pick end point
    tp.clear_all_picks(m3d)
    tp.pick_end_point_from_id(m3d, solid1, 16)
    tp.pick_end_point_from_id(m3d, solid1, 15)
    tp.pick_end_point_from_id(m3d, solid1, 14)

    port1 = Port(
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
    ).create_from_attributes(m3d)

    # clear picks
    tp.clear_all_picks(m3d)

    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    #######################################
    # region 下方喇叭天线建模
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

    horn_down_WCS = (
        WCS(
            "horn_up_WCS",  # 坐标系名称
            "0",  # normal_x
            "0",  # normal_y
            "1",  # normal_z
            (l_sub * Parameter(ARRAY_SIZE[0] / 2)).name,  # origin_x
            (w_sub * Parameter(ARRAY_SIZE[1] / 2)).name,  # origin_y
            (-waveguide_height - horn_length - horn_gap).name,  # origin_z
            "1",  # uVector_x
            "0",  # uVector_y
            "0",  # uVector_z
        )
        .set_to_current(m3d)
        .store(m3d)
    )
    horn_down_comp = component.Component("horn_down")

    solid1_down = Brick(
        "solid1",  # 实体名
        (waveguide_width / Parameter(-2)).name,  # xmin
        (waveguide_width / Parameter(2)).name,  # xmax
        (waveguide_height / Parameter(-2)).name,  # ymin
        (waveguide_height / Parameter(2)).name,  # ymax
        "0",  # zmin
        "10.92",  # zmax
        horn_down_comp.name,  # 分组名
        material.PEC_,  # 材料名
    ).create(m3d)

    # 选择顶面
    tp.pick_face_from_id(m3d, solid1_down, 1)
    solid2_down = p2s.Extrude(
        "solid2",
        horn_down_comp.name,
        "PEC",
        properties={
            "Mode": ' "Picks"',
            "Height": ' "horn_length"',
            "Twist": ' "0.0"',
            "Taper": ' "taper_angle"',
            "UsePicksForHeight": ' "False"',
            "DeleteBaseFaceSolid": ' "False"',
            "ClearPickedFace": ' "True"',
        },
    ).create_from_attributes(m3d)
    solid1_down.add(m3d, solid2_down)

    # pick face
    tp.pick_face_from_id(m3d, solid1_down, 5)
    tp.pick_face_from_id(m3d, solid1_down, 8)
    so.advanced_shell(m3d, solid1_down, "Outside", wall_thickness)

    # pick end point
    tp.pick_end_point_from_id(m3d, solid1_down, 16)
    tp.pick_end_point_from_id(m3d, solid1_down, 15)
    tp.pick_end_point_from_id(m3d, solid1_down, 13)

    # define port:
    port2 = Port(
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
    ).create_from_attributes(m3d)

    # clear picks
    tp.clear_all_picks(m3d)

    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    #######################################
    # region reset view
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
    WCS.activate(m3d, "global")
    Plot.reset_view(m3d)

    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    #######################################
    # region 边界条件
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

    bg = solver.Background(
        attributes={"Type": '"normal"'}, Type='"normal"'
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

    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    #######################################
    # region 求解器设置
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

    units = _global.Units().define(m3d)
    solver.hf.define_frequency_range(m3d, fmin, fmax)
    _global.change_solver_type(m3d, "HF Time Domain")

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
            "UseParallelization": ' "True"',
            "MaximumNumberOfThreads": ' "64"',
            "MaximumNumberOfCPUDevices": ' "1"',
            "RemoteCalculation": ' "False"',
            "UseDistributedComputing": ' "False"',
            "MaxNumberOfDistributedComputingPorts": ' "64"',
            "DistributeMatrixCalculation": ' "True"',
            "MPIParallelization": ' "False"',
            "AutomaticMPI": ' "False"',
            "ConsiderOnly0D1DResultsForMPI": ' "False"',
            "HardwareAcceleration": ' "True"',
            "MaximumNumberOfGPUs": ' "1"',
        }
    ).create_from_attributes(m3d)

    # 求解前保存
    proj.save(fullname)

    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    #######################################
    # region 求解
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

    m3d.start_solver()
    proj.save()

    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    #######################################
    # region
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

    time_all_end = time.time()
    time_all_interval = time_all_end - time_all_start
    logger.info("Total run time: %s", common.time_to_string(time_all_interval))

    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    pass
