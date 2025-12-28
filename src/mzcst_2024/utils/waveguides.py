"""常用波导
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

from .. import Parameter, component, interface, material
from .. import profiles_to_shapes as p2s
from .. import shape_operations as so
from .. import transformations_and_picks as tp
from ..common import time_decorator
from ..shapes import Brick
from ..sources_and_ports.hf import Port

_logger = logging.getLogger(__name__)


class WR90:
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
        self.name = name

        self.port = port_config
        return

    @time_decorator
    def create_waveguide(self, modeler: "interface.Model3D") -> "WR90":
        """在给定的建模器中创建WR-90波导。

        Args:
            modeler (interface.Model3D): 建模环境。
        """

        taper_angle = Parameter("11.2")
        horn_length = Parameter("218.16")
        wall_thickness = Parameter("3.78")
        waveguide_width = Parameter("37.38")
        waveguide_height = Parameter("16.38")

        horn_down_comp = component.Component(self.name)

        solid1_down = Brick(
            "solid1",  # 实体名
            (waveguide_width / Parameter(-2)).name,  # xmin
            (waveguide_width / Parameter(2)).name,  # xmax
            (waveguide_height / Parameter(-2)).name,  # ymin
            (waveguide_height / Parameter(2)).name,  # ymax
            "0",  # zmin
            "10.92",  # zmax
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
        self.port.create_from_attributes(modeler)

        # clear picks
        tp.clear_all_picks(modeler)
        return self