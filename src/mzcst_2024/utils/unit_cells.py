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


class BaseUnitCellObject(abc.ABC):
    """周期结构单元的基类。

    Attributes
    ----------
    name : str
        结构名称
    base : list[Parameter]
        结构基点坐标 [x, y, z]
    """

    def __init__(
        self,
        name: str,
        *,
        base: tuple[ParameterLike, ParameterLike, ParameterLike] = (0, 0, 0),
    ):
        """初始化周期结构单元。

        Parameters
        ----------
        name : str
            结构名称
        base : tuple[ParameterLike, ParameterLike, ParameterLike], optional
            结构基点坐标，默认为 (0, 0, 0)
        """
        self.name = name
        self.base = [Parameter(b) for b in base]


class JerusalemCross(BaseUnitCellObject):
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
        h_boss: ParameterLike = Parameter(0),
        substrate_material: material.Material = material.VACUUM,
        trace_material: material.Material = material.PEC,
        *,
        base: tuple[ParameterLike, ParameterLike, ParameterLike] = (0, 0, 0),
    ):
        """根据结构参数初始化耶路撒冷十字结构。"""
        super().__init__(name, base=base)
        self.l_sub = Parameter(l_sub)
        self.w_sub = Parameter(w_sub)
        self.h_sub = Parameter(h_sub)
        self.l_cross = Parameter(l_cross)
        self.w_cross = Parameter(w_cross)
        self.l_hat = Parameter(l_hat)
        self.w_hat = Parameter(w_hat)
        self.h_trace = Parameter(h_trace)
        self.h_boss = Parameter(h_boss)
        self.substrate_material = substrate_material
        self.trace_material = trace_material

        # 生成派生参数
        self.l_unit = 2 * (w_hat + l_cross) + w_cross
        self.w_unit = 2 * (w_hat + l_cross) + w_cross
        self.center_x = l_sub / 2
        self.center_y = w_sub / 2

        self.trace_comp = "traces"
        self.substrate_comp = "substrate"
        self.boss_comp = "boss"
        self.shell_comp = "shell"
        self.trace = None
        self.substrate = None
        self.boss = None
        self.shell = None
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
        TRACE_COMP: str = self.trace_comp
        traces_info: list[list[str]] = [
            [
                "trace_0",  # 横向十字
                f"{self.base[0] - (self.l_unit / 2)}",  # xmin
                f"{self.base[0] + (self.l_unit / 2)}",  # xmax
                f"{self.base[1] - (self.w_cross / 2)}",  # ymin
                f"{self.base[1] + (self.w_cross / 2)}",  # ymax
                f"{self.base[2] + self.h_sub + self.h_boss}",  # zmin
                f"{self.base[2] + self.h_sub + self.h_boss + self.h_trace}",  # zmax
                unit_comp + "/" + TRACE_COMP,  # 分组名
                self.trace_material.name,  # 材料名
            ],
            [
                "trace_1",  # 纵向十字
                f"{self.base[0] - (self.w_cross / 2)}",  # xmin
                f"{self.base[0] + (self.w_cross / 2)}",  # xmax
                f"{self.base[1] - (self.l_unit / 2)}",  # ymin
                f"{self.base[1] + (self.l_unit / 2)}",  # ymax
                f"{self.base[2] + self.h_sub + self.h_boss}",  # zmin
                f"{self.base[2] + self.h_sub + self.h_boss + self.h_trace}",  # zmax
                unit_comp + "/" + TRACE_COMP,  # 分组名
                self.trace_material.name,  # 材料名
            ],
            [
                "trace_2",  # 下部帽子
                f"{self.base[0] - self.center_x + (self.l_sub - self.l_hat) / 2}",  # xmin
                f"{self.base[0] - self.center_x + (self.l_sub - self.l_hat) / 2 + self.l_hat}",  # xmax
                f"{self.base[1] - self.center_y + (self.w_sub - self.w_unit) / 2}",  # ymin
                f"{self.base[1] - self.center_y + (self.w_sub - self.w_unit) / 2 + self.w_hat}",  # ymax
                f"{self.base[2] + self.h_sub + self.h_boss}",  # zmin
                f"{self.base[2] + self.h_sub + self.h_boss + self.h_trace}",  # zmax
                unit_comp + "/" + TRACE_COMP,  # 分组名
                self.trace_material.name,  # 材料名
            ],
            [
                "trace_3",  # 上部帽子
                f"{self.base[0] - self.center_x + (self.l_sub - self.l_hat) / 2}",  # xmin
                f"{self.base[0] - self.center_x + (self.l_sub - self.l_hat) / 2 + self.l_hat}",  # xmax
                f"{self.base[1] - self.center_y + (self.w_sub + self.w_unit) / 2 - self.w_hat}",  # ymin
                f"{self.base[1] - self.center_y + (self.w_sub + self.w_unit) / 2}",  # ymax
                f"{self.base[2] + self.h_sub + self.h_boss}",  # zmin
                f"{self.base[2] + self.h_sub + self.h_boss + self.h_trace}",  # zmax
                unit_comp + "/" + TRACE_COMP,  # 分组名
                self.trace_material.name,  # 材料名
            ],
            [
                "trace_4",  # 左侧帽子
                f"{self.base[0] - self.center_x + (self.l_sub - self.l_unit) / 2}",  # xmin
                f"{self.base[0] - self.center_x + (self.l_sub - self.l_unit) / 2 + self.w_cross}",  # xmax
                f"{self.base[1] - self.center_y + (self.w_sub - self.l_hat) / 2}",  # ymin
                f"{self.base[1] - self.center_y + (self.w_sub - self.l_hat) / 2 + self.l_hat}",  # ymax
                f"{self.base[2] + self.h_sub + self.h_boss}",  # zmin
                f"{self.base[2] + self.h_sub + self.h_boss + self.h_trace}",  # zmax
                unit_comp + "/" + TRACE_COMP,  # 分组名
                self.trace_material.name,  # 材料名
            ],
            [
                "trace_5",  # 右侧帽子
                f"{self.base[0] - self.center_x + (self.l_sub + self.l_unit) / 2 - self.w_cross}",  # xmin
                f"{self.base[0] - self.center_x + (self.l_sub + self.l_unit) / 2}",  # xmax
                f"{self.base[1] - self.center_y + (self.w_sub - self.l_hat) / 2}",  # ymin
                f"{self.base[1] - self.center_y + (self.w_sub - self.l_hat) / 2 + self.l_hat}",  # ymax
                f"{self.base[2] + self.h_sub + self.h_boss}",  # zmin
                f"{self.base[2] + self.h_sub + self.h_boss + self.h_trace}",  # zmax
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

        substrate_comp: str = self.substrate_comp
        self.substrate = Brick(
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
        return self.substrate

    def create_boss(
        self,
        modeler: "interface.Model3D",
        *,
        gap: ParameterLike = 0,
        boss_name: str | None = None,
    ) -> "Brick":
        """创建凸台。

        Parameters
        ----------
        modeler : interface.Model3D
            建模器。
        gap : ParameterLike, optional
            凸台之间的间隙，默认为0。
        boss_name : str, optional
            凸台的名称，默认为 None，如果为 None，则使用默认名称 "boss"。

        Returns
        -------
        Brick
            凸台对象。
        """
        boss_gap = Parameter(gap)
        unit_comp = self.name
        if boss_name is not None:
            BOSS_COMP: str = boss_name
            self.boss_comp = boss_name
        else:
            BOSS_COMP: str = self.boss_comp
        bosses_info: list[list[str]] = [
            [
                "boss_0",  # 横向十字
                f"{self.base[0] - (self.l_unit / 2) - boss_gap}",  # xmin
                f"{self.base[0] + (self.l_unit / 2) + boss_gap}",  # xmax
                f"{self.base[1] - (self.w_cross / 2) - boss_gap}",  # ymin
                f"{self.base[1] + (self.w_cross / 2) + boss_gap}",  # ymax
                f"{self.base[2] + self.h_sub}",  # zmin
                f"{self.base[2] + self.h_sub + self.h_boss}",  # zmax
                unit_comp + "/" + BOSS_COMP,  # 分组名
                self.substrate_material.name,  # 材料名
            ],
            [
                "boss_1",  # 纵向十字
                f"{self.base[0] - (self.w_cross / 2) - boss_gap}",  # xmin
                f"{self.base[0] + (self.w_cross / 2) + boss_gap}",  # xmax
                f"{self.base[1] - (self.l_unit / 2) - boss_gap}",  # ymin
                f"{self.base[1] + (self.l_unit / 2) + boss_gap}",  # ymax
                f"{self.base[2] + self.h_sub}",  # zmin
                f"{self.base[2] + self.h_sub + self.h_boss}",  # zmax
                unit_comp + "/" + BOSS_COMP,  # 分组名
                self.substrate_material.name,  # 材料名
            ],
            [
                "boss_2",  # 下部帽子
                f"{self.base[0] - self.center_x + (self.l_sub - self.l_hat) / 2 - boss_gap}",  # xmin
                f"{self.base[0] - self.center_x + (self.l_sub - self.l_hat) / 2 + self.l_hat + boss_gap}",  # xmax
                f"{self.base[1] - self.center_y + (self.w_sub - self.w_unit) / 2 - boss_gap}",  # ymin
                f"{self.base[1] - self.center_y + (self.w_sub - self.w_unit) / 2 + self.w_hat + boss_gap}",  # ymax
                f"{self.base[2] + self.h_sub}",  # zmin
                f"{self.base[2] + self.h_sub + self.h_boss}",  # zmax
                unit_comp + "/" + BOSS_COMP,  # 分组名
                self.substrate_material.name,  # 材料名
            ],
            [
                "boss_3",  # 上部帽子
                f"{self.base[0] - self.center_x + (self.l_sub - self.l_hat) / 2 - boss_gap}",  # xmin
                f"{self.base[0] - self.center_x + (self.l_sub - self.l_hat) / 2 + self.l_hat + boss_gap}",  # xmax
                f"{self.base[1] - self.center_y + (self.w_sub + self.w_unit) / 2 - self.w_hat - boss_gap}",  # ymin
                f"{self.base[1] - self.center_y + (self.w_sub + self.w_unit) / 2 + boss_gap}",  # ymax
                f"{self.base[2] + self.h_sub}",  # zmin
                f"{self.base[2] + self.h_sub + self.h_boss}",  # zmax
                unit_comp + "/" + BOSS_COMP,  # 分组名
                self.substrate_material.name,  # 材料名
            ],
            [
                "boss_4",  # 左侧帽子
                f"{self.base[0] - self.center_x + (self.l_sub - self.l_unit) / 2 - boss_gap}",  # xmin
                f"{self.base[0] - self.center_x + (self.l_sub - self.l_unit) / 2 + self.w_cross + boss_gap}",  # xmax
                f"{self.base[1] - self.center_y + (self.w_sub - self.l_hat) / 2 - boss_gap}",  # ymin
                f"{self.base[1] - self.center_y + (self.w_sub - self.l_hat) / 2 + self.l_hat + boss_gap}",  # ymax
                f"{self.base[2] + self.h_sub}",  # zmin
                f"{self.base[2] + self.h_sub + self.h_boss}",  # zmax
                unit_comp + "/" + BOSS_COMP,  # 分组名
                self.substrate_material.name,  # 材料名
            ],
            [
                "boss_5",  # 右侧帽子
                f"{self.base[0] - self.center_x + (self.l_sub + self.l_unit) / 2 - self.w_cross - boss_gap}",  # xmin
                f"{self.base[0] - self.center_x + (self.l_sub + self.l_unit) / 2 + boss_gap}",  # xmax
                f"{self.base[1] - self.center_y + (self.w_sub - self.l_hat) / 2 - boss_gap}",  # ymin
                f"{self.base[1] - self.center_y + (self.w_sub - self.l_hat) / 2 + self.l_hat + boss_gap}",  # ymax
                f"{self.base[2] + self.h_sub}",  # zmin
                f"{self.base[2] + self.h_sub + self.h_boss}",  # zmax
                unit_comp + "/" + BOSS_COMP,  # 分组名
                self.substrate_material.name,  # 材料名
            ],
        ]
        bosses: list[Brick] = []
        for j in range(len(bosses_info)):
            bosses.append(Brick(*bosses_info[j]).create(modeler))

        for j in range(len(bosses_info) - 1, 0, -1):
            bosses[j - 1].add(modeler, bosses[j])
        self.boss = bosses[0]
        return self.boss

    def create_boss_and_shell(
        self, modeler: "interface.Model3D", *, shell_gap: ParameterLike = 0
    ) -> tuple["Brick", "Brick"]:
        """创建凸台和凸台的互补壳（带壳体间隙）。

        Parameters
        ----------
        modeler : interface.Model3D
            建模器。

        Returns
        -------
        tuple[Brick, Brick]
            凸台对象和互补壳对象。
        """
        boss = self.create_boss(modeler, gap=shell_gap, boss_name="boss_temp")
        unit_comp = self.name

        SHELL_COMP: str = self.shell_comp
        shell = Brick(
            "shell",  # 实体名
            f"{self.base[0] - self.l_sub/2}",  # xmin
            f"{self.base[0] + self.l_sub/2}",  # xmax
            f"{self.base[1] - self.w_sub/2}",  # ymin
            f"{self.base[1] + self.w_sub/2}",  # ymax
            f"{self.base[2] + self.h_sub}",  # zmin
            f"{self.base[2] + self.h_sub + self.h_boss}",  # zmax
            unit_comp + "/" + SHELL_COMP,  # 分组名
            material.VACUUM_,  # 材料名
        ).create(modeler)
        shell.insert(modeler, boss)
        return boss, shell

    def create_shell(
        self, modeler: "interface.Model3D", shell_gap: ParameterLike = 0
    ) -> "Brick":
        """创建凸台的互补壳。

        Parameters
        ----------
        modeler : interface.Model3D
            建模器。
        shell_gap : ParameterLike
            壳体与凸台的间隙。

        Returns
        -------
        Brick
            互补壳对象。
        """
        unit_comp = self.name

        boss_temp = self.create_boss(
            modeler, gap=shell_gap, boss_name="boss_temp"
        )
        SHELL_COMP: str = self.shell_comp
        self.shell = Brick(
            "shell",  # 实体名
            f"{self.base[0] - self.l_sub/2}",  # xmin
            f"{self.base[0] + self.l_sub/2}",  # xmax
            f"{self.base[1] - self.w_sub/2}",  # ymin
            f"{self.base[1] + self.w_sub/2}",  # ymax
            f"{self.base[2] + self.h_sub}",  # zmin
            f"{self.base[2] + self.h_sub + self.h_boss}",  # zmax
            unit_comp + "/" + SHELL_COMP,  # 分组名
            material.VACUUM_,  # 材料名
        ).create(modeler)
        self.shell.subtract(modeler, boss_temp)
        return self.shell

    def create_flat_traces(self, modeler: "interface.Model3D") -> "Brick":
        """忽略凸台，创建平坦的耶路撒冷十字结构单元的铜层。

        Parameters
        ----------
        modeler : interface.Model3D
            The specified modeler.

        Returns
        -------
        Brick
            The instance itself.
        """
        time_start = time.perf_counter()
        boss_old = self.h_boss
        self.h_boss = Parameter(0)
        self.trace = self.create_traces(modeler)
        self.h_boss = boss_old
        time_end = time.perf_counter()
        _logger.info(
            "%s",
            f'Flat traces of "{self.name}" created, execution time: {common.time_to_string(time_end - time_start)}',
        )
        return self.trace

    def create_flat_unit(
        self, modeler: "interface.Model3D"
    ) -> "JerusalemCross":
        """创建平坦的耶路撒冷十字结构单元，不含凸台。

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
        boss_old = self.h_boss
        self.h_boss = Parameter(0)
        self.create_substrate(modeler)
        self.create_traces(modeler)
        self.h_boss = boss_old
        time_end = time.perf_counter()
        _logger.info(
            "%s",
            f'Flat unit cell of "{self.name}" created, execution time: {common.time_to_string(time_end - time_start)}',
        )
        return self

    def create_bossed_unit(
        self,
        modeler: "interface.Model3D",
    ) -> tuple[Brick, Brick]:
        """创建有凸台的耶路撒冷十字结构单元。

        Parameters
        ----------
        modeler : interface.Model3D
            The specified modeler.

        Returns
        -------
        tuple[Brick,  Brick]
            The substrate and trace bricks.
        """
        time_start = time.perf_counter()
        self.substrate = self.create_substrate(modeler)
        self.boss = self.create_boss(modeler)
        self.substrate.add(modeler, self.boss)
        self.boss = None
        self.trace = self.create_traces(modeler)
        time_end = time.perf_counter()
        _logger.info(
            "%s",
            f'Bossed unit cell of "{self.name}" created, execution time: {common.time_to_string(time_end - time_start)}',
        )
        return self.substrate, self.trace
