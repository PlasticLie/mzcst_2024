"""参考TAP论文：

Zhaohui WEI, Zhao ZHOU, Peng WANG, Jian REN, Yingzeng YIN, Gert Frolund PEDERSEN,
Ming SHEN. Fully Automated Design Method Based on Reinforcement Learning and
Surrogate Modeling for Antenna Array Decoupling[J]. IEEE transactions on
antennas and propagation, 2023,71(1): 660-671.

https://ieeexplore.ieee.org/document/9953971
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
from mzcst_2024 import Parameter

if __name__ == "__main__":
    #######################################
    # region 开始计时
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

    time_all_start: float = time.perf_counter()
    current_time: str = mz.common.current_time_string()

    CURRENT_PATH: str = os.path.dirname(
        os.path.abspath(__file__)
    )  # 获取当前py文件所在文件夹
    PARENT_PATH: str = os.path.dirname(CURRENT_PATH)

    FILE_NAME_PREFIX: str = "decouple-metasurface-"

    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    #######################################
    # region 日志设置
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

    LOG_PATH: str = os.path.join(CURRENT_PATH, "logs")
    LOG_FILE_NAME: str = f"{FILE_NAME_PREFIX}-{current_time}.log"
    LOG_LEVEL = logging.INFO
    FMT = "%(asctime)s.%(msecs)-3d %(name)s - %(levelname)s - %(message)s"
    DATEFMT = r"%Y-%m-%d %H:%M:%S"
    LOG_FORMATTER = logging.Formatter(FMT, DATEFMT)
    mz.common.create_folder(LOG_PATH)
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

    PROJECT_ABSOLUTE_PATH: str = r"D:\CST-2024-local\patch-decouple-local"
    mz.common.create_folder(PROJECT_ABSOLUTE_PATH)
    os.startfile(PROJECT_ABSOLUTE_PATH)
    filename: str = f"{FILE_NAME_PREFIX}-{current_time}.cst"
    fullname: str = os.path.join(PROJECT_ABSOLUTE_PATH, filename)
    logger.info('Project full path: "%s"', fullname)
    design_env = mz.interface.DesignEnvironment()
    proj = design_env.new_mws()
    m3d = proj.model3d
    logger.info("CST started.")

    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    #######################################
    # region CST参数
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

    # 环境
    fmin: Parameter = Parameter("fmin", "3", "频带下限(GHz)").store(m3d)
    fmax: Parameter = Parameter("fmax", "4", "频带上限(GHz)").store(m3d)
    fcenter = ((fmin + fmax) / Parameter(2)).rename("fcenter").store(m3d)
    wavelength = (
        (Parameter("3e8") / fcenter / Parameter("1e6"))
        .rename("wavelength")
        .re_describe("中心频率波长")
        .store(m3d)
    )
    # theta: Parameter = Parameter("theta", "0", "入射俯仰角").store(m3d)
    # phi: Parameter = Parameter("phi", "0", "入射方位角").store(m3d)

    # 接地
    l_gnd = Parameter("l_gnd", "200", "地板长度(x)").store(m3d)
    w_gnd = Parameter("w_gnd", "200", "地板宽度(y)").store(m3d)
    h_gnd = Parameter("h_gnd", "0.5", "地板厚度").store(m3d)

    # 天线单元
    s_p = Parameter("s_p", "1.5", "贴片间距").store(m3d)

    l_p = Parameter("l_p", "30.5", "贴片长度").store(m3d)
    w_p = Parameter("w_p", "l_p", "贴片宽度").store(m3d)

    l_s = Parameter("l_s", "21.2", "槽线长度").store(m3d)
    w_s = Parameter("w_s", "1.4", "槽线宽度").store(m3d)
    l = Parameter("l", "13", "槽线间距").store(m3d)

    l_f = Parameter("l_f", "1.8").store(m3d)
    w_f = Parameter("w_f", "4.15").store(m3d)

    h_2 = Parameter("h_2", "4.5", "天线到地板的距离").store(m3d)
    edge_spacing = Parameter("edge_spacing", "10", "基板四周留白").store(m3d)

    l_unit = Parameter("l_unit", "l_p + s_p", "单元基板长度").store(m3d)
    w_unit = Parameter("w_unit", "l_unit", "单元基板长度").store(m3d)

    l_sub = Parameter(
        "l_sub", "l_unit * 2 + edge_spacing * 2", "单元基板长度"
    ).store(m3d)
    w_sub = Parameter(
        "w_sub", "w_unit + edge_spacing * 2", "单元基板宽度"
    ).store(m3d)
    h_sub = Parameter("h_sub", "0.5", "基板厚度").store(m3d)
    h_trace = Parameter("h_trace", "0.035", "导线厚度").store(m3d)

    # 馈电
    feed_x = (w_sub / Parameter(2)).rename("feed_x").store(m3d)
    feed_y = ((l_sub - l_p) / Parameter(2) + l_f).rename("feed_y").store(m3d)
    r_in = Parameter("r_in", "1.27 / 2", "馈电端口内径(mm)").store(m3d)
    r_out = Parameter("r_out", "6 / 2", "馈电端口外径(mm)").store(m3d)
    l_feed = Parameter("l_feed", "4", "馈电端口长度(mm)").store(m3d)
    d = Parameter("d", "1", "馈电位置到贴片下沿的距离").store(m3d)

    # 超表面（需要优化的参数）
    n_x = Parameter("n_x", "13", "超表面单元数目X").store(m3d)
    n_y = Parameter("n_y", "4", "超表面单元数目Y").store(m3d)
    l_m = Parameter("l_m", "18", "超表面单元长度").store(m3d)
    w_m = Parameter("w_m", "6", "超表面单元宽度").store(m3d)
    s_x = Parameter("s_x", "9", "超表面单元间距X").store(m3d)
    s_y = Parameter("s_y", "21", "超表面单元间距Y").store(m3d)

    h_1 = Parameter("h_1", "7.5", "天线到超表面的距离").store(m3d)

    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    #######################################
    # region 材料定义
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
    copper_annealed = mz.material.Material(
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

    F4B_substrate = mz.material.Material(
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
    ).create(m3d)

    coaxial_dielectric = mz.material.Material(
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
    ).create(m3d)

    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    #######################################
    # region CST 天线建模
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

    feed_comp = mz.component.Component("feed").create(m3d)
    antenna_comp = mz.component.Component("antenna").create(m3d)

    ground = mz.shapes.Brick(
        "ground",
        f"{0}",
        f"{l_gnd}",
        f"{0}",
        f"{w_gnd}",
        f"{0}",
        f"{h_gnd}",
        f"{antenna_comp}",
        f"{copper_annealed}",
    ).create(m3d)

    sub_base = [
        (l_gnd - l_sub) / Parameter(2),
        (w_gnd - w_sub) / Parameter(2),
        h_gnd + h_2,
    ]
    sub = mz.shapes.Brick(
        "sub",
        f"{sub_base[0]}",
        f"{sub_base[0] + l_sub}",
        f"{sub_base[1]}",
        f"{sub_base[1] + w_sub}",
        f"{sub_base[2]}",
        f"{sub_base[2] + h_sub}",
        f"{antenna_comp}",
        f"{F4B_substrate}",
    ).create(m3d)

    patch_1_base = [
        sub_base[0] + edge_spacing + s_p / Parameter(2),
        sub_base[1] + edge_spacing + s_p / Parameter(2),
        sub_base[2] + h_sub,
    ]
    patch_1 = mz.shapes.Brick(
        "patch_1",
        f"{patch_1_base[0]}",
        f"{patch_1_base[0] + l_p}",
        f"{patch_1_base[1]}",
        f"{patch_1_base[1] + w_p}",
        f"{patch_1_base[2]}",
        f"{patch_1_base[2] + h_trace}",
        f"{antenna_comp}",
        f"{copper_annealed}",
    ).create(m3d)
    patch_1_slot_1 = mz.shapes.Brick(
        "patch_1_slot_1",
        f"{patch_1_base[0] + (l_p - l - w_s) / Parameter(2)}",
        f"{patch_1_base[0] + (l_p - l + w_s) / Parameter(2)}",
        f"{patch_1_base[1]}",
        f"{patch_1_base[1] + l_s}",
        f"{patch_1_base[2]}",
        f"{patch_1_base[2] + h_trace}",
        f"{antenna_comp}",
        f"{copper_annealed}",
    ).create(m3d)
    patch_1_slot_2 = mz.shapes.Brick(
        "patch_1_slot_2",
        f"{patch_1_base[0] + (l_p + l - w_s) / Parameter(2)}",
        f"{patch_1_base[0] + (l_p + l + w_s) / Parameter(2)}",
        f"{patch_1_base[1]}",
        f"{patch_1_base[1] + l_s}",
        f"{patch_1_base[2]}",
        f"{patch_1_base[2] + h_trace}",
        f"{antenna_comp}",
        f"{copper_annealed}",
    ).create(m3d)
    patch_1.subtract(m3d, patch_1_slot_1)
    patch_1.subtract(m3d, patch_1_slot_2)

    feed_1_base = [
        patch_1_base[0] + l_p / Parameter(2),
        patch_1_base[1] + d,
    ]
    feed_1 = mz.shapes.Cylinder(
        name="feed_1",
        component=f"{feed_comp}",
        material=f"{mz.material.PEC}",
        axis="z",
        r_in=f"{0}",
        r_out=f"{r_in}",
        center_1=f"{feed_1_base[0]}",
        center_2=f"{feed_1_base[1]}",
        range_1=f"{-l_feed}",
        range_2=f"{patch_1_base[2]}",
    ).create(m3d)
    feed_1_dielectric = mz.shapes.Cylinder(
        name="feed_1_dielectric",
        component=f"{feed_comp}",
        material=f"{coaxial_dielectric}",
        axis="z",
        r_in=f"{r_in}",
        r_out=f"{r_out}",
        center_1=f"{feed_1_base[0]}",
        center_2=f"{feed_1_base[1]}",
        range_1=f"{-l_feed}",
        range_2=f"{h_gnd}",
    ).create(m3d)
    feed_1_gnd = mz.shapes.Cylinder(
        name="feed_1_gnd",
        component=f"{feed_comp}",
        material=f"{mz.material.PEC}",
        axis="z",
        r_in=f"{r_out}",
        r_out=f"{r_out+h_trace}",
        center_1=f"{feed_1_base[0]}",
        center_2=f"{feed_1_base[1]}",
        range_1=f"{-l_feed}",
        range_2=f"{h_gnd}",
    ).create(m3d)

    sub.insert(m3d, feed_1)
    ground.insert(m3d, feed_1)
    ground.insert(m3d, feed_1_dielectric)
    ground.insert(m3d, feed_1_gnd)

    # 贴片2
    patch_2_base = [
        sub_base[0] + (l_sub + s_p) / Parameter(2),
        sub_base[1] + edge_spacing + s_p / Parameter(2),
        sub_base[2] + h_sub,
    ]
    patch_2 = mz.shapes.Brick(
        "patch_2",
        f"{patch_2_base[0]}",
        f"{patch_2_base[0] + l_p}",
        f"{patch_2_base[1]}",
        f"{patch_2_base[1] + w_p}",
        f"{patch_2_base[2]}",
        f"{patch_2_base[2] + h_trace}",
        f"{antenna_comp}",
        f"{copper_annealed}",
    ).create(m3d)
    patch_2_slot_1 = mz.shapes.Brick(
        "patch_2_slot_1",
        f"{patch_2_base[0] + (l_p - l - w_s) / Parameter(2)}",
        f"{patch_2_base[0] + (l_p - l + w_s) / Parameter(2)}",
        f"{patch_2_base[1]}",
        f"{patch_2_base[1] + l_s}",
        f"{patch_2_base[2]}",
        f"{patch_2_base[2] + h_trace}",
        f"{antenna_comp}",
        f"{copper_annealed}",
    ).create(m3d)
    patch_2_slot_2 = mz.shapes.Brick(
        "patch_2_slot_2",
        f"{patch_2_base[0] + (l_p + l - w_s) / Parameter(2)}",
        f"{patch_2_base[0] + (l_p + l + w_s) / Parameter(2)}",
        f"{patch_2_base[1]}",
        f"{patch_2_base[1] + l_s}",
        f"{patch_2_base[2]}",
        f"{patch_2_base[2] + h_trace}",
        f"{antenna_comp}",
        f"{copper_annealed}",
    ).create(m3d)
    patch_2.subtract(m3d, patch_2_slot_1)
    patch_2.subtract(m3d, patch_2_slot_2)

    feed_2_base = [
        patch_2_base[0] + l_p / Parameter(2),
        patch_2_base[1] + d,
    ]
    feed_2 = mz.shapes.Cylinder(
        name="feed_2",
        component=f"{feed_comp}",
        material=f"{mz.material.PEC}",
        axis="z",
        r_in=f"{0}",
        r_out=f"{r_in}",
        center_1=f"{feed_2_base[0]}",
        center_2=f"{feed_2_base[1]}",
        range_1=f"{-l_feed}",
        range_2=f"{patch_2_base[2]}",
    ).create(m3d)
    feed_2_dielectric = mz.shapes.Cylinder(
        name="feed_2_dielectric",
        component=f"{feed_comp}",
        material=f"{coaxial_dielectric}",
        axis="z",
        r_in=f"{r_in}",
        r_out=f"{r_out}",
        center_1=f"{feed_2_base[0]}",
        center_2=f"{feed_2_base[1]}",
        range_1=f"{-l_feed}",
        range_2=f"{h_gnd}",
    ).create(m3d)
    feed_2_gnd = mz.shapes.Cylinder(
        name="feed_2_gnd",
        component=f"{feed_comp}",
        material=f"{mz.material.PEC}",
        axis="z",
        r_in=f"{r_out}",
        r_out=f"{r_out+h_trace}",
        center_1=f"{feed_2_base[0]}",
        center_2=f"{feed_2_base[1]}",
        range_1=f"{-l_feed}",
        range_2=f"{h_gnd}",
    ).create(m3d)

    sub.insert(m3d, feed_2)
    ground.insert(m3d, feed_2)
    ground.insert(m3d, feed_2_dielectric)
    ground.insert(m3d, feed_2_gnd)

    # 定义端口
    mz.transformations_and_picks.pick_face_from_id(m3d, feed_1_gnd, 1)
    port1 = mz.sources_and_ports.hf.Port(
        "",
        1,
        properties={
            "NumberOfModes": '"1"',
            "AdjustPolarization": '"False"',
            "PolarizationAngle": ' "0.0"',
            "ReferencePlaneDistance": '"0"',
            "TextSize": ' "50"',
            "Coordinates": '"Picks"',
            "Orientation": '"positive"',
            "PortOnBound": '"True"',
            "ClipPickedPortToBound": ' "False"',
        },
    ).create_from_attributes(m3d)
    mz.transformations_and_picks.pick_face_from_id(m3d, feed_2_gnd, 1)
    port1 = mz.sources_and_ports.hf.Port(
        "",
        2,
        properties={
            "NumberOfModes": '"1"',
            "AdjustPolarization": '"False"',
            "PolarizationAngle": ' "0.0"',
            "ReferencePlaneDistance": '"0"',
            "TextSize": ' "50"',
            "Coordinates": '"Picks"',
            "Orientation": '"positive"',
            "PortOnBound": '"True"',
            "ClipPickedPortToBound": ' "False"',
        },
    ).create_from_attributes(m3d)
    mz.transformations_and_picks.clear_all_picks(m3d)

    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    #######################################
    # region 超表面建模
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

    metasurface_comp = mz.component.Component("metasurface").create(m3d)
    meta_unit_comp = metasurface_comp.create_sub_component(m3d, "units")
    l_meta = s_x * n_x
    w_meta = s_y * n_y
    meta_base: list[Parameter] = [
        (l_gnd - l_meta) / Parameter(2),
        (w_gnd - w_meta) / Parameter(2),
        h_gnd + h_2 + h_sub + h_1,
    ]
    meta_unit_base: list[Parameter] = [
        (s_x - w_m) / Parameter(2),
        (s_y - l_m) / Parameter(2),
        meta_base[2],
    ]

    meta_sub = mz.shapes.Brick(
        "meta_sub",
        f"{meta_base[0]}",
        f"{meta_base[0]+l_meta}",
        f"{meta_base[1]}",
        f"{meta_base[1]+w_meta}",
        f"{meta_base[2]}",
        f"{meta_base[2]+h_sub}",
        f"{metasurface_comp}",
        f"{F4B_substrate}",
    ).create(m3d)
    meta_units = [[] for _ in range(n_y.value)]

    for i in range(n_y.value):
        for j in range(n_x.value):
            x = meta_base[0] + Parameter(j) * s_x + meta_unit_base[0]
            y = meta_base[1] + Parameter(i) * s_y + meta_unit_base[1]
            meta_units[i].append(
                {
                    "top": mz.shapes.Brick(
                        f"meta_{i}_{j}_top",
                        f"{x}",
                        f"{x + w_m}",
                        f"{y}",
                        f"{y + l_m}",
                        f"{meta_unit_base[2]+h_sub}",
                        f"{meta_unit_base[2]+h_sub + h_trace}",
                        f"{meta_unit_comp}",
                        f"{copper_annealed}",
                    ).create(m3d),
                    "bottom": mz.shapes.Brick(
                        f"meta_{i}_{j}_bottom",
                        f"{x}",
                        f"{x + w_m}",
                        f"{y}",
                        f"{y + l_m}",
                        f"{meta_unit_base[2] -h_trace}",
                        f"{meta_unit_base[2]}",
                        f"{meta_unit_comp}",
                        f"{copper_annealed}",
                    ).create(m3d),
                }
            )

    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    #######################################
    # region 边界条件
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

    bg = mz.solver.Background(
        attributes={"Type": '"normal"'}, Type='"normal"'
    ).create_from_attributes(m3d)

    bd = mz.solver.Boundary(
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

    mz.plot.Plot.reset_view(m3d)

    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    #######################################
    # region 求解器设置
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

    mz.solver.hf.define_frequency_range(m3d, fmin, fmax)
    mz.change_solver_type(m3d, "HF Time Domain")

    mz.solver.hf.SolverHF(
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
            "MaximumNumberOfThreads": ' "32"',
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
    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    

    #######################################
    # region 求解器设置
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

    units = mz.Units().define(m3d)
    mz.solver.hf.define_frequency_range(m3d, fmin, fmax)
    mz.change_solver_type(m3d, "HF Time Domain")

    solver_config=mz.solver.hf.SolverHF(
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
    save_proj = True
    if save_proj:
        proj.save(fullname)

    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    #######################################
    # region 求解
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

    m3d.start_solver()
    # proj.save()

    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    #######################################
    # region
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

    time_all_end = time.time()
    time_all_interval = time_all_end - time_all_start
    logger.info("Total run time: %s", mz.common.time_to_string(time_all_interval))

    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    pass  # EOF
