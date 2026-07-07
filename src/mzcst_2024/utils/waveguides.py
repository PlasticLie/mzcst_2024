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

from .. import Parameter, common, component, interface, material, math_
from .. import profiles_to_shapes as p2s
from .. import shape_operations as so
from .. import transformations_and_picks as tp
from ..common import time_decorator
from ..shapes import Brick
from ..sources_and_ports.hf import Port

_logger = logging.getLogger(__name__)


class BasicWaveguideHornAntenna(abc.ABC):

    wall_thickness = Parameter(1.5)  # 壁厚

    waveguide_width = Parameter(0)  # 波导宽度
    waveguide_height = Parameter(0)  # 波导高度
    waveguide_length = Parameter(0)  # 波导长度

    total_length = Parameter(0)  # 天线总长度

    aperture_width = Parameter(0)  # 天线口径宽度
    aperture_height = Parameter(0)  # 天线口径高度

    # taper_angle = Parameter(0)  # 喇叭角度

    @property
    def taper_angle(self) -> Parameter:
        a1 = math_.atan2D(
            self.aperture_width - self.waveguide_width, 2 * self.horn_length
        )
        a2 = math_.atan2D(
            self.aperture_height - self.waveguide_height, 2 * self.horn_length
        )
        return (a1 + a2) / 2

    @property
    def horn_length(self) -> Parameter:
        return self.total_length - self.waveguide_length

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
    ) -> "BasicWaveguideHornAntenna":
        """在给定的建模器中创建波导。

        Args:
            modeler (interface.Model3D): 建模环境。
        """
        t0 = time.perf_counter()

        horn_down_comp = component.Component(self._name)

        solid1_down = Brick(
            "solid1",  # 实体名
            f"{self.waveguide_width / (-2)}",  # xmin
            f"{self.waveguide_width / (2)}",  # xmax
            f"{self.waveguide_height / (-2)}",  # ymin
            f"{self.waveguide_height / (2)}",  # ymax
            "0",  # zmin
            f"{self.waveguide_length}",  # zmax
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
                "Height": f' "{self.horn_length}"',
                "Twist": ' "0.0"',
                "Taper": f' "{self.taper_angle}"',
                "UsePicksForHeight": ' "False"',
                "DeleteBaseFaceSolid": ' "False"',
                "ClearPickedFace": ' "True"',
            },
        ).create_from_attributes(modeler)
        solid1_down.add(modeler, solid2_down)

        # pick face
        tp.pick_face_from_id(modeler, solid1_down, 5)
        tp.pick_face_from_id(modeler, solid1_down, 8)
        so.advanced_shell(modeler, solid1_down, "Outside", self.wall_thickness)

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
        pass


class WR90(BasicWaveguideHornAntenna):
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


class WR159(BasicWaveguideHornAntenna):
    """WR159(BJ58)标准增益喇叭天线, 4.64-7.05GHz, 增益15dB, FDP58矩形平法兰"""

    waveguide_width = Parameter(40.4)
    waveguide_height = Parameter(20.2)
    waveguide_length = Parameter(20)

    total_length = Parameter(250)

    aperture_width = Parameter(149.2)
    aperture_height = Parameter(104.1)

    def __init__(self, name: str, port_config: Port):
        super().__init__(name, port_config)
        return

    def create_waveguide(self, modeler: "interface.Model3D") -> "RWHA159_15":
        super().create_waveguide(modeler)
        return self


class PEWAN090_20(BasicWaveguideHornAntenna):
    """WR90标准增益喇叭天线|专业型, 8.2-12.4GHz, 增益20dB, FDP38矩形平法兰"""

    waveguide_width = Parameter(37.38)
    waveguide_height = Parameter(16.38)
    waveguide_length = Parameter(10.92)

    total_length = Parameter(229.08)

    aperture_width = Parameter(111.8)
    aperture_height = Parameter(82.9)

    @property
    def taper_angle(self) -> Parameter:
        return Parameter(11.2)

    def __init__(self, name: str, port_config: Port):
        super().__init__(name, port_config)
        return

    def create_waveguide(self, modeler: "interface.Model3D") -> "PEWAN090_20":
        super().create_waveguide(modeler)
        return self


class RWHA187_10(BasicWaveguideHornAntenna):
    """WR187(BJ48)标准增益喇叭天线|专业型, 3.94-5.99GHz, 增益10dB, FDP48矩形平法兰"""

    waveguide_width = Parameter(47.5)
    waveguide_height = Parameter(22.15)
    waveguide_length = Parameter(15)

    total_length = Parameter(110)

    aperture_width = Parameter(98)
    aperture_height = Parameter(73)

    def __init__(self, name: str, port_config: Port):
        super().__init__(name, port_config)
        return

    def create_waveguide(self, modeler: "interface.Model3D") -> "RWHA187_10":
        super().create_waveguide(modeler)
        return self


class RWHA187_20(BasicWaveguideHornAntenna):
    """WR187(BJ48)标准增益喇叭天线|专业型, 3.94-5.99 GHz, 增益20dB, FDP48矩形平法兰"""

    waveguide_width = Parameter(47.5)
    waveguide_height = Parameter(22.15)
    waveguide_length = Parameter(40)

    total_length = Parameter(440)

    aperture_width = Parameter(280)
    aperture_height = Parameter(212)

    def __init__(self, name: str, port_config: Port):
        super().__init__(name, port_config)
        return

    def create_waveguide(self, modeler: "interface.Model3D") -> "RWHA187_20":
        super().create_waveguide(modeler)
        return self


class RWHA159_10(BasicWaveguideHornAntenna):
    """WR159(BJ58)标准增益喇叭天线, 4.64-7.05GHz, 增益10dB, FDP58矩形平法兰"""

    waveguide_width = Parameter(40.4)
    waveguide_height = Parameter(20.2)
    waveguide_length = Parameter(20)

    total_length = Parameter(100)

    aperture_width = Parameter(87)
    aperture_height = Parameter(67)

    def __init__(self, name: str, port_config: Port):
        super().__init__(name, port_config)
        return

    def create_waveguide(self, modeler: "interface.Model3D") -> "RWHA159_10":
        super().create_waveguide(modeler)
        return self


class RWHA159_15(BasicWaveguideHornAntenna):
    """WR159(BJ58)标准增益喇叭天线, 4.64-7.05GHz, 增益15dB, FDP58矩形平法兰"""

    waveguide_width = Parameter(40.4)
    waveguide_height = Parameter(20.2)
    waveguide_length = Parameter(20)

    total_length = Parameter(177)

    aperture_width = Parameter(149.2)
    aperture_height = Parameter(104.1)

    def __init__(self, name: str, port_config: Port):
        super().__init__(name, port_config)
        return

    def create_waveguide(self, modeler: "interface.Model3D") -> "RWHA159_15":
        super().create_waveguide(modeler)
        return self


class RWHA159_20(BasicWaveguideHornAntenna):
    """WR159(BJ58)标准增益喇叭天线, 4.64-7.05GHz, 增益20dB, FDP58矩形平法兰"""

    waveguide_width = Parameter(40.4)
    waveguide_height = Parameter(20.2)
    waveguide_length = Parameter(20)

    total_length = Parameter(400)

    aperture_width = Parameter(245)
    aperture_height = Parameter(175)

    def __init__(self, name: str, port_config: Port):
        super().__init__(name, port_config)
        return

    def create_waveguide(self, modeler: "interface.Model3D") -> "RWHA159_20":
        super().create_waveguide(modeler)
        return self


class WaveguideHornAntenna(BasicWaveguideHornAntenna):
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
        waveguide_length: Parameter = Parameter(20),
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
