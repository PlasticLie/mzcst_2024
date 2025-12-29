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
from mpl_toolkits.mplot3d import Axes3D  # type:ignore
from mpl_toolkits.mplot3d.art3d import Poly3DCollection  # type:ignore

from .. import Parameter, common, component, interface, material
from .. import profiles_to_shapes as p2s
from .. import shape_operations as so
from .. import transformations_and_picks as tp
from ..shapes import Brick
from ..sources_and_ports.hf import Port

_logger = logging.getLogger(__name__)


class JerusalemCross:
    """
    JerusalemCross 的 Docstring

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
        l_sub: Parameter,
        w_sub: Parameter,
        h_sub: Parameter,
        l_cross: Parameter,
        w_cross: Parameter,
        l_hat: Parameter,
        w_hat: Parameter,
        h_trace: Parameter,
        substrate_material: material.Material = material.VACUUM,
        trace_material: material.Material = material.PEC,
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

        # 计算派生参数
        self.l_unit = Parameter(2) * (w_hat + l_cross) + w_cross
        self.w_unit = Parameter(2) * (w_hat + l_cross) + w_cross
        self.center_x = l_sub / Parameter(2)
        self.center_y = w_sub / Parameter(2)
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
                (-(self.l_unit / Parameter("2"))).name,  # xmin
                (+(self.l_unit / Parameter("2"))).name,  # xmax
                (-(self.w_cross / Parameter("2"))).name,  # ymin
                (+(self.w_cross / Parameter("2"))).name,  # ymax
                self.h_sub.name,  # zmin
                (self.h_sub + self.h_trace).name,  # zmax
                unit_comp + "/" + TRACE_COMP,  # 分组名
                self.trace_material.name,  # 材料名
            ],
            [
                "trace_1",  # 纵向十字
                (-(self.w_cross / Parameter("2"))).name,  # xmin
                (+(self.w_cross / Parameter("2"))).name,  # xmax
                (-(self.l_unit / Parameter("2"))).name,  # ymin
                (+(self.l_unit / Parameter("2"))).name,  # ymax
                self.h_sub.name,  # zmin
                (self.h_sub + self.h_trace).name,  # zmax
                unit_comp + "/" + TRACE_COMP,  # 分组名
                self.trace_material.name,  # 材料名
            ],
            [
                "trace_2",  # 下部帽子
                (
                    -self.center_x + (self.l_sub - self.l_hat) / Parameter("2")
                ).name,  # xmin
                (
                    -self.center_x
                    + (self.l_sub - self.l_hat) / Parameter("2")
                    + self.l_hat
                ).name,  # xmax
                (
                    -self.center_y + (self.w_sub - self.w_unit) / Parameter("2")
                ).name,  # ymin
                (
                    -self.center_y
                    + (self.w_sub - self.w_unit) / Parameter("2")
                    + self.w_hat
                ).name,  # ymax
                self.h_sub.name,  # zmin
                (self.h_sub + self.h_trace).name,  # zmax
                unit_comp + "/" + TRACE_COMP,  # 分组名
                self.trace_material.name,  # 材料名
            ],
            [
                "trace_3",  # 上部帽子
                (
                    -self.center_x + (self.l_sub - self.l_hat) / Parameter("2")
                ).name,  # xmin
                (
                    -self.center_x
                    + (self.l_sub - self.l_hat) / Parameter("2")
                    + self.l_hat
                ).name,  # xmax
                (
                    -self.center_y
                    + (self.w_sub + self.w_unit) / Parameter("2")
                    - self.w_hat
                ).name,  # ymin
                (
                    -self.center_y + (self.w_sub + self.w_unit) / Parameter("2")
                ).name,  # ymax
                self.h_sub.name,  # zmin
                (self.h_sub + self.h_trace).name,  # zmax
                unit_comp + "/" + TRACE_COMP,  # 分组名
                self.trace_material.name,  # 材料名
            ],
            [
                "trace_4",  # 左侧帽子
                (
                    -self.center_x + (self.l_sub - self.l_unit) / Parameter("2")
                ).name,  # xmin
                (
                    -self.center_x
                    + (self.l_sub - self.l_unit) / Parameter("2")
                    + self.w_cross
                ).name,  # xmax
                (
                    -self.center_y + (self.w_sub - self.l_hat) / Parameter("2")
                ).name,  # ymin
                (
                    -self.center_y
                    + (self.w_sub - self.l_hat) / Parameter("2")
                    + self.l_hat
                ).name,  # ymax
                self.h_sub.name,  # zmin
                (self.h_sub + self.h_trace).name,  # zmax
                unit_comp + "/" + TRACE_COMP,  # 分组名
                self.trace_material.name,  # 材料名
            ],
            [
                "trace_5",  # 右侧帽子
                (
                    -self.center_x
                    + (self.l_sub + self.l_unit) / Parameter("2")
                    - self.w_cross
                ).name,  # xmin
                (
                    -self.center_x + (self.l_sub + self.l_unit) / Parameter("2")
                ).name,  # xmax
                (
                    -self.center_y + (self.w_sub - self.l_hat) / Parameter("2")
                ).name,  # ymin
                (
                    -self.center_y
                    + (self.w_sub - self.l_hat) / Parameter("2")
                    + self.l_hat
                ).name,  # ymax
                self.h_sub.name,  # zmin
                (self.h_sub + self.h_trace).name,  # zmax
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
            "0",  # xmin
            self.l_sub.name,  # xmax
            "0",  # ymin
            self.w_sub.name,  # ymax
            "0",  # zmin
            self.h_sub.name,  # zmax
            unit_comp + "/" + substrate_comp,  # 分组名
            self.substrate_material.name,  # 材料名
        ).create(modeler)

        t1 = time.perf_counter()
        _logger.info(
            "%s",
            f'Trace of "{self.name}" created, execution time: {common.time_to_string(t1-t0)}',
        )
        return sub

    def create_flat_unit(
        self, modeler: "interface.Model3D"
    ) -> "JerusalemCross":
        unit_comp: str = self.name
        substrate_comp: str = "substrate"
        sub = Brick(
            "substrate",  # 实体名
            "0",  # xmin
            self.l_sub.name,  # xmax
            "0",  # ymin
            self.w_sub.name,  # ymax
            "0",  # zmin
            self.h_sub.name,  # zmax
            unit_comp + "/" + substrate_comp,  # 分组名
            self.substrate_material.name,  # 材料名
        ).create(modeler)

        unit_base_x = self.center_x
        unit_base_y = self.center_y
        TRACE_COMP: str = "traces"
        traces_info: list[list[str]] = [
            [
                "trace_0",  # 横向十字
                (unit_base_x - (self.l_unit / Parameter("2"))).name,  # xmin
                (unit_base_x + (self.l_unit / Parameter("2"))).name,  # xmax
                (unit_base_y - (self.w_cross / Parameter("2"))).name,  # ymin
                (unit_base_y + (self.w_cross / Parameter("2"))).name,  # ymax
                self.h_sub.name,  # zmin
                (self.h_sub + self.h_trace).name,  # zmax
                unit_comp + "/" + TRACE_COMP,  # 分组名
                self.trace_material.name,  # 材料名
            ],
            [
                "trace_1",  # 纵向十字
                (unit_base_x - (self.w_cross / Parameter("2"))).name,  # xmin
                (unit_base_x + (self.w_cross / Parameter("2"))).name,  # xmax
                (unit_base_y - (self.l_unit / Parameter("2"))).name,  # ymin
                (unit_base_y + (self.l_unit / Parameter("2"))).name,  # ymax
                self.h_sub.name,  # zmin
                (self.h_sub + self.h_trace).name,  # zmax
                unit_comp + "/" + TRACE_COMP,  # 分组名
                self.trace_material.name,  # 材料名
            ],
            [
                "trace_2",  # 下部帽子
                (
                    unit_base_x
                    - self.center_x
                    + (self.l_sub - self.l_hat) / Parameter("2")
                ).name,  # xmin
                (
                    unit_base_x
                    - self.center_x
                    + (self.l_sub - self.l_hat) / Parameter("2")
                    + self.l_hat
                ).name,  # xmax
                (
                    unit_base_y
                    - self.center_y
                    + (self.w_sub - self.w_unit) / Parameter("2")
                ).name,  # ymin
                (
                    unit_base_y
                    - self.center_y
                    + (self.w_sub - self.w_unit) / Parameter("2")
                    + self.w_hat
                ).name,  # ymax
                self.h_sub.name,  # zmin
                (self.h_sub + self.h_trace).name,  # zmax
                unit_comp + "/" + TRACE_COMP,  # 分组名
                self.trace_material.name,  # 材料名
            ],
            [
                "trace_3",  # 上部帽子
                (
                    unit_base_x
                    - self.center_x
                    + (self.l_sub - self.l_hat) / Parameter("2")
                ).name,  # xmin
                (
                    unit_base_x
                    - self.center_x
                    + (self.l_sub - self.l_hat) / Parameter("2")
                    + self.l_hat
                ).name,  # xmax
                (
                    unit_base_y
                    - self.center_y
                    + (self.w_sub + self.w_unit) / Parameter("2")
                    - self.w_hat
                ).name,  # ymin
                (
                    unit_base_y
                    - self.center_y
                    + (self.w_sub + self.w_unit) / Parameter("2")
                ).name,  # ymax
                self.h_sub.name,  # zmin
                (self.h_sub + self.h_trace).name,  # zmax
                unit_comp + "/" + TRACE_COMP,  # 分组名
                self.trace_material.name,  # 材料名
            ],
            [
                "trace_4",  # 左侧帽子
                (
                    unit_base_x
                    - self.center_x
                    + (self.l_sub - self.l_unit) / Parameter("2")
                ).name,  # xmin
                (
                    unit_base_x
                    - self.center_x
                    + (self.l_sub - self.l_unit) / Parameter("2")
                    + self.w_cross
                ).name,  # xmax
                (
                    unit_base_y
                    - self.center_y
                    + (self.w_sub - self.l_hat) / Parameter("2")
                ).name,  # ymin
                (
                    unit_base_y
                    - self.center_y
                    + (self.w_sub - self.l_hat) / Parameter("2")
                    + self.l_hat
                ).name,  # ymax
                self.h_sub.name,  # zmin
                (self.h_sub + self.h_trace).name,  # zmax
                unit_comp + "/" + TRACE_COMP,  # 分组名
                self.trace_material.name,  # 材料名
            ],
            [
                "trace_5",  # 右侧帽子
                (
                    unit_base_x
                    - self.center_x
                    + (self.l_sub + self.l_unit) / Parameter(2)
                    - self.w_cross
                ).name,  # xmin
                (
                    unit_base_x
                    - self.center_x
                    + (self.l_sub + self.l_unit) / Parameter(2)
                ).name,  # xmax
                (
                    unit_base_y
                    - self.center_y
                    + (self.w_sub - self.l_hat) / Parameter("2")
                ).name,  # ymin
                (
                    unit_base_y
                    - self.center_y
                    + (self.w_sub - self.l_hat) / Parameter("2")
                    + self.l_hat
                ).name,  # ymax
                self.h_sub.name,  # zmin
                (self.h_sub + self.h_trace).name,  # zmax
                unit_comp + "/" + TRACE_COMP,  # 分组名
                self.trace_material.name,  # 材料名
            ],
        ]
        traces: list[Brick] = []
        for j in range(len(traces_info)):
            traces.append(Brick(*traces_info[j]).create(modeler))

        for j in range(len(traces_info) - 1, 0, -1):
            traces[j - 1].add(modeler, traces[j])
        return self
