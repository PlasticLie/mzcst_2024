"""本文件用于删除python缓存文件和日志文件，包括：

.mypy_cache\n
__pycache__\n


"""

import logging

# python 标准库
import os
import pathlib
import shutil
import sys
import zipfile

if __name__ == "__main__":

    #######################################
    # region 日志设置
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

    LOG_LEVEL = logging.INFO
    FMT = "%(asctime)s.%(msecs)-3d %(name)s: %(levelname)s: %(message)s"
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
    # region 命令行参数和目标路径处理
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

    CURRENT_PATH: str = os.path.dirname(os.path.abspath(__file__))
    logger.debug('location of current file: "%s"', CURRENT_PATH)
    PARENT_PATH: str = os.path.dirname(CURRENT_PATH)

    argc = len(sys.argv)
    if argc > 1:
        TARGET_PATH = sys.argv[1]
    else:
        TARGET_PATH = PARENT_PATH

    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    #######################################
    # region 删除缓存文件
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

    pycache_confirm = input("是否删除 __pycache__ 缓存? (y/[n])")
    if pycache_confirm.lower() == "y":
        logger.info("删除 __pycache__ 缓存")
        for p in pathlib.Path(TARGET_PATH).rglob("__pycache__"):
            if ".conda" in str(p):
                logger.info('skip directory "%s"', p)
                continue
            logger.debug('__pycache__ path: "%s"', p)
            for p2 in p.glob("*.pyc"):
                # logger.debug('deleting file "%s"', p2)
                os.remove(p2)
                logger.info('deleted file: "%s"', p2)
            logger.info('__pycache__ cleared: "%s"', p)
    else:
        logger.info("不删除 __pycache__ 缓存")

    debug_log_confirm = input("是否删除 debug.log文件? (y/[n])")
    if debug_log_confirm == "y":
        logger.info("删除 debug.log文件")
        for p in pathlib.Path(TARGET_PATH).rglob("debug.log"):
            os.remove(p)
            logger.info('debug.log deleted: "%s"', p)
    else:
        logger.info("不删除 debug.log 日志。")

    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
    logger.info("脚本运行完毕.")

    pass
