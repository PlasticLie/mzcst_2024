"""定义 `Group` 类和与其相关的方法。"""

import logging
import typing
from pathlib import PurePath, PurePosixPath

from . import interface
from .common import NEW_LINE, quoted
from .global_ import BaseObject, CSTPath, Parameter

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
        path: str | CSTPath,
        type_: typing.Literal["normal", "mesh"],
        *,
        attributes=None,
        vba=None,
    ):
        super().__init__(attributes=attributes, vba=vba)
        self._name: str = name
        if isinstance(path, CSTPath):
            path = str(path)
        self._path: str = path
        self._type: str = type_
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

    @property
    def full_name(self) -> str:
        return f"{self._path}:{self._name}"

    def add(self, modeler: interface.Model3D) -> "Group":
        """Creates a new group of a give type with the given name.

        Args:
            type_: The type of the group. Possible values are "normal" and "mesh".

        Returns:
            The created Group object.
        """
        self._history.append(
            f'add group "{self.full_name}" of type "{self._type}"'
        )
        _logger.info("%s", self._history[-1])
        cmd = f'Group.Add "{self.full_name}", "{self._type}"'
        modeler.add_to_history(self._history[-1], cmd)
        return self

    def delete(self, modeler: interface.Model3D) -> "Group":
        """Deletes an existing group. The solids assigned to this group will lose their assignment."""
        self._history.append(f'delete group "{self.full_name}"')
        _logger.info("%s", self._history[-1])
        cmd = f'Group.Delete "{self.full_name}"'
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
            f'rename group "{self.full_name}" to "{self._path}:{new_name}"'
        )
        _logger.info("%s", self._history[-1])
        cmd = f'Group.Rename "{self.full_name}", "{self._path}:{new_name}"'
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
            f'add item "{item_name}" to group "{self.full_name}"'
        )
        _logger.info("%s", self._history[-1])
        cmd = f'Group.AddItem "{item_name}", "{self.full_name}"'
        modeler.add_to_history(self._history[-1], cmd)
        return self

    def remove_item(
        self, modeler: interface.Model3D, item_name: str
    ) -> "Group":
        """Removes a solid from the group.

        Args:
            modeler: The modeler interface used to interact with the 3D model.
            item_name: The name of the solid to be removed. It can be either the name of the solid itself or the name of a group that contains the solid.

        Returns:
            The Group object itself.
        """
        self._history.append(
            f'remove item "{item_name}" from group "{self.full_name}"'
        )
        _logger.info("%s", self._history[-1])
        cmd = f'Group.RemoveItem "{item_name}", "{self.full_name}"'
        modeler.add_to_history(self._history[-1], cmd)
        return self


def new_folder(modeler: interface.Model3D, path: str | CSTPath) -> None:
    """Creates a new group folder. The folder can be used to organize groups in the navigation tree.

    Parameters
    ----------
    modeler : interface.Model3D
        The modeler interface used to interact with the 3D model.
    path : str | CSTPath
        The path where the new folder will be created. The path should be in the format `"folder1/folder2/.../folderN"`. If the path already exists, no new folder will be created.

    Returns
    -------
        None
    """
    if isinstance(path, CSTPath):
        path = str(path)
    cmd = f'Group.NewFolder "{path}"'
    modeler.add_to_history(f'create new group folder "{path}"', cmd)
    return


def delete_folder(modeler: interface.Model3D, path: str | CSTPath) -> None:
    """Deletes an existing group folder. The solids assigned to the groups in this folder will lose their assignment.

    Parameters
    ----------
    modeler : interface.Model3D
        The modeler interface used to interact with the 3D model.
    path : str | CSTPath
        The path of the folder to be deleted. The path should be in the format `"folder1/folder2/.../folderN"`. If the path does not exist, no folder will be deleted.

    Returns
    -------
        None
    """
    if isinstance(path, CSTPath):
        path = str(path)
    cmd = f'Group.DeleteFolder "{path}"'
    modeler.add_to_history(f'delete group folder "{path}"', cmd)
    return


def rename_folder(
    modeler: interface.Model3D, old_path: str | CSTPath, new_path: str | CSTPath
) -> None:
    """Renames an existing group folder.

    Parameters
    ----------
    modeler : interface.Model3D
        The modeler interface used to interact with the 3D model.
    old_path : str | CSTPath
        The current path of the folder to be renamed. The path should be in the format `"folder1/folder2/.../folderN"`. If the path does not exist, no folder will be renamed.
    new_path : str | CSTPath
        The new path of the folder after renaming. The path should be in the format `"folder1/folder2/.../folderN"`. If a folder with the new path already exists, no folder will be renamed.

    Returns
    -------
        None
    """
    if isinstance(old_path, CSTPath):
        old_path = str(old_path)
    if isinstance(new_path, CSTPath):
        new_path = str(new_path)
    cmd = f'Group.RenameFolder "{old_path}", "{new_path}"'
    modeler.add_to_history(
        f'rename group folder from "{old_path}" to "{new_path}"', cmd
    )
    return
