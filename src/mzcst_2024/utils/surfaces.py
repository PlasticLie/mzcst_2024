"""曲面定义和相关计算。"""

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

_logger = logging.getLogger(__name__)

#######################################
# region 曲面类定义
# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓


class BaseSurfaceObject(abc.ABC):
    """曲面基类，不建议直接实例化。"""

    @staticmethod
    def vec_rotate(
        vec: np.ndarray, axis: np.ndarray, degree: float
    ) -> np.ndarray:
        """绕指定旋转轴旋转目标向量。

        矢量 `a` 垂直于转轴 `n`, 旋转θ角后变为矢量 `b` 。

        旋转后的矢量由两部分合成：
        `b = a cos θ + n / |n| × a sin θ`


        Parameters
        ----------
        vec : np.ndarray
            目标向量。
        axis : np.ndarray
            旋转轴
        degree : float
            旋转角度

        Returns
        -------
        np.ndarray
            旋转后的向量
        """
        # radian = degree / 180 * np.pi
        radian = np.deg2rad(degree)
        r = vec * np.cos(radian) + np.cross(
            axis / npl.norm(axis), vec * np.sin(radian)
        )
        return r

    def __init__(self):
        pass


class BinarySurface(BaseSurfaceObject):
    """可以写成二元函数的曲面。"""

    def __init__(self):
        super().__init__()
        return

    @abc.abstractmethod
    def get_z(
        self, x: float | np.ndarray, y: float | np.ndarray
    ) -> float | np.ndarray:
        return 0.0


