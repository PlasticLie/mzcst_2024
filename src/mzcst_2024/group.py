"""定义 `Group` 类和与其相关的方法。"""

import logging
import typing
from pathlib import PurePath, PurePosixPath

from . import interface
from .common import NEW_LINE, quoted
from .global_ import BaseObject, Parameter

__all__: list[str] = []

_logger = logging.getLogger(__name__)


class Group(BaseObject):
    """The Group Object lets you define or change the groups. Solids can be
    assigned to groups in order to facilitate changing the properties of
    multiple solids.
    """

    def __init__(
        self,
        name: str,
        path: str,
        type_: typing.Literal["normal", "mesh"],
        *,
        attributes=None,
        vba=None,
    ):
        super().__init__(attributes=attributes, vba=vba)
        self._name = name
        self._path = path
        self._type = type_
        return

    @property
    def name(self) -> str:
        return self._name

    @property
    def path(self) -> str:
        return self._path

    @property
    def type_(self) -> str:
        return self._type

    def add(self, modeler: interface.Model3D) -> "Group":
        """Creates a new group of a give type with the given name.

        Args:
            type_: The type of the group. Possible values are "normal" and "mesh".

        Returns:
            The created Group object.
        """
        self._history.append(
            f'add group "{self._path}:{self._name}" of type "{self._type}"'
        )
        _logger.info("%s", self._history[-1])
        cmd = f'Group.Add "{self._name}", "{self._type}"'
        modeler.add_to_history(self._history[-1], cmd)
        return self

    def delete(self, modeler: interface.Model3D) -> "Group":
        """Deletes an existing group. The solids assigned to this group will lose their assignment."""
        self._history.append(f'delete group "{self._path}:{self._name}"')
        _logger.info("%s", self._history[-1])
        cmd = f'Group.Delete "{self._name}"'
        modeler.add_to_history(self._history[-1], cmd)
        return self

    def rename(self, modeler: interface.Model3D, new_name: str) -> "Group":
        """Changes the name of an existing group.

        Args:
            new_name: The new name of the group.

        Returns:
            The Group object itself.
        """
        self._history.append(
            f'rename group "{self._path}:{self._name}" to "{self._path}:{new_name}"'
        )
        _logger.info("%s", self._history[-1])
        cmd = f'Group.Rename "{self._name}", "{new_name}"'
        modeler.add_to_history(self._history[-1], cmd)
        self._name = new_name
        return self

    def add_item(self, modeler: interface.Model3D, item_name: str) -> "Group":
        """Adds a solid to the group.

        Args:
            item_name: The name of the solid to be added. It can be either the name of the solid itself or the name of a group that contains the solid.

        Returns:
            The Group object itself.
        """
        self._history.append(
            f'add item "{item_name}" to group "{self._path}:{self._name}"'
        )
        _logger.info("%s", self._history[-1])
        cmd = f'Group.AddItem "{item_name}", "{self._name}"'
        modeler.add_to_history(self._history[-1], cmd)
        return self

    def remove_item(
        self, modeler: interface.Model3D, item_name: str
    ) -> "Group":
        """Removes a solid from the group.

        Args:
            item_name: The name of the solid to be removed. It can be either the name of the solid itself or the name of a group that contains the solid.

        Returns:
            The Group object itself.
        """
        self._history.append(
            f'remove item "{item_name}" from group "{self._path}:{self._name}"'
        )
        _logger.info("%s", self._history[-1])
        cmd = f'Group.RemoveItem "{item_name}", "{self._name}"'
        modeler.add_to_history(self._history[-1], cmd)
        return self
