# -*- coding: utf-8 -*-
import logging
import sys
import time

import tomli
import tomli_w

STABLE_VERSION = [
    "0.1.0",
]


def version(tag: str = "test") -> str:
    current_time = time.localtime()
    match tag:
        case "test":
            version_name = f"{current_time.tm_year:04d}.{current_time.tm_mon:02d}.{current_time.tm_mday:02d}.{current_time.tm_hour:02d}{current_time.tm_min:02d}"
        case "stable":
            version_name = f"{current_time.tm_year:04d}.{current_time.tm_mon:02d}.{current_time.tm_mday:02d}"
        case _:
            raise ValueError(
                f"Unknown tag: {tag}, expected 'test' or 'stable'."
            )
    return version_name


if __name__ == "__main__":

    LOG_LEVEL = logging.INFO
    FMT = "%(asctime)s.%(msecs)-3d %(name)s: %(levelname)s: %(message)s"
    DATEFMT = r"%Y-%m-%d %H:%M:%S"
    LOG_FORMATTER = logging.Formatter(FMT, DATEFMT)
    logging.basicConfig(
        format=FMT, datefmt=DATEFMT, level=LOG_LEVEL, force=True
    )

    logger = logging.getLogger(__name__)

    argc = len(sys.argv)
    argv = sys.argv

    current_version = version(argv[1] if argc > 1 else "test")

    with open("pyproject.toml", "rb") as f:
        meta = tomli.load(f)
        meta["project"]["version"] = current_version

    with open("pyproject.toml", "wb") as f2:
        tomli_w.dump(meta, f2)

    logger.info("%s", f"Version updated to {current_version} in pyproject.toml")
    pass