class EllipticalParaboloidDome(BinarySurface):
    """椭圆抛物面，开口向下，以z轴为对称轴。

    表达式为: `x**2 / a**2 + y**2 / b**2 = 1 - z / h`；

    变形得到: `x**2 / a**2 + y**2 / b**2 + z / h - 1 = 0`；

    也可写成: `z = h * (1 - x**2 / a**2 - y**2 / b**2)`。

    其中`a`是`x`方向的半长轴，`b`是`y`方向的半短轴。

    Attributes:
        semi_x (float): `z == 0` 平面的半长轴（x方向）。
        semi_y (float): `z == 0` 平面的半短轴（y方向）。
        height (float): 高度。

    """

    def __init__(self, semi_x: float, semi_y: float, height: float):
        super().__init__()
        self._semi_x = semi_x
        self._semi_y = semi_y
        self._height = height
        return

    # 属性方法

    @property
    def semi_x(self):
        return self._semi_x

    @property
    def semi_y(self) -> float:
        return self._semi_y

    @property
    def height(self) -> float:
        return self._height

    # 特殊方法
    def __repr__(self) -> str:
        return f"EllipticalParaboloidDome({self._semi_x}, {self._semi_y}, {self._height})"

    def __call__(
        self,
        x: float | np.ndarray,
        y: float | np.ndarray,
    ) -> float | np.ndarray:
        """作为函数调用时返回给定x、y值对应的z值。

        Args:
            x (Union[float, np.ndarray]): x值
            y (Union[float, np.ndarray]): y值

        Returns:
            Union[float, np.ndarray]: z值
        """

        z = self._height * (1 - x**2 / self._semi_x**2 - y**2 / self._semi_y**2)
        return z

    # 其他方法
    def get_z(
        self, x: float | np.ndarray, y: float | np.ndarray
    ) -> float | np.ndarray:
        """作为函数调用时返回给定x、y值对应的z值。

        Args:
            x (float | np.ndarray): x值
            y (float | np.ndarray): y值

        Returns:
            float | np.ndarray: z值
        """
        z_ = self._height * (
            1 - x**2 / self._semi_x**2 - y**2 / self._semi_y**2
        )
        return z_

    def ymax(self, x: float, z: float = 0) -> float:
        # y2 = self.semi_minor**2 * (1 - x**2 / self.semi_major**2)
        y2 = self.semi_y**2 * ((1 - z / self.height) - x**2 / self.semi_x**2)
        return math.sqrt(y2) if y2 >= 0 else math.nan

    def xmax(self, y: float, z: float = 0) -> float:
        x2 = self.semi_x**2 * ((1 - z / self.height) - y**2 / self.semi_y**2)
        return math.sqrt(x2) if x2 >= 0 else math.nan

    def normal_vector(
        self,
        x: float,
        y: float,
        z: float = 0,  # pylint: disable=unused-argument
    ) -> list[float]:
        """返回曲面上给定位置的法向量。

        Args:
            x (float): x坐标。
            y (float): y坐标。
            z (float): z坐标。

        Returns:
            list[float]: 法向量。
        """

        return [2 * x / self.semi_x**2, 2 * y / self.semi_y**2, 1 / self.height]

    def normal_vector_np(self, pos: np.ndarray) -> np.ndarray:
        """返回曲面上给定位置的法向量，但是参数直接给numpy数组。

        Args:
            pos (np.ndarray): 位置向量。

        Returns:
            np.ndarray: 法向量。
        """
        return np.array(
            [
                2 * pos[0] / self.semi_x**2,
                2 * pos[1] / self.semi_y**2,
                1 / self.height,
            ]
        )

    def _u_axis_base(self, pos: np.ndarray) -> np.ndarray:
        """在给定坐标建坐标系，求x轴方向向量。
        这个方向向量是采样点所在z平面与曲面的交线的切线方向。

        Args:
            pos (np.ndarray): 位置向量。

        Returns:
            np.ndarray: x轴方向向量
        """
        pos_ = pos.tolist()
        ux: float = 0
        uy: float = 0
        uz: float = 0

        ux = +1
        uz = -2 * self.height / self.semi_x**2 * pos_[0]

        return np.array([ux, uy, uz])

    def _u_axis_rotate(self, pos: np.ndarray, degree: float) -> np.ndarray:
        return self.vec_rotate(
            self._u_axis_base(pos), self.normal_vector_np(pos), degree
        )

    def u_axis_np(self, pos: np.ndarray) -> np.ndarray:
        """在给定坐标建坐标系，求x轴方向向量。
        这个方向向量是采样点所在z平面与曲面的交线的切线方向。

        Args:
            pos (np.ndarray): 位置向量。

        Returns:
            np.ndarray: x轴方向向量
        """

        return self._u_axis_rotate(pos, 0)

    def u_axis_np_20250308(self, pos: np.ndarray) -> np.ndarray:
        """在给定坐标建坐标系，求x轴方向向量。这个方向向量是采样点所在z平面与曲面的交线
        的切线方向。

        Args:
            pos (np.ndarray): 位置向量。

        Returns:
            np.ndarray: x轴方向向量
        """
        pos_ = pos.tolist()
        ux: float = 0
        uy: float = 0
        uz: float = 0
        if pos_[1] < 0:
            ux = 1
            uy = -1 * self.semi_y**2 * pos_[0] / (self.semi_x**2 * pos_[1])
        elif pos_[1] > 0:
            ux = -1
            uy = +1 * self.semi_y**2 * pos_[0] / (self.semi_x**2 * pos_[1])
        else:  # pos_[1] == 0
            if pos_[0] > 0:
                ux = 0
                uy = 1
            elif pos_[0] < 0:
                ux = 0
                uy = -1
            else:
                ux = 1

        return np.array([ux, uy, uz])


