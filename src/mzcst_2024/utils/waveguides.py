"""常用波导"""

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

from .. import Parameter, common, component, interface, material
from .. import profiles_to_shapes as p2s
from .. import shape_operations as so
from .. import transformations_and_picks as tp
from ..common import time_decorator
from ..shapes import Brick
from ..sources_and_ports.hf import Port

_logger = logging.getLogger(__name__)


class BasicWaveguide(abc.ABC):
    def __init__(self, name: str, port_config: Port):
        """初始化波导。

        Args:
            name (str): 波导名称。
            port_config (Port): 波导对应的端口对象。
        """
        self._name = name
        self._port = port_config

    @property
    def name(self) -> str:
        """返回波导名称。"""
        return self._name

    @property
    def port(self) -> Port:
        """返回波导对应的端口对象。"""
        return self._port

    @abc.abstractmethod
    def create_waveguide(
        self, modeler: "interface.Model3D"
    ) -> "BasicWaveguide":
        """在给定的建模器中创建波导。

        Args:
            modeler (interface.Model3D): 建模环境。
        """
        pass


class WR90(BasicWaveguide):
    """标准WR-90波导的参数和建模方法。

    Parameters
    ----------
    name : str
        结构名称
    port_config: Port
        波导对应的端口对象
    """

    def __init__(self, name: str, port_config: Port):
        """根据结构参数初始化WR-90波导。"""
        super().__init__(name, port_config)
        self._taper_angle = 11.2
        self._horn_length = 218.16
        self._wall_thickness = 3.78
        self._waveguide_width = 37.38
        self._waveguide_height = 16.38
        self._waveguide_length = 10.92
        return

    def create_waveguide(self, modeler: "interface.Model3D") -> "WR90":
        """在给定的建模器中创建WR-90波导。

        Args:
            modeler (interface.Model3D): 建模环境。
        """
        t0 = time.perf_counter()

        taper_angle = Parameter(f"{self._taper_angle}")
        horn_length = Parameter(f"{self._horn_length}")
        wall_thickness = Parameter(f"{self._wall_thickness}")
        waveguide_width = Parameter(f"{self._waveguide_width}")
        waveguide_height = Parameter(f"{self._waveguide_height}")
        waveguide_length = Parameter(f"{self._waveguide_length}")

        horn_down_comp = component.Component(self._name)

        solid1_down = Brick(
            "solid1",  # 实体名
            (waveguide_width / Parameter(-2)).name,  # xmin
            (waveguide_width / Parameter(2)).name,  # xmax
            (waveguide_height / Parameter(-2)).name,  # ymin
            (waveguide_height / Parameter(2)).name,  # ymax
            "0",  # zmin
            waveguide_length.name,  # zmax
            horn_down_comp.name,  # 分组名
            material.PEC_,  # 材料名
        ).create(modeler)

        # 选择顶面
        tp.pick_face_from_id(modeler, solid1_down, 1)
        solid2_down = p2s.Extrude(
            "solid2",
            horn_down_comp.name,
            "PEC",
            properties={
                "Mode": ' "Picks"',
                "Height": f' "{horn_length}"',
                "Twist": ' "0.0"',
                "Taper": f' "{taper_angle}"',
                "UsePicksForHeight": ' "False"',
                "DeleteBaseFaceSolid": ' "False"',
                "ClearPickedFace": ' "True"',
            },
        ).create_from_attributes(modeler)
        solid1_down.add(modeler, solid2_down)

        # pick face
        tp.pick_face_from_id(modeler, solid1_down, 5)
        tp.pick_face_from_id(modeler, solid1_down, 8)
        so.advanced_shell(modeler, solid1_down, "Outside", wall_thickness)

        # pick end point
        tp.pick_end_point_from_id(modeler, solid1_down, 16)
        tp.pick_end_point_from_id(modeler, solid1_down, 15)
        tp.pick_end_point_from_id(modeler, solid1_down, 13)

        # define port:
        self._port.create_from_attributes(modeler)

        # clear picks
        tp.clear_all_picks(modeler)

        t1 = time.perf_counter()
        _logger.info(
            "%s",
            f'Waveguide "{self._name}" created, execution time: {common.time_to_string(t1-t0)}',
        )
        return self


