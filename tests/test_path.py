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
    # region 路径测试
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

    p = mz.CSTPath("a/b/c", "d/e/f")
    logger.info("CSTPath: %s", p)
    logger.info("CSTPath parts: %s", p.parts)

    p2 = p / "g/h/i"
    logger.info("p2: %s", repr(p2))
    p3 = mz.CSTPath(p2)
    logger.info("p3: %s", repr(p3))
    logger.info("%s",f"{p3},{repr(p3)}")

    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
