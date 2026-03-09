"""Classes for construction curves."""

import logging
import typing

from . import interface
from .global_ import BaseObject

_logger = logging.getLogger(__name__)


class Curve(BaseObject):
    """This object is used to apply operations on curves and curve items."""

    def __init__(
        self,
        name: str,
    ):
        super().__init__()
        self._name: str = name
        return

    @property
    def name(self) -> str:
        return self._name

    def create(self, modeler: interface.Model3D) -> "Curve":
        """Creates a new curve with the given name.

        Args:
            modeler (interface.Model3D): The modeler interface used to interact with the 3D model.

        Returns:
            Curve: The created Curve object.
        """
        cmd = f'Curve.NewCurve "{self._name}"'
        self._history.append(f'create curve "{self._name}"')
        modeler.add_to_history(self._history[-1], cmd)
        _logger.info(self._history[-1])
        return self

    def rename(self, modeler: interface.Model3D, new_name: str) -> "Curve":
        """Changes the name of an existing curve.

        Args:
            modeler (interface.Model3D): The modeler interface used to interact with the 3D model.
            new_name (str): The new name of the curve.

        Returns:
            The Curve object itself.
        """
        self._history.append(f'rename curve "{self._name}" to "{new_name}"')
        _logger.info(self._history[-1])
        cmd = f'Curve.RenameCurve "{self._name}", "{new_name}"'
        modeler.add_to_history(self._history[-1], cmd)
        self._name = new_name
        return self

    def delete(self, modeler: interface.Model3D) -> "Curve":
        """Deletes an existing curve.

        Args:
            modeler (interface.Model3D): The modeler interface used to interact with the 3D model.

        Returns:
            The Curve object itself.
        """
        self._history.append(f'delete curve "{self._name}"')
        _logger.info(self._history[-1])
        cmd = f'Curve.DeleteCurve "{self._name}"'
        modeler.add_to_history(self._history[-1], cmd)
        return self
