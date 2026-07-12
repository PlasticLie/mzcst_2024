"""定义 `Component` 类和与其相关的方法。"""

import logging
import typing

from . import interface
from .common import NEW_LINE, quoted
from .global_ import BaseObject, CSTPath, Parameter

__all__: list[str] = []

_logger = logging.getLogger(__name__)


class Component(BaseObject):
    """The Component Object lets you define or change components. Each solid is
    sorted into a component.
    """

    def __init__(self, name: str | CSTPath):
        super().__init__()
        self._name = CSTPath(name)
        return

    @classmethod
    def delete_all_empty_components(cls, modeler: interface.Model3D):
        """Deletes all empty components."""
        title = "Deletes all empty components."
        cmd = "Component.DeleteAllEmptyComponents"
        modeler.add_to_history(title, cmd)
        _logger.info("%s", title)
        return

    @classmethod
    def hide(cls, modeler: interface.Model3D):
        """Hides the currently selected objects."""
        title = "Hides the currently selected objects."
        cmd = "Component.Hide"
        modeler.add_to_history(title, cmd)
        _logger.info("%s", title)
        return

    @classmethod
    def show(cls, modeler: interface.Model3D):
        """Shows the currently selected objects."""
        title = "Shows the currently selected objects."
        cmd = "Component.Show"
        modeler.add_to_history(title, cmd)
        _logger.info("%s", title)
        return

    @classmethod
    def hide_unselected(cls, modeler: interface.Model3D):
        """Hides the currently not selected objects."""
        title = "Hides the currently not selected objects."
        cmd = "Component.HideUnselected"
        modeler.add_to_history(title, cmd)
        _logger.info("%s", title)
        return

    @classmethod
    def show_unselected(cls, modeler: interface.Model3D):
        """Shows the currently not selected objects."""
        title = "Shows the currently not selected objects."
        cmd = "Component.ShowUnselected"
        modeler.add_to_history(title, cmd)
        _logger.info("%s", title)
        return

    @classmethod
    def show_all(cls, modeler: interface.Model3D):
        """Shows all hideable objects."""
        title = "Shows all hideable objects."
        cmd = "Component.ShowAll"
        modeler.add_to_history(title, cmd)
        _logger.info("%s", title)
        return

    @classmethod
    def hide_all(cls, modeler: interface.Model3D):
        """Hides or shows all hideable objects."""
        title = "Hides or shows all hideable objects."
        cmd = "Component.HideAll"
        modeler.add_to_history(title, cmd)
        _logger.info("%s", title)
        return

    @classmethod
    def hide_all_ports(cls, modeler: interface.Model3D):
        """Hides all ports."""
        title = "Hides all ports."
        cmd = "Component.HideAllPorts"
        modeler.add_to_history(title, cmd)
        _logger.info("%s", title)
        return

    @classmethod
    def show_all_ports(cls, modeler: interface.Model3D):
        """Shows all ports."""
        title = "Shows all ports."
        cmd = "Component.ShowAllPorts"
        modeler.add_to_history(title, cmd)
        _logger.info("%s", title)
        return

    @classmethod
    def hide_all_field_sources(cls, modeler: interface.Model3D):
        """Hides all field sources."""
        title = "Hides all field sources."
        cmd = "Component.HideAllFieldSources"
        modeler.add_to_history(title, cmd)
        _logger.info("%s", title)
        return

    @classmethod
    def show_all_field_sources(cls, modeler: interface.Model3D):
        """Shows all field sources."""
        title = "Shows all field sources."
        cmd = "Component.ShowAllFieldSources"
        modeler.add_to_history(title, cmd)
        _logger.info("%s", title)
        return

    @classmethod
    def hide_all_lumped_elements(cls, modeler: interface.Model3D):
        """Hides all lumped elements."""
        title = "Hides all lumped elements."
        cmd = "Component.HideAllLumpedElements"
        modeler.add_to_history(title, cmd)
        _logger.info("%s", title)
        return

    @classmethod
    def show_all_lumped_elements(cls, modeler: interface.Model3D):
        """Shows all lumped elements."""
        title = "Shows all lumped elements."
        cmd = "Component.ShowAllLumpedElements"
        modeler.add_to_history(title, cmd)
        _logger.info("%s", title)
        return

    @classmethod
    def hide_all_wires(cls, modeler: interface.Model3D):
        """Hides all wires."""
        title = "Hides all wires."
        cmd = "Component.HideAllWires"
        modeler.add_to_history(title, cmd)
        _logger.info("%s", title)
        return

    @classmethod
    def show_all_wires(cls, modeler: interface.Model3D):
        """Shows all wires."""
        title = "Shows all wires."
        cmd = "Component.ShowAllWires"
        modeler.add_to_history(title, cmd)
        _logger.info("%s", title)
        return

    @classmethod
    def hide_all_dielectric(cls, modeler: interface.Model3D):
        """Hides all dielectric."""
        title = "Hides all dielectric."
        cmd = "Component.HideAllDielectric"
        modeler.add_to_history(title, cmd)
        _logger.info("%s", title)
        return

    @classmethod
    def show_all_dielectric(cls, modeler: interface.Model3D):
        """Shows all dielectric."""
        title = "Shows all dielectric."
        cmd = "Component.ShowAllDielectric"
        modeler.add_to_history(title, cmd)
        _logger.info("%s", title)
        return

    @classmethod
    def hide_all_metals(cls, modeler: interface.Model3D):
        """Hides all metals."""
        title = "Hides all metals."
        cmd = "Component.HideAllMetals"
        modeler.add_to_history(title, cmd)
        _logger.info("%s", title)
        return

    @classmethod
    def show_all_metals(cls, modeler: interface.Model3D):
        """Shows all metals."""
        title = "Shows all metals."
        cmd = "Component.ShowAllMetals"
        modeler.add_to_history(title, cmd)
        _logger.info("%s", title)
        return

    @property
    def name(self) -> str:
        return str(self._name)

    @property
    def path(self) -> CSTPath:
        return self._name

    def __str__(self):
        return str(self._name)

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.name}")'

    def rename(
        self, modeler: interface.Model3D, new_name: str | CSTPath
    ) -> "Component":
        """重命名Component，不建议使用，脚本有问题的话反正都会直接重跑的。

        Args:
            modeler (interface.Model3D): 建模器
            new_name (str | CSTPath): 新的名字

        Returns:
            Component: self
        """
        cmd = f'Component.Rename "{self._name}" "{new_name}"'
        self._history.append(f'rename component "{self._name}" to "{new_name}"')
        modeler.add_to_history(self._history[-1], cmd)
        self._name = CSTPath(new_name)
        _logger.info("%s", self._history[-1])
        return self

    def create(
        self,
        modeler: interface.Model3D,
    ) -> "Component":
        """创建 Component。

        实际上不创建也不影响建模。创建实体时会顺带创建不存在的 Component。

        Args:
            modeler (interface.Model3D): 建模器

        Returns:
            Component: self
        """
        sCommand = [f'Component.New "{self.name}"']
        cmd = NEW_LINE.join(sCommand)
        self._history.append(f"new component: {self.name}")
        modeler.add_to_history(self._history[-1], cmd)
        _logger.info("%s", self._history[-1])
        return self

    def delete(
        self,
        modeler: "interface.Model3D",
    ) -> "Component":
        """在CST中删除当前Component，不建议直接在脚本中使用。

        Args:
            modeler (interface.Model3D): 建模器。

        Returns:
            Component: self
        """
        sCommand = [f'Component.Delete "{self.name}"']
        cmd = NEW_LINE.join(sCommand)
        self._history.append(f"delete component: {self.name}")
        modeler.add_to_history(self._history[-1], cmd)
        _logger.info("%s", self._history[-1])
        return self

    def hide_component(self, modeler: interface.Model3D) -> "Component":
        """Hides all shapes within this component and its sub components.

        Args:
            modeler (interface.Model3D): 目标建模器。

        Returns:
            Component: self
        """
        title = f'hide component "{self._name}"'
        cmd = f'Component.HideComponent "{self._name}"'
        modeler.add_to_history(title, cmd)
        _logger.info("%s", title)
        return self

    def show_component(self, modeler: interface.Model3D) -> "Component":
        """Shows all shapes within this component and its sub components.

        Args:
            modeler (interface.Model3D): 目标建模器。

        Returns:
            Component: self
        """
        title = f'show component "{self._name}"'
        cmd = f'Component.ShowComponent "{self._name}"'
        modeler.add_to_history(title, cmd)
        _logger.info("%s", title)
        return self

    def create_sub_component(
        self,
        modeler: interface.Model3D,
        sub_component_name: str | typing.Iterable[str],
    ) -> "Component":
        """创建子组件。

        Args:
            modeler (interface.Model3D): 建模器。
            sub_component_name (str): 子组件名称。

        Returns:
            Component: 新创建的子组件。
        """
        if isinstance(sub_component_name, str):
            new_comp_name = "/".join([self._name, sub_component_name])
        elif isinstance(sub_component_name, typing.Iterable):
            new_comp_name = join([self._name, *sub_component_name])
        else:
            raise TypeError(
                f"sub_component_name must be str or Iterable[str], got {type(sub_component_name)}"
            )

        return Component(new_comp_name).create(modeler)


def join(iterable: typing.Iterable[str]) -> str:
    r = "/".join(iterable)
    return r


if __name__ == "__main__":
    print(join(["fuck", "shit"]))
    pass