class WR817(BasicWaveguide):
    def __init__(self, name: str, port_config: Port):
        super().__init__(name, port_config)
        return

    def create_waveguide(self, modeler: "interface.Model3D") -> "WR817":
        """在给定的建模器中创建WR-817波导。包含FDP48法兰。

        Args:
            modeler (interface.Model3D): 建模环境。
        """
        t0 = time.perf_counter()

        taper_angle = Parameter(20)
        horn_length = Parameter(110 - 40)
        wall_thickness = Parameter(2)
        waveguide_width = Parameter(47.5)
        waveguide_height = Parameter(22.15)
        waveguide_length = Parameter(40)

        horn_down_comp = component.Component(self._name)

        solid1_down = Brick(
            "solid1",  # 实体名
            f"{waveguide_width / (-2)}",  # xmin
            f"{waveguide_width / (2)}",  # xmax
            f"{waveguide_height / (-2)}",  # ymin
            f"{waveguide_height / (2)}",  # ymax
            "0",  # zmin
            f'{waveguide_length}',  # zmax
            horn_down_comp.name,  # 分组名
            material.PEC_,  # 材料名
        ).create(modeler)

        # 选择顶面
        tp.pick_face_from_id(modeler, solid1_down, 1)
        solid2_down = p2s.Extrude(
            "solid2",
            horn_down_comp.name,
            "PEC",
            properties={
                "Mode": ' "Picks"',
                "Height": f' "{horn_length}"',
                "Twist": ' "0.0"',
                "Taper": f' "{taper_angle}"',
                "UsePicksForHeight": ' "False"',
                "DeleteBaseFaceSolid": ' "False"',
                "ClearPickedFace": ' "True"',
            },
        ).create_from_attributes(modeler)
        solid1_down.add(modeler, solid2_down)

        # pick face
        tp.pick_face_from_id(modeler, solid1_down, 5)
        tp.pick_face_from_id(modeler, solid1_down, 8)
        so.advanced_shell(modeler, solid1_down, "Outside", wall_thickness)

        # pick end point
        tp.pick_end_point_from_id(modeler, solid1_down, 16)
        tp.pick_end_point_from_id(modeler, solid1_down, 15)
        tp.pick_end_point_from_id(modeler, solid1_down, 13)

        # define port:
        self._port.create_from_attributes(modeler)

        # clear picks
        tp.clear_all_picks(modeler)

        t1 = time.perf_counter()
        _logger.info(
            "%s",
            f'Waveguide "{self._name}" created, execution time: {common.time_to_string(t1-t0)}',
        )
        return self


class WaveguideHornAntenna(BasicWaveguide):
    def __init__(
        self,
        name: str,
        port_config: Port,
        *,
        taper_angle: Parameter,
        horn_length: Parameter,
        wall_thickness: Parameter,
        waveguide_width: Parameter,
        waveguide_height: Parameter,
        waveguide_length: Parameter,
    ):
        super().__init__(name, port_config)
        self._taper_angle = taper_angle
        self._horn_length = horn_length
        self._wall_thickness = wall_thickness
        self._waveguide_width = waveguide_width
        self._waveguide_height = waveguide_height
        self._waveguide_length = waveguide_length
        return

    def create_waveguide(
        self, modeler: "interface.Model3D"
    ) -> "WaveguideHornAntenna":
        t0 = time.perf_counter()

        horn_comp = component.Component(self._name)

        solid1_down = Brick(
            "solid1",  # 实体名
            f"{self._waveguide_width / -2}",  # xmin
            f"{self._waveguide_width / 2}",  # xmax
            f"{self._waveguide_height / -2}",  # ymin
            f"{self._waveguide_height / 2}",  # ymax
            "0",  # zmin
            f"{self._waveguide_length}",  # zmax
            f"{horn_comp}",  # 分组名
            material.PEC_,  # 材料名
        ).create(modeler)

        # 选择顶面
        tp.pick_face_from_id(modeler, solid1_down, 1)
        solid2_down = p2s.Extrude(
            "solid2",
            horn_comp.name,
            "PEC",
            properties={
                "Mode": ' "Picks"',
                "Height": f' "{self._horn_length}"',
                "Twist": ' "0.0"',
                "Taper": f' "{self._taper_angle}"',
                "UsePicksForHeight": ' "False"',
                "DeleteBaseFaceSolid": ' "False"',
                "ClearPickedFace": ' "True"',
            },
        ).create_from_attributes(modeler)
        solid1_down.add(modeler, solid2_down)

        # 选择外壳面
        tp.pick_face_from_id(modeler, solid1_down, 5)
        tp.pick_face_from_id(modeler, solid1_down, 8)
        so.advanced_shell(modeler, solid1_down, "Outside", self._wall_thickness)

        # pick end point
        tp.pick_end_point_from_id(modeler, solid1_down, 16)
        tp.pick_end_point_from_id(modeler, solid1_down, 15)
        tp.pick_end_point_from_id(modeler, solid1_down, 13)

        # define port:
        self._port.create_from_attributes(modeler)

        # clear picks
        tp.clear_all_picks(modeler)

        t1 = time.perf_counter()
        _logger.info(
            "%s",
            f'Waveguide "{self._name}" created, execution time: {common.time_to_string(t1-t0)}',
        )
        return self
