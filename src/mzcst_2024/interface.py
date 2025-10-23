"""提供与`cst.interface`的接口。

The `cst.interface` module offers a general interface to the CST Studio Suite.

The cst.interface package provides a python interface that allows to control the
CST Studio Suite. It is possible to connect to a running DesignEnvironnent (main
screen) or start a new one. Once connected the package provides access to CST
projects (`.cst`) which can be opened, closed and saved and provide access to
the associated applications (`prj.model3d`)."""

import logging
import os
from typing import Dict, List, Union

import cst
import cst.interface

from . import _global

_logger = logging.getLogger(__name__)


class Model3D:
    """与`cst.interface.Model3D`的接口。

    This class provides an interface to the 3D Model.
    """

    def __init__(self, modeler: "cst.interface.Model3D"):
        """初始化

        Args:
            modeler (cst.interface.Model3D): 建模器对象。
        """
        self.model3d = modeler
        return

    def abort_solver(self, *, timeout: int = None) -> None:
        """Aborts the currently running (or paused) solver.

        Args:
            timeout (int, optional): 执行时间限制. Defaults to None.

        Returns:
            None
        """
        return self.model3d.abort_solver(timeout)

    def add_to_history(
        self, header: str, vba_code: str, *, timeout: int = None
    ) -> None:
        """AddToHistory creates a new history block in the modeler with the
        given header-name and executes the `vba_code`

        Args:
            header (str): 历史记录标题
            vba_code (str): VBA代码
            timeout (int, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        return self.model3d.add_to_history(header, vba_code, timeout=timeout)

    def get_active_solver_name(self, *, timeout: int = None) -> str:
        """Returns the currently active solver name.

        Args:
            timeout (int, optional): _description_. Defaults to None.

        Returns:
            str: _description_
        """
        return self.model3d.get_active_solver_name(timeout=timeout)

    def is_solver_running(self, *, timeout: int = None) -> bool:
        """Queries whether the solver is currently running.

        Args:
            timeout (int, optional): _description_. Defaults to None.

        Returns:
            bool: _description_
        """
        return self.model3d.is_solver_running(timeout=timeout)

    def pause_solver(self, *, timeout: int = None) -> None:
        """Pause the currently running solver.

        Parameters
        ----------
        timeout : int, optional
            _description_, by default None

        Returns
        -------
        None
        """
        return self.model3d.pause_solver(timeout=timeout)

    def resume_solver(self, *, timeout: int = None) -> None:
        """Resume the currently paused solver.

        Parameters
        ----------
        timeout : int, optional
            _description_, by default None

        Returns
        -------
        None
        """
        return self.model3d.resume_solver(timeout=timeout)

    def run_solver(self, *, timeout: int = None) -> None:
        """Runs the currently selected solver until it finishes. In case of an error a RunTimeError exception will be thrown.

        Parameters
        ----------
        timeout : int, optional
            _description_, by default None

        Returns
        -------
        None
        """
        return self.model3d.run_solver(timeout=timeout)

    def start_solver(self, *, timeout: int = None) -> None:
        """Starts the currently selected solver asynchronously and gives back
        control to the calling script. It does not wait for the solver to
        finish, use in combination with `is_solver_running()`.

        Args:
            timeout (int, optional): 执行指令的限制时间，只接受整数，尚不清楚时间单位是什么. Defaults to None.

        Returns:
            None:
        """
        _logger.info("Starting solver asynchronously.")
        return self.model3d.start_solver(timeout=timeout)

    def create_object(self, obj: _global.BaseObject) -> None:
        """Creates a new object in the 3D modeler.

        Args:
            obj (_global.BaseObject): The object to create in the modeler.

        Returns:
            None
        """

        try:
            obj.create_from_attributes(self.model3d)
        except AttributeError:
            _logger.warning(
                "Object %s does not have create_from_attributes method, trying create_from_kwargs.",
                obj.__class__.__name__,
            )
            try:
                obj.create_from_kwargs(self.model3d)
            except AttributeError:
                _logger.error(
                    "Object %s does not have create_from_attributes or create_from_kwargs method.",
                    obj.__class__.__name__,
                )
        return


class Schematic:
    def __init__(self):
        pass


class InterfacePCBS:
    def __init__(self):
        pass


class Project:
    """与`cst.interface.Project`的接口

    Provides an interface to live CST projects. Offers capabilities to save and
    close projects, but also carries the associated interfaces to various
    applications.
    """

    def __init__(self, p: "cst.interface.Project"):
        self._proj = p
        self._model3d = Model3D(self._proj.model3d)
        self._dsn_env = DesignEnvironment(self._proj.design_environment)
        pass

    @property
    def model3d(self) -> Model3D:
        """Gives access to the 3D model (Model3D) associated with the project if
        it exists. Is None when there is no associated modeler.

        Returns:
            Model3D: the 3D model (Model3D) associated with the project
        """
        return self._model3d

    @property
    def design_environment(self) -> "DesignEnvironment":
        """The instance of the `DesignEnvironment` in which this Project is open"""
        return self._dsn_env

    def activate(self) -> None:
        """Makes this project the currently active project.

        Returns:
            None:
        """
        return self._proj.activate()

    def close(self) -> None:
        """Closes the project without saving.

        Returns:
            None:
        """
        return self._proj.close()

    def filename(self) -> str:
        """Returns the current filename of the project.

        Returns:
            str: current filename
        """
        return self._proj.filename()

    def folder(self) -> str:
        """Returns the folder pertaining to the project.

        Returns:
            str: folder name
        """
        return self._proj.folder()

    def get_messages(self):
        """Returns messages from the Messages Window if any."""
        return self._proj.get_messages()

    def save(
        self,
        path: os.PathLike = "",
        include_results: bool = True,
        allow_overwrite: bool = False,
    ) -> None:
        """Saves the project to the specified path and optionally includes the
        results. If no path is given (default) then the current filename will be
        used.

        Args:
            path (os.PathLike, optional): 包含文件名的绝对路径，留空则保持当前文件名. Defaults to "".
            include_results (bool, optional): 是否包含结果. Defaults to True.
            allow_overwrite (bool, optional): 是否允许覆盖. Defaults to False.

        Returns:
            None:
        """
        self._proj.save(path, include_results, allow_overwrite)
        _logger.info("project saved: %s", path)
        return


class DesignEnvironment:
    """与`cst.interface.DesignEnvironment`的接口。

    This class provides an interface to the CST Studio Suite main frontend.
    It allows to connect to, and open new CST Studio Suite instances.
    Furthermore it allows to open or create `.cst` projects.
    """

    def __init__(self, existing_env: cst.interface.DesignEnvironment = None):
        """如果不指定已有的设计环境，那就新建一个。

        Args:
            existing_env (cst.interface.DesignEnvironment, optional): 已有的设计环境. Defaults to None.
        """
        if existing_env is None:
            self._env = cst.interface.DesignEnvironment()
        else:
            self._env = existing_env
        pass

    def new_mws(self) -> Project:
        proj = self._env.new_mws()
        return Project(proj)