class Plane(BaseSurfaceObject):
    """通过一般式方程定义平面，A、B、C不全为0。

    `Ax + By + Cz + D = 0`

    类方法中提供了点法式和三点式构建方法。"""

    def __init__(self, a: float, b: float, c: float, d: float):
        super().__init__()
        self._a = a
        self._b = b
        self._c = c
        self._d = d
        return

    @classmethod
    def define_from_point_normal(cls, p1: np.ndarray, normal: np.ndarray):
        d: np.float64 = -1.0 * np.sum(p1 * normal)
        return cls(normal.item(0), normal.item(1), normal.item(2), d.item())

    @classmethod
    def define_from_3_points(
        cls, p1: np.ndarray, p2: np.ndarray, p3: np.ndarray
    ):
        v1 = p2 - p1
        v2 = p3 - p2
        normal = np.cross(v1, v2)
        return cls.define_from_point_normal(p1, normal)

    @property
    def a(self) -> float:
        return self._a

    @property
    def b(self) -> float:
        return self._b

    @property
    def c(self) -> float:
        return self._c

    @property
    def d(self) -> float:
        return self.d

    @property
    def coefficients(self) -> list[float]:
        return [self._a, self._b, self._c, self._d]

    @property
    def normal(self) -> np.ndarray:
        return np.array([self._a, self._b, self._c])

    def get_z(self, x: float, y: float) -> float:
        """返回给定x、y值对应的z值。"""

        try:
            z = -1.0 * (self._a * x + self._b * y + self._d) / self._c
        except ZeroDivisionError:
            z = float("nan")
        return z


# endregion
# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

#######################################
# region 计算用辅助函数
# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓


def reorderCenterOutwards(lineXYZ: np.ndarray, cIdx: int) -> np.ndarray:
    """辅助函数: 根据“中心索引”重排，使序号1=中心，2=中心上方,3=中心下方,...

    lineXYZ: size(S,3). cIdx是中心所在的行索引
    我们想要新的序列:

      1 => cIdx
      2 => cIdx+1
      3 => cIdx-1
      4 => cIdx+2
      5 => cIdx-2
      ...

      直到用完区间 [1,S].

    若某一步越界则跳过该方向; 直到两方向都越界才停止.

    Attributes:
        param1 (type): 第1个属性。

    """

    S: int = lineXYZ.shape[0]
    outLine = np.zeros((S, 3))
    outLine[0, :] = lineXYZ[cIdx, :]
    usedCount = 1  # 下一个放入outLine中的数据的行位置索引
    delta = 1
    signFlag = +1  # +1先走上面(或右边), -1走下面(左边)
    while usedCount < S:
        if signFlag > 0:
            tryIdx = cIdx + delta
        else:
            tryIdx = cIdx - delta
        if tryIdx >= 0 and tryIdx <= S - 1:
            outLine[usedCount, :] = lineXYZ[tryIdx, :]
            usedCount += 1
        signFlag = -signFlag  # 换方向
        if signFlag > 0:
            delta += 1  # 每次负->正时, delta加1
        # 如果下次再越界, 继续循环, 直到 S次填完或两边都越界.
        if delta > max(cIdx, S - cIdx - 1):
            # 说明两边都越界,无法再放
            break

    return outLine[: usedCount + 1, :]


def xy2gridIndex(
    x: float,
    y: float,
    xMin: float,
    xMax: float,
    yMin: float,
    yMax: float,
    Nx: int,
    Ny: int,
):
    """
    将连续坐标 `(x,y)` 映射到离散网格索引 `(iRow, jCol)`
    `xMin..xMax`, `yMin..yMax`: 网格覆盖区域
    `Nx`, `Ny`: 网格维度 `(sizeu, sizev)`

    思路：先把 `x`,`y` 线性映射到 `[1..Nx]`, `[1..Ny]`，再 `round()`，最后 clamp。"""
    # 防止分母为0
    TINY_FLOAT = 1e-12
    if xMax == xMin:
        xMax = xMin + TINY_FLOAT
    if yMax == yMin:
        yMax = yMin + TINY_FLOAT

    # 映射到网格坐标
    iFloat = (x - xMin) / (xMax - xMin) * (Nx - 1)
    jFloat = (y - yMin) / (yMax - yMin) * (Ny - 1)

    # 四舍五入到最近像素
    iRow = round(iFloat)
    jCol = round(jFloat)

    return (iRow, jCol)


# endregion
# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
