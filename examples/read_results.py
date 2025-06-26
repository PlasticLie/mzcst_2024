"""测试python读取cst仿真结果"""

import logging
import math
import os
import sys
import time

import matplotlib.pyplot as plt
import mzcst_2024 as mz
import numpy as np
from mzcst import common

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
    LOG_FILE_NAME: str = f"conformal-Rumpf-demo-{current_time}.log"
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
    print(s11)
    s11_xdata = s11.get_xdata()
    s11_data = s11.get_data()
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

    pass
