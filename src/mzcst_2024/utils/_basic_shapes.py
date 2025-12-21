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

from typing import Optional


class BasicShape(abc.ABC):
    def __init__(self) -> None:
        pass


class Point(BasicShape):
    def __init__(
        self,
        x: float | np.ndarray,
        y: Optional[float] = None,
        z: Optional[float] = None,
    ) -> None:
        super().__init__()
        if isinstance(x, np.ndarray):
            if x.shape == (2,):
                self._x = x[0]
                self._y = x[1]
                self._z = 0.0
            elif x.shape == (3,):
                self._x = x[0]
                self._y = x[1]
                self._z = x[2]
            else:
                raise ValueError("Numpy array must be of shape (2,) or (3,).")
        else:
            if y is None or z is None:
                raise ValueError("y and z must be provided when x is a float.")
            self._x = x
            self._y = y
            self._z = z
        return

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z


class Line2D(BasicShape):
    """Represents a 2D line in the form ax + by + c = 0."""

    def __init__(self, a: float, b: float, c: float) -> None:
        super().__init__()
        self._a = a
        self._b = b
        self._c = c
        return

    @classmethod
    def from_points(cls, p1: np.ndarray, p2: np.ndarray) -> "Line2D":
        """Create a Line2D instance from two points."""
        a = p2[1] - p1[1]
        b = p1[0] - p2[0]
        c = p2[0] * p1[1] - p1[0] * p2[1]
        return cls(a, b, c)

    @property
    def a(self):
        return self._a

    @property
    def b(self):
        return self._b

    @property
    def c(self):
        return self._c

    @property
    def slope(self):
        if self._b == 0:
            raise ValueError("Slope is undefined for vertical lines.")
        return -self._a / self._b

    @property
    def intercept(self):
        if self._b == 0:
            raise ValueError("Intercept is undefined for vertical lines.")
        return -self._c / self._b

    def get_x(self, y: float) -> float:
        """Get x coordinate for a given y on the line."""
        if self._a == 0:
            raise ValueError("Cannot compute x for horizontal lines.")
        return (-self._b * y - self._c) / self._a

    def get_y(self, x: float) -> float:
        """Get y coordinate for a given x on the line."""
        if self._b == 0:
            raise ValueError("Cannot compute y for vertical lines.")
        return (-self._a * x - self._c) / self._b
