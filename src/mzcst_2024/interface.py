"""提供与`cst.interface`的接口。

The `cst.interface` module offers a general interface to the CST Studio Suite.

The cst.interface package provides a python interface that allows to control the
CST Studio Suite. It is possible to connect to a running DesignEnvironnent (main
screen) or start a new one. Once connected the package provides access to CST
projects (`.cst`) which can be opened, closed and saved and provide access to
the associated applications (`prj.model3d`)."""

import logging
import os
from typing import Optional, overload

import cst
import cst.interface

from . import global_

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

    def abort_solver(self, *, timeout: Optional[int] = None) -> None:
        """Aborts the currently running (or paused) solver.

        Args:
            timeout (int, optional): 执行时间限制. Defaults to None.

        Returns:
            None
        """
        return self.model3d.abort_solver(timeout)

    def add_to_history(
        self, header: str, vba_code: str, *, timeout: Optional[int] = None
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

    def get_active_solver_name(self, *, timeout: Optional[int] = None) -> str:
        """Returns the currently active solver name.

        Args:
            timeout (int, optional): _description_. Defaults to None.

        Returns:
            str: _description_
        """
        return self.model3d.get_active_solver_name(timeout=timeout)

    def get_solver_run_info(self, *, timeout: Optional[int] = None) -> dict:
        """Retrieves as dict containing information on the last or current solver run.

        Args:
            timeout (int, optional): _description_. Defaults to None.

        Returns:
            str: _description_
        """
        return self.model3d.get_solver_run_info(timeout=timeout)

    def is_solver_running(self, *, timeout: Optional[int] = None) -> bool:
        """Queries whether the solver is currently running.

        Args:
            timeout (int, optional): _description_. Defaults to None.

        Returns:
            bool: _description_
        """
        return self.model3d.is_solver_running(timeout=timeout)

    def pause_solver(self, *, timeout: Optional[int] = None) -> None:
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

    def resume_solver(self, *, timeout: Optional[int] = None) -> None:
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

    def run_solver(self, *, timeout: Optional[int] = None) -> None:
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

    def start_solver(self, *, timeout: Optional[int] = None) -> None:
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

    def create_object(self, obj: global_.BaseObject) -> None:
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
                obj.create_from_vba(self.model3d)
            except AttributeError:
                _logger.error(
                    "Object %s does not have create_from_attributes or create_from_kwargs method.",
                    obj.__class__.__name__,
                )
        return

    @property
    def solver_info(self) -> dict[str, Optional[str]]:
        r: dict[str, Optional[str]] = {
            "name": self.model3d.get_active_solver_name()
        }
        r.update(self.model3d.get_solver_run_info())
        return r


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
        path: str = "",
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

    @staticmethod
    def new(
        options: Optional[list[str]] = None,
        gui_linux: Optional[bool] = None,
        process_info: Optional[
            "cst.interface.DesignEnvironment.ProcessInfo"
        ] = None,
        env: Optional[dict] = None,
    ) -> "DesignEnvironment":
        """Opens a new DE and connects to it.
        A number of command line `options` may be passed as a list of strings.
        For a list of available options call the `print_command_line_options()` method.
        Use `gui_linux` to control whether the DE should run with or without a GUI in a Linux environment.

        Args:
            options (list[str], optional): 启动选项列表. Defaults to None.
            gui_linux (bool, optional): 在Linux上是否启用GUI. Defaults to None.
            process_info (cst.interface.DesignEnvironment.ProcessInfo, optional): 进程信息. Defaults to None.
            env (dict, optional): 环境变量. Defaults to None.

        Returns:
            DesignEnvironment: 新创建的设计环境实例
        """
        env = cst.interface.DesignEnvironment.new(
            options=options,
            gui_linux=gui_linux,
            process_info=process_info,
            env=env,
        )
        return DesignEnvironment(env)

    @staticmethod
    @overload
    def connect(pid: int) -> "DesignEnvironment":
        """Connects to an existing CST Studio Suite Design Environment
        (main window) given its process ID.

        Args:
            pid (int): 目标CST Studio Suite进程的ID

        Returns:
            DesignEnvironment: 连接到的设计环境实例
        """
        env = cst.interface.DesignEnvironment.connect(pid)
        return DesignEnvironment(env)

    @staticmethod
    @overload
    def connect(tcp_address: str) -> "DesignEnvironment":
        """Connects to an existing CST Studio Suite Design Environment
        (main window) given its TCP address.

        Args:
            tcp_address (str): 目标CST Studio Suite进程的TCP地址

        Returns:
            DesignEnvironment: 连接到的设计环境实例
        """
        env = cst.interface.DesignEnvironment.connect(tcp_address)
        return DesignEnvironment(env)

    @staticmethod
    def connect_to_any() -> "DesignEnvironment":
        """Connects to any existing CST Studio Suite Design Environment
        (main window).

        If you want to connect to a specific DE, use the `connect()` method.

        Returns:
            DesignEnvironment: 连接到的设计环境实例
        """
        env = cst.interface.DesignEnvironment.connect_to_any()
        return DesignEnvironment(env)

    @staticmethod
    def connect_to_any_or_new() -> "DesignEnvironment":
        """Connects to any existing CST Studio Suite Design Environment
        (main window). If none exists, a new instance is started.

        Returns:
            DesignEnvironment: 连接到的设计环境实例
        """
        env = cst.interface.DesignEnvironment.connect_to_any_or_new()
        return DesignEnvironment(env)

    def __init__(
        self, existing_env: Optional[cst.interface.DesignEnvironment] = None
    ):
        """如果不指定已有的设计环境，那就新建一个。

        Args:
            existing_env (cst.interface.DesignEnvironment, optional): 已有的设计环境. Defaults to None.
        """
        if existing_env is None:
            self._env = cst.interface.DesignEnvironment()
        else:
            self._env = existing_env
        pass

    def quiet_mode_enabled(self):
        """Convenience method to turn on quiet mode with a 'with'-statement
        and automatically reset it to the previous state on exiting.

        Returns:
            contextmanager: 上下文管理器
        """
        return self._env.quiet_mode_enabled()

    def quiet_mode_disabled(self):
        """Convenience method to turn off quiet mode with a 'with'-statement
        and automatically reset it to the previous state on exiting.

        Returns:
            contextmanager: 上下文管理器
        """
        return self._env.quiet_mode_disabled()

    def active_project(self) -> Optional[Project]:
        """Returns the currently active project if any.

        Returns:
            Project | None: 当前活动项目
        """
        proj = self._env.active_project()
        if proj is None:
            return None
        return Project(proj)

    def close(self) -> None:
        """Closes the Design Environment.

        Returns:
            None:
        """
        return self._env.close()

    def get_open_project(self, path: str) -> Project:
        """Returns a handle to an already open project with the path given by 
        `path`. 
        
        Raises an exception when there is no project found corresponding to the given path.

        Args:
            path (str): 项目路径

        Returns:
            Project: 已打开的项目
        """
        proj = self._env.get_open_project(path)
        return Project(proj)

    def get_open_projects(self, re_filter: str = ".*") -> list[Project]:
        """Returns a list of currently open projects matching the regular 
        expression filter `re_filter`.

        Returns:
            list[Project]: 当前打开的项目列表
        """
        projs = self._env.get_open_projects(re_filter)
        return [Project(p) for p in projs]

    def has_active_project(self) -> bool:
        """Queries whether there is an active project.

        Returns:
            bool: 是否有活动项目
        """
        return self._env.has_active_project()

    def in_quiet_mode(self) -> bool:
        return self._env.in_quiet_mode()

    def is_connected(self) -> bool:
        return self._env.is_connected()

    def list_open_projects(self) -> list[str]:
        """Returns the paths of the currently open projects.

        Returns:
            list[str]: 当前打开的项目文件名列表
        """
        return self._env.list_open_projects()

    def new_cs(self) -> Project:
        """Creates a new CST Cable Studio project and returns an instance of `Project` pertaining to it."""
        proj = self._env.new_cs()
        return Project(proj)

    def new_ds(self) -> Project:
        """Creates a new CST Design Studio project and returns an instance of `Project` pertaining to it."""
        proj = self._env.new_ds()
        return Project(proj)

    def new_ems(self) -> Project:
        """Creates a new CST EM Studio project and returns an instance of `Project` pertaining to it."""
        proj = self._env.new_ems()
        return Project(proj)

    def new_fd3d(self) -> Project:
        """Creates a new Filter Designer 3D project and returns an instance of `Project` pertaining to it."""
        proj = self._env.new_fd3d()
        return Project(proj)

    def new_mps(self) -> Project:
        """Creates a new CST Mphysics Studio project and returns an instance of `Project` pertaining to it."""
        proj = self._env.new_mps()
        return Project(proj)

    def new_mws(self) -> Project:
        """Creates a new CST Microwave Studio project and returns an instance of `Project` pertaining to it."""
        proj = self._env.new_mws()
        return Project(proj)

    def new_pcbs(self) -> Project:
        """Creates a new CST PCB Studio project and returns an instance of `Project` pertaining to it."""
        proj = self._env.new_pcbs()
        return Project(proj)

    def new_project(self, project_type: cst.interface.ProjectType) -> Project:
        """Creates a new CST project of the specified type and returns an instance of `Project` pertaining to it.

        Args:
            project_type (cst.interface.ProjectType): 项目类型
        Returns:
            Project: 新创建的项目
        """
        proj = self._env.new_project(project_type)
        return Project(proj)

    def new_ps(self) -> Project:
        """Creates a new CST Particle Studio project and returns an instance of `Project` pertaining to it."""
        proj = self._env.new_ps()
        return Project(proj)

    def open_project(self, path: str) -> Project:
        """Opens the CST project given by `path` and returns an instance of `Project` pertaining to it.

        Args:
            path (str): 项目路径
        Returns:
            Project: 打开的项目
        """
        proj = self._env.open_project(path)
        return Project(proj)

    @property
    def pid(self) -> int:
        return self._env.pid

    @staticmethod
    def print_command_line_options() -> None:
        """Prints the available command line options which can be used with `new()`.

        Returns:
            None:
        """
        return cst.interface.DesignEnvironment.print_command_line_options()

    @property
    def command_line_options(self) -> str:
        """Prints the available command line options which can be used with `new()`."""
        return cst.interface.DesignEnvironment.print_command_line_options()

    @staticmethod
    def print_version() -> str:
        """Prints the version of the CST Studio Suite installation.

        Returns:
            None:
        """
        return cst.interface.DesignEnvironment.print_version()

    def set_quiet_mode(self, flag: bool) -> None:
        """When `flag` is set to True message boxes are suppressed.

        Please note: Dialog boxes which require user input cannot be suppressed.

        Args:
            flag (bool): 是否启用安静模式
        Returns:
            None:
        """
        return self._env.set_quiet_mode(flag)

    @staticmethod
    def version() -> str:
        """Return the version string of the current DE.

        Returns:
            str: 版本字符串
        """
        return cst.interface.DesignEnvironment.version()
