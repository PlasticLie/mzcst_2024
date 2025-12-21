"""

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

    def __repr__(self) -> str:
        return f"Line2D(a={self._a}, b={self._b}, c={self._c})"

    def distance_to_point(self, point: np.ndarray) -> float:
        """Calculate the perpendicular distance from a point to the line."""
        numerator = abs(self._a * point[0] + self._b * point[1] + self._c)
        denominator = math.sqrt(self._a**2 + self._b**2)
        return numerator / denominator


class Line3D(BasicShape):
    """Represents a 3D line defined by a point and a direction vector."""

    def __init__(self, point: np.ndarray, direction: np.ndarray) -> None:
        super().__init__()
        self._point = point
        self._direction = direction / npl.norm(direction)
        return

    @property
    def point(self):
        return self._point

    @property
    def direction(self):
        return self._direction

    def __repr__(self) -> str:
        return f"Line3D(point={self._point}, direction={self._direction})"

    def distance_to_point(self, point: np.ndarray) -> float:
        """Calculate the shortest distance from a point to the line."""
        p0 = self._point
        d = self._direction
        p = point
        cross_prod = npl.norm(np.cross(p - p0, d))
        return float(cross_prod / npl.norm(d))


class Plane(BasicShape):
    """Represents a plane in 3D space defined by the equation ax + by + cz + d = 0."""

    def __init__(self, a: float, b: float, c: float, d: float) -> None:
        super().__init__()
        self._a = a
        self._b = b
        self._c = c
        self._d = d
        return

    @classmethod
    def from_point_normal(
        cls, point: np.ndarray, normal: np.ndarray
    ) -> "Plane":
        """Create a Plane instance from a point and a normal vector."""
        a, b, c = normal
        d = -(a * point[0] + b * point[1] + c * point[2])
        return cls(a, b, c, d)

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
    def d(self):
        return self._d

    def __repr__(self) -> str:
        return f"Plane(a={self._a}, b={self._b}, c={self._c}, d={self._d})"

    def distance_to_point(self, point: np.ndarray) -> float:
        """Calculate the perpendicular distance from a point to the plane."""
        numerator = abs(
            self._a * point[0]
            + self._b * point[1]
            + self._c * point[2]
            + self._d
        )
        denominator = math.sqrt(self._a**2 + self._b**2 + self._c**2)
        return numerator / denominator
