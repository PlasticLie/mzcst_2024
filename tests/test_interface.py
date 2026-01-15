import logging
import math
import os
import sys
import time

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

    new_env = mz.interface.DesignEnvironment()

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
    # region 打开已有的项目
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

    PROJECT_ABSOLUTE_PATH: str = r"D:\CST-2024-local\fss-rumpf-local"
    filename: str = "flat-demo-20260112-175322.cst"
    fullname: str = os.path.join(PROJECT_ABSOLUTE_PATH, filename)

    envs[-1].open_project(fullname)

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
