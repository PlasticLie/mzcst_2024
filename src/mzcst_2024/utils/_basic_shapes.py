"""
mzcst_2024.utils._basic_shapes 的 Docstring

This module provides basic geometric shapes for use in the mzcst_2024 package.
"""


import abc
import logging
import math
import typing

import matplotlib.pyplot as plt
import numpy as np
import numpy.linalg as npl
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D  # type:ignore
from mpl_toolkits.mplot3d.art3d import Poly3DCollection  # type:ignore


class BasicShape(abc.ABC):
    def __init__(self) -> None:
        pass


class Point(BasicShape):
    def __init__(self, position: np.ndarray) -> None:
        super().__init__()
        self._position = position

    @property
    def position(self):
        return self._position


class Line(BasicShape):
    def __init__(self, start: np.ndarray, end: np.ndarray) -> None:
        super().__init__()
        self._start = start
        self._end = end

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end