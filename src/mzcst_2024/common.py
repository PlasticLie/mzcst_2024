"""实现一些通用的功能。"""

__all__: list[str] = [
    "NEW_LINE",
    "OPERATION_SUCCESS",
    "OPERATION_FAILED",
    "quoted",
]

import logging
import math
import os
import sys
import time
import typing
from enum import Enum
from re import L

NEW_LINE: str = "\n"
OPERATION_SUCCESS: str = r"Operation Success: %s"
OPERATION_FAILED: str = r"Operation Failed: %s"

_logger = logging.getLogger(__name__)


def quoted(s: str) -> str:
    """给字符串首尾各添加一个双引号。

    Args:
        s (str): 输入的字符串。

    Returns:
        str: 输出的字符串。
    """
    return '"' + s + '"'


def create_folder(path: str):
    """Create a folder in the specified `path` if `path` does not exist.

    Parameters
    ----------
    path : str
        path string.
    """
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        _logger.info('New folder "%s" created.', path)
    else:
        _logger.info('Folder "%s" exists.', path)

    return


def delete_all_files_in_folder(path: str) -> None:
    """删除文件夹内的所有文件。

    Args:
        path (str): 文件夹路径。

    Returns:
        None
    """
    abs_path = os.path.abspath(path)
    file_list = os.listdir(abs_path)
    for file in file_list:
        file_path = os.path.join(abs_path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
            _logger.info('File "%s" deleted.', file_path)
    return


def current_time_string():
    current_time = time.localtime()
    time_str = "%04d%02d%02d-%02d%02d%02d" % (
        current_time.tm_year,
        current_time.tm_mon,
        current_time.tm_mday,
        current_time.tm_hour,
        current_time.tm_min,
        current_time.tm_sec,
    )
    time_str_ = (
        f"{current_time.tm_year:04d}{current_time.tm_mon:02d}"
        + f"{current_time.tm_mday:02d}-{current_time.tm_hour:02d}"
        + f"{current_time.tm_min:02d}{current_time.tm_sec:02d}"
    )
    return time_str_


class Log_tag(Enum):
    INFO = 1
    WARNING = 2
    ERROR = 3


def print_log(*objects, sep=" ", end="\n", file_ptr=sys.stdout):
    print(*objects, sep=sep, end=end)
    if file_ptr != sys.stdout:
        print(*objects, file=file_ptr)


def calculate_time(t_s: float):
    time_interval_day = t_s // 86400
    time_interval_hour = (t_s % 86400) // 3600
    time_interval_minute = (t_s % 3600) // 60
    time_interval_second = t_s % 60
    return (
        time_interval_day,
        time_interval_hour,
        time_interval_minute,
        time_interval_second,
    )


def time_to_string(t: float) -> str:
    time_interval_day = int(t // 86400)
    time_interval_hour = int((t % 86400) // 3600)
    time_interval_minute = int((t % 3600) // 60)
    time_interval_second = t % 60
    r: str = ""
    if time_interval_day != 0:
        r = f"{time_interval_day:d}:{time_interval_hour:d}:{time_interval_minute:d}:{time_interval_second:.3f}"
    elif time_interval_hour != 0:
        r = f"{time_interval_hour:d}:{time_interval_minute:d}:{time_interval_second:.3f}"
    elif time_interval_minute != 0:
        r = f"{time_interval_minute:d}:{time_interval_second:.3f}"
    else:
        r = f"{time_interval_second:.3f}"
    return r


def progress_bar(name: str, current: int, total: int):
    SCALE: int = 50
    STEP: float = 100 / SCALE
    percent: float = current / total * 100
    num_bars: int = int(percent / STEP)
    num_empty: int = SCALE - num_bars
    digits: int = int(math.log10(abs(total))) + 1
    f_i: str = r"{: >" + str(digits) + r"d}"
    title: str = name + " " + f_i + " of " + f_i + " ({: >5.1f}%): ["
    print("\r", end="")
    print(
        title.format(current, total, percent),
        "█" * (num_bars) + " " * (num_empty),
        "]",
        end="",
        sep="",
    )
    sys.stdout.flush()
    return


def time_decorator(func):
    def wrapper(*args, **kwargs):
        t_start = time.perf_counter()
        result = func(*args, **kwargs)
        t_end = time.perf_counter()
        _logger.info(
            "%s",
            f"{func.__name__} execution time: {time_to_string(t_end-t_start)}",
        )
        return result

    return wrapper


class clock:
    DEFAULT_FMT: str = r"[{elapsed:0.8f}s] {name}({args}) -> {result}"

    def __init__(self, fmt: str = DEFAULT_FMT):
        self.fmt = fmt

    def __call__(self, func) -> typing.Any:  # <3>
        def time_to_string(t: float) -> str:
            time_interval_day = int(t // 86400)
            time_interval_hour = int((t % 86400) // 3600)
            time_interval_minute = int((t % 3600) // 60)
            time_interval_second = t % 60
            r: str = ""
            if time_interval_day != 0:
                r = f"{time_interval_day:d}:{time_interval_hour:d}:{time_interval_minute:d}:{time_interval_second:.3f}"
            elif time_interval_hour != 0:
                r = f"{time_interval_hour:d}:{time_interval_minute:d}:{time_interval_second:.3f}"
            elif time_interval_minute != 0:
                r = f"{time_interval_minute:d}:{time_interval_second:.3f}"
            else:
                r = f"{time_interval_second:.3f}"
            return r

        def wrapper(*args, **kwargs):
            t_start = time.perf_counter()
            result = func(*args, **kwargs)
            t_end = time.perf_counter()
            elapsed = t_end - t_start
            _logger.info(
                "%s",
                f"{func.__name__} execution time: {time_to_string(t_end-t_start)}",
            )
            print(
                f"{func.__name__} execution time: {time_to_string(t_end-t_start)}",
            )
            return result

        return wrapper

    @staticmethod
    def shit():
        return 0


if __name__ == "__main__":
    # create_folder("folder_demo")
    # print_log("1", "hello")
    # print(
    #     "Total run time: %d:%d:%d:%.3f" % (calculate_time(60.357)),
    # )
    print(time_to_string(88560.389))

    @time_decorator
    def slow_func():
        time.sleep(1)

    slow_func()
