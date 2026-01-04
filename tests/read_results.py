"""测试python读取cst仿真结果"""

import logging
import math
import os
import sys
import time

import matplotlib.pyplot as plt
import numpy as np

import mzcst_2024 as mz
from mzcst_2024 import common

if __name__ == "__main__":

    #######################################
    # region 开始计时
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

    time_all_start: float = time.perf_counter()

    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    #######################################
    # region 设置
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

    time_stamps: list[float] = [time_all_start]
    current_time: str = common.current_time_string()

    CURRENT_PATH: str = os.path.dirname(
        os.path.abspath(__file__)
    )  # 获取当前py文件所在文件夹
    PARENT_PATH: str = os.path.dirname(CURRENT_PATH)

    results_demo_path = os.path.join(
        PARENT_PATH, "cst-projects\\cst-results-demos"
    )

    # 阶段计时
    time_stamps.append(time.perf_counter())

    LOG_PATH: str = os.path.join(PARENT_PATH, "logs")
    LOG_FILE_NAME: str = f"read-results-demo-{current_time}.log"
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

    time_stamps.append(time.perf_counter())
    logger.info(
        "warm up: %s",
        common.time_to_string(time_stamps[-1] - time_stamps[-2]),
    )
    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    #######################################
    # region 文件处理
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

    project_path = os.path.join(results_demo_path, "Dual Patch Antenna.cst")
    project = mz.results.ProjectFile(
        filepath=project_path, allow_interactive=True
    )
    s11 = project.get_3d().get_result_item(r"1D Results\S-Parameters\S1,1")
    print("S11 Result Item of Dual Patch Antenna.cst:")
    print(s11)
    s11_xdata = s11.get_xdata()
    s11_data = s11.get_data()
    print("S11 data Item of Dual Patch Antenna.cst:")
    print(s11_data)

    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    #######################################
    # region 官方案例1
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

    eg1_path = os.path.join(results_demo_path, "project.cst")
    eg1 = mz.results.ProjectFile(eg1_path, allow_interactive=True)
    eg1_s11 = eg1.get_3d().get_result_item(r"1D Results\S-Parameters\S1,1")
    eg1_s11_data = eg1_s11.get_data()
    print(eg1_s11_data)

    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    #######################################
    # region 官方案例2
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
    eg2_path = os.path.join(results_demo_path, "Antenna Reflector Assembly.cst")
    eg2 = mz.results.ProjectFile(eg2_path, allow_interactive=True)
    eg2_tree_items = eg2.get_schematic().get_tree_items()
    print("eg2_tree_items:")
    print(eg2_tree_items)
    print("eg2 subprojects:")
    print(eg2.list_subprojects())
    eg2_subproject = eg2.load_subproject("Tasks\\SP1")
    eg2_sub1_tree_items = eg2_subproject.get_3d().get_tree_items()
    print("eg2_sub1_tree_items:")
    print(eg2_sub1_tree_items)
    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    #######################################
    # region 官方案例3
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
    eg3_path = os.path.join(results_demo_path, "VCO Parameter Sweep.cst")
    eg3 = mz.results.ProjectFile(eg3_path, allow_interactive=True)
    eg3_schematic = eg3.get_schematic()
    eg3_schematic_all_runids = eg3_schematic.get_all_run_ids()
    print("eg3_schematic_all_runids:")
    print(eg3_schematic_all_runids)
    eg3_schematic_runid_port1 = eg3_schematic.get_run_ids('Tasks\\Sweep Tuning Voltage\\Tran1\\TD Currents\\Port1')
    print("eg3_schematic_runid_port1:")
    print(eg3_schematic_runid_port1)
    # port1 = eg3_schematic.get_result_item('Tasks\\Sweep Tuning Voltage\\Tran1\\TD Currents\\Port1',5)
    port1 = eg3_schematic.get_result_item('Tasks\\Sweep Tuning Voltage\\Tran1\\TD Currents\\Port1',0)
    print(f"port1 length: {port1.length}")
    print("eg3_schematic.get_parameter_combination(4):")
    print(eg3_schematic.get_parameter_combination(4))
    print("eg3_schematic.get_parameter_combination(5):")
    print(eg3_schematic.get_parameter_combination(5))
    f = eg3_schematic.get_result_item('Tasks\\Sweep Tuning Voltage\\Tran1\\PP1\\0D\\Oscillation Frequency',5)
    print(f"f.run_id: {f.run_id}")
    print(f"f.get_parameter_combination(): {f.get_parameter_combination()}")
    tree_item = 'Tasks\\Sweep Tuning Voltage\\Tran1\\PP1\\0D\\Oscillation Frequency'
    x = []
    y = []
    run_ids = eg3_schematic.get_run_ids(tree_item,skip_nonparametric=True)
    for run in run_ids:
        result = eg3_schematic.get_result_item(tree_item,run)
        x.append(result.get_parameter_combination()['VTUNE'])
        y.append(result.get_ydata())

    for i in range(len(x)):
        print (x[i], y[i])
    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
    pass
