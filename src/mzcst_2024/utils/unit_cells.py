"""常用周期结构单元"""

import abc
import logging
import math
import time
import typing

import matplotlib.pyplot as plt
import numpy as np
import numpy.linalg as npl
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D  # type: ignore
from mpl_toolkits.mplot3d.art3d import Poly3DCollection  # type: ignore

from .. import Parameter, ParameterLike, common, component, interface, material
from .. import profiles_to_shapes as p2s
from .. import shape_operations as so
from .. import transformations_and_picks as tp
from ..shapes import Brick
from ..sources_and_ports.hf import Port

_logger = logging.getLogger(__name__)


class JerusalemCross:
    """
    耶路撒冷十字结构单元。

    Parameters
    ----------
    name : str
        结构名称
    l_sub : Parameter
        基板长度
    w_sub : Parameter
        基板宽度
    h_sub : Parameter
        基板高度
    l_cross : Parameter
        十字臂长度
    w_cross : Parameter
        十字臂宽度
    l_hat : Parameter
        帽子长度
    w_hat : Parameter
        帽子宽度
    h_trace : Parameter
        铜厚
    """

    def __init__(
        self,
        name: str,
        l_sub: ParameterLike,
        w_sub: ParameterLike,
        h_sub: ParameterLike,
        l_cross: ParameterLike,
        w_cross: ParameterLike,
        l_hat: ParameterLike,
        w_hat: ParameterLike,
        h_trace: ParameterLike,
        substrate_material: material.Material = material.VACUUM,
        trace_material: material.Material = material.PEC,
        *,
        base: tuple[ParameterLike, ParameterLike, ParameterLike] = (0, 0, 0),
    ):
        """根据结构参数初始化耶路撒冷十字结构。"""
        self.name = name
        self.l_sub = l_sub
        self.w_sub = w_sub
        self.h_sub = h_sub
        self.l_cross = l_cross
        self.w_cross = w_cross
        self.l_hat = l_hat
        self.w_hat = w_hat
        self.h_trace = h_trace
        self.substrate_material = substrate_material
        self.trace_material = trace_material

        self.base = [Parameter(b) for b in base]

        # 计算派生参数
        self.l_unit = 2 * (w_hat + l_cross) + w_cross
        self.w_unit = 2 * (w_hat + l_cross) + w_cross
        self.center_x = l_sub / 2
        self.center_y = w_sub / 2
        return

    def create_traces(self, modeler: "interface.Model3D") -> "Brick":
        """在给定的建模器中创建耶路撒冷十字结构。

        Args:
            modeler (interface.Model3D): 建模环境。

        Returns:
            self: 对象自身的引用。
        """
        t0 = time.perf_counter()
        unit_comp = self.name
        TRACE_COMP: str = "traces"
        traces_info: list[list[str]] = [
            [
                "trace_0",  # 横向十字
                f"{self.base[0] - (self.l_unit / 2)}",  # xmin
                f"{self.base[0] + (self.l_unit / 2)}",  # xmax
                f"{self.base[1] - (self.w_cross / 2)}",  # ymin
                f"{self.base[1] + (self.w_cross / 2)}",  # ymax
                f"{self.base[2] + self.h_sub}",  # zmin
                f"{self.base[2] + self.h_sub + self.h_trace}",  # zmax
                unit_comp + "/" + TRACE_COMP,  # 分组名
                self.trace_material.name,  # 材料名
            ],
            [
                "trace_1",  # 纵向十字
                f"{self.base[0] - (self.w_cross / 2)}",  # xmin
                f"{self.base[0] + (self.w_cross / 2)}",  # xmax
                f"{self.base[1] - (self.l_unit / 2)}",  # ymin
                f"{self.base[1] + (self.l_unit / 2)}",  # ymax
                f"{self.base[2] + self.h_sub}",  # zmin
                f"{self.base[2] + self.h_sub + self.h_trace}",  # zmax
                unit_comp + "/" + TRACE_COMP,  # 分组名
                self.trace_material.name,  # 材料名
            ],
            [
                "trace_2",  # 下部帽子
                f"{self.base[0] - self.center_x + (self.l_sub - self.l_hat) / 2}",  # xmin
                f"{self.base[0] - self.center_x + (self.l_sub - self.l_hat) / 2 + self.l_hat}",  # xmax
                f"{self.base[1] - self.center_y + (self.w_sub - self.w_unit) / 2}",  # ymin
                f"{self.base[1] - self.center_y + (self.w_sub - self.w_unit) / 2 + self.w_hat}",  # ymax
                f"{self.base[2] + self.h_sub}",  # zmin
                f"{self.base[2] + self.h_sub + self.h_trace}",  # zmax
                unit_comp + "/" + TRACE_COMP,  # 分组名
                self.trace_material.name,  # 材料名
            ],
            [
                "trace_3",  # 上部帽子
                f"{self.base[0] - self.center_x + (self.l_sub - self.l_hat) / 2}",  # xmin
                f"{self.base[0] - self.center_x + (self.l_sub - self.l_hat) / 2 + self.l_hat}",  # xmax
                f"{self.base[1] - self.center_y + (self.w_sub + self.w_unit) / 2 - self.w_hat}",  # ymin
                f"{self.base[1] - self.center_y + (self.w_sub + self.w_unit) / 2}",  # ymax
                f"{self.base[2] + self.h_sub}",  # zmin
                f"{self.base[2] + self.h_sub + self.h_trace}",  # zmax
                unit_comp + "/" + TRACE_COMP,  # 分组名
                self.trace_material.name,  # 材料名
            ],
            [
                "trace_4",  # 左侧帽子
                f"{self.base[0] - self.center_x + (self.l_sub - self.l_unit) / 2}",  # xmin
                f"{self.base[0] - self.center_x + (self.l_sub - self.l_unit) / 2 + self.w_cross}",  # xmax
                f"{self.base[1] - self.center_y + (self.w_sub - self.l_hat) / 2}",  # ymin
                f"{self.base[1] - self.center_y + (self.w_sub - self.l_hat) / 2 + self.l_hat}",  # ymax
                f"{self.base[2] + self.h_sub}",  # zmin
                f"{self.base[2] + self.h_sub + self.h_trace}",  # zmax
                unit_comp + "/" + TRACE_COMP,  # 分组名
                self.trace_material.name,  # 材料名
            ],
            [
                "trace_5",  # 右侧帽子
                f"{self.base[0] - self.center_x + (self.l_sub + self.l_unit) / 2 - self.w_cross}",  # xmin
                f"{self.base[0] - self.center_x + (self.l_sub + self.l_unit) / 2}",  # xmax
                f"{self.base[1] - self.center_y + (self.w_sub - self.l_hat) / 2}",  # ymin
                f"{self.base[1] - self.center_y + (self.w_sub - self.l_hat) / 2 + self.l_hat}",  # ymax
                f"{self.base[2] + self.h_sub}",  # zmin
                f"{self.base[2] + self.h_sub + self.h_trace}",  # zmax
                unit_comp + "/" + TRACE_COMP,  # 分组名
                self.trace_material.name,  # 材料名
            ],
        ]
        traces: list[Brick] = []
        for j in range(len(traces_info)):
            traces.append(Brick(*traces_info[j]).create(modeler))

        for j in range(len(traces_info) - 1, 0, -1):
            traces[j - 1].add(modeler, traces[j])

        t1 = time.perf_counter()
        _logger.info(
            "%s",
            f'Trace of "{self.name}" created, execution time: {common.time_to_string(t1-t0)}',
        )

        return traces[0]

    def create_substrate(self, modeler: "interface.Model3D") -> "Brick":
        t0 = time.perf_counter()
        unit_comp = self.name

        substrate_comp: str = "substrate"
        sub = Brick(
            "substrate",  # 实体名
            f"{self.base[0] - self.l_sub/2}",  # xmin
            f"{self.base[0] + self.l_sub/2}",  # xmax
            f"{self.base[1] - self.w_sub/2}",  # ymin
            f"{self.base[1] + self.w_sub/2}",  # ymax
            f"{self.base[2]}",  # zmin
            f"{self.base[2]+self.h_sub}",  # zmax
            unit_comp + "/" + substrate_comp,  # 分组名
            self.substrate_material.name,  # 材料名
        ).create(modeler)

        t1 = time.perf_counter()
        _logger.info(
            "%s",
            f'Substrate of "{self.name}" created, execution time: {common.time_to_string(t1-t0)}',
        )
        return sub

    def create_flat_unit(
        self, modeler: "interface.Model3D"
    ) -> "JerusalemCross":
        """Create Jerusalem Cross unit cell in the given modeler.

        Parameters
        ----------
        modeler : interface.Model3D
            The specified modeler.

        Returns
        -------
        JerusalemCross
            The instance itself.
        """
        time_start = time.perf_counter()
        self.create_substrate(modeler)
        self.create_traces(modeler)
        time_end = time.perf_counter()
        _logger.info(
            "%s",
            f'Flat unit cell of "{self.name}" created, execution time: {common.time_to_string(time_end - time_start)}',
        )
        return self
