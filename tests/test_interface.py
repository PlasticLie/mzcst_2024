import logging
import math
import os
import sys
import time

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

import mzcst_2024 as mz

if __name__ == "__main__":
    timestamps: list[float] = [time.perf_counter()]

    #######################################
    # region 日志设置
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

    LOG_LEVEL = logging.INFO
    FMT = "%(asctime)s.%(msecs)-3d %(name)s %(lineno)4d: %(levelname)s: %(message)s"
    DATEFMT = r"%Y-%m-%d %H:%M:%S"
    LOG_FORMATTER = logging.Formatter(FMT, DATEFMT)
    logging.basicConfig(
        format=FMT, datefmt=DATEFMT, level=LOG_LEVEL, force=True
    )

    logger = logging.getLogger(__name__)
    logger.info("Start logging: %s", __file__)

    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    #######################################
    # region 创建新环境
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

    envs: list[mz.interface.DesignEnvironment] = []

    new_env = mz.interface.DesignEnvironment.connect_to_any_or_new()

    version_info = mz.interface.DesignEnvironment.version()
    logger.info("CST Version:")
    print(version_info)

    logger.info("Created new DesignEnvironment with PID: %s", f"{new_env.pid_}")
    logger.info("CST Version: %s", new_env.version())
    logger.info("Is in quiet mode: %s", new_env.in_quiet_mode_)

    envs.append(new_env)

    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    #######################################
    # region 绘图设置
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

    # 时间戳记录
    timestamps.append(time.perf_counter())
    # 清空已打开的图形
    plt.close("all")

    # 存储图形的容器
    figs: list[plt.Figure] = []
    axs: list[Axes3D] = []

    # 字体设置
    font_settings = {
        "sans-serif": "Arial, SimHei, sans-serif",
        "serif": "Times New Roman, SimSun, serif",
    }
    if sys.platform.startswith("linux"):
        logger.info("system platform: Linux")
    elif sys.platform.startswith("darwin"):
        logger.info("system platform: macOS")
    elif sys.platform.startswith("win32"):
        logger.info("system platform: Windows")
        plt.rcParams["font.family"] = font_settings["sans-serif"]
        logger.info(
            "font family of matplotlib is set as: %s",
            font_settings["sans-serif"],
        )
    # 是否绘图
    DRAW_FIGURES: dict[int | str, bool] = {
        0: True,  # 总开关
        "s11_magnitude": True,
        "s21_magnitude": True,
        "keep": True,
    }
    # 是否建模
    BUILD_MODEL: bool = True

    plt.ion()

    timestamps.append(time.perf_counter())
    logger.info(
        "plot config: %s",
        mz.common.time_to_string(timestamps[-1] - timestamps[-2]),
    )
    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    #######################################
    # region 打开已有的项目
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

    PROJECT_ABSOLUTE_PATH: str = r"D:\CST-2024-local\cst-results-demos"
    filename: str = "Dual Patch Antenna.cst"
    fullname: str = os.path.join(PROJECT_ABSOLUTE_PATH, filename)

    envs[-1].open_project(fullname)
    flat_demo_project = envs[-1].active_project()
    flat_demo_result = mz.results.ProjectFile(fullname, allow_interactive=True)
    flat_demo_3d = flat_demo_result.get_3d()
    parameters = flat_demo_3d.get_parameter_combination(0)
    tree_items = flat_demo_3d.get_tree_items()
    s11 = flat_demo_3d.get_result_item("1D Results\\S-Parameters\\S1,1")
    s21 = flat_demo_3d.get_result_item("1D Results\\S-Parameters\\S2,1")

    s11_x = np.array(s11.xdata)
    s11_y = np.array(s11.ydata)
    s11_y_db20 = 20 * np.log10(np.abs(s11_y))

    s21_x = np.array(s21.xdata)
    s21_y = np.array(s21.ydata)
    s21_y_db20 = 20 * np.log10(np.abs(s21_y))

    # 创建图形和坐标轴
    if DRAW_FIGURES[0]:
        figs.append(plt.figure("S 参数", figsize=(10, 10)))
        axs.append(figs[-1].add_subplot(1, 1, 1))
        axs[-1].set_title("S 参数")
        axs[-1].set_xlabel("频率 (GHz)")
        axs[-1].set_ylabel("S 参数幅度 (dB)")

    if DRAW_FIGURES[0] and DRAW_FIGURES["s11_magnitude"]:
        axs[-1].plot(s11_x, s11_y_db20, label="S11")

    if DRAW_FIGURES[0] and DRAW_FIGURES["s21_magnitude"]:
        axs[-1].plot(s21_x, s21_y_db20, label="S21")

    if DRAW_FIGURES["keep"]:
        logger.info("KEEP FIGURES is True, blocking show...")
        plt.show(block=True)

    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    #######################################
    # region 结束
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

    timestamps.append(time.perf_counter())
    elapsed = timestamps[-1] - timestamps[0]
    logger.info(
        "Finished %s, total elapsed time: %s.",
        __file__,
        mz.common.time_to_string(elapsed),
    )

    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
