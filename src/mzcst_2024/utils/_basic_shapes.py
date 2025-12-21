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
    def __init__(
        self,
        x: float,
        y: float,
        z: float = 0.0,
    ) -> None:
        super().__init__()

        self._x = x
        self._y = y
        self._z = z
        return

    @classmethod
    def from_array(cls, arr: np.ndarray) -> "Point":
        """Create a Point instance from a numpy array."""
        if arr.shape == (2,):
            return cls(arr[0], arr[1], 0.0)
        if arr.shape == (3,):
            return cls(arr[0], arr[1], arr[2])
        raise ValueError("Array must be of shape (2,) or (3,)")

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z

    def __repr__(self) -> str:
        return f"Point(x={self._x}, y={self._y}, z={self._z})"

    def to_array(self) -> np.ndarray:
        return np.array([self._x, self._y, self._z])

    def distance_to(self, other: "Point") -> float:
        """Calculate the Euclidean distance to another point."""
        return math.sqrt(
            (self._x - other.x) ** 2
            + (self._y - other.y) ** 2
            + (self._z - other.z) ** 2
        )


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
