"""提供与`cst.results`交互的接口。

This module allows reading one-dimensional result curves and data points of
CST project files. These results are referred to as “0D/1D Results”.

No running instance of CST Studio Suite is required for data access.

Supported are unpacked and unprotected project files generated with CST Studio
Suite 2023 or CST Studio Suite 2024.

To understand how this module can be used, see the Examples section of the
documentation.

General Notes
-------

This module supports only access to unpacked CST files. A packed CST project
file (generated via “Archive As”) can be extracted by opening it with CST Studio
Suite. If the project has subprojects (see Examples), they need to be unpacked
recursively as well (i.e. by double-clicking on the corresponding subproject
tree entry in Schematic, then saving the parent project).

Protected project files are not supported.

Please also note that access to projects which are being simulated in an open
CST Studio Suite is not supported.

"""

import logging
import numbers
import os

import cst.results
import numpy
from cst.results import get_version_info, print_version_info

# -pylint: disable=no-member


_logger = logging.getLogger(__name__)


class ProjectFile:
    """提供与`cst.results.ProjectFile`的接口。

    This class allows loading a CST file to access its results."""

    def __init__(
        self,
        filepath: os.PathLike | str | None = None,
        allow_interactive: bool = False,
    ):
        """

        Initialize a ProjectFile with a filepath to a CST file. The setting
        `allow_interactive=True` allows accessing a project which can be
        simultaneously opened in CST Studio Suite. In this interactive mode,
        data access can be done after ‘Save’ was triggered in CST Studio Suite.
        If any changes are made in CST Studio Suite to the project without
        saving (e.g. a solver is started), the retrieved data will be outdated
        or ill-formed. It is up to the user to ensure that the project is not in
        an intermediate state.
        """

        self._pf = cst.results.ProjectFile(filepath, allow_interactive)
        _logger.debug(
            "%s",
            f"Initialized ProjectFile with filepath: {filepath}, allow_interactive: {allow_interactive}",
        )

        return

    def __str__(self):
        return str(self._pf)

    def __repr__(self):
        return repr(self._pf)

    @classmethod
    def init(cls, pf: "cst.results.ProjectFile"):
        """_summary_

        Parameters
        ----------
        rm : cst.results.ResultModule
            cst 库的 ProjectFile 对象

        Returns
        -------
        ResultModule
            mzcst 库的接口对象
        """
        _new = cls(pf.filename)
        # _new._pf = pf
        return _new

    @property
    def filename(self) -> str:
        """The filename of the CST project."""
        return self._pf.filename

    def get_3d(self) -> "ResultModule":
        """Get the 3D submodule of a CST project."""
        g3 = self._pf.get_3d()
        return ResultModule.init(g3)

    def get_schematic(self):
        """Get the Schematic submodule of a CST project."""
        gs = self._pf.get_schematic()
        return ResultModule.init(gs)

    def list_subprojects(self) -> list[str]:
        """List tree paths which represent subprojects (i.e. Simulation Projects
        Tasks or Block Simulation Tasks).

        Returns
        -------
        list[str]
            包含子项目的树状路径。
        """
        _logger.info("Listing subprojects")
        return self._pf.list_subprojects()

    def load_subproject(self, subproject_path: str) -> "ProjectFile":
        """Load a subproject from a tree path.

        Returns
        -------
        ProjectFile
            project file object of subproject
        """
        _logger.info("Loading subproject: %s", subproject_path)
        ls = self._pf.load_subproject(subproject_path)
        return ProjectFile.init(ls)


class ResultModule:
    """提供与`cst.results.ResultModule`的接口。

    This class provides an interface to access the 3D or Schematic results
    submodule of a of a CST project.
    """

    def __init__(self):
        self._rm = None
        return

    def __str__(self):
        return str(self._rm)

    def __repr__(self):
        return repr(self._rm)

    @classmethod
    def init(cls, rm: "cst.results.ResultModule"):
        """从 `cst.results.ResultModule` 对象创建 ResultItem 接口。

        Parameters
        ----------
        rm : cst.results.ResultModule
            cst库的ResultModule对象

        Returns
        -------
        ResultModule
            mzcst库的接口对象
        """
        _new = cls()
        _new._rm = rm
        return _new

    def get_all_run_ids(self, max_mesh_passes_only: bool = True) -> list[int]:
        """Get all existing run ids (independent of a tree path).

        Parameters
        ----------
        max_mesh_passes_only : bool, optional
            if `max_mesh_passes_only` is True, this method yields only
        results with the highest mesh pass, by default True

        Returns
        -------
        list[int]
            all existing run ids.
        """
        _logger.info(
            "%s",
            f"Getting all run ids, max_mesh_passes_only={max_mesh_passes_only}",
        )
        return self._rm.get_all_run_ids(max_mesh_passes_only)

    def get_parameter_combination(self, run_id: int) -> dict[str, float]:
        """Return the parameter combination which corresponds to the provided run id.

        Parameters
        ----------
        run_id : int
            _description_

        Returns
        -------
        dict
            _description_
        """
        _logger.info("Getting parameter combination for run id: %d", run_id)
        return self._rm.get_parameter_combination(run_id)

    def get_result_item(
        self, treepath: str, run_id: int = 0, load_impedances: bool = True
    ) -> "ResultItem":
        """Get result of a navigation tree item. The setting `load_impedances=False` omits automatic loading of reference impedances.

        Parameters
        ----------
        treepath : str
            path of result item
        run_id : int, optional
            run id, by default 0
        load_impedances : bool, optional
            if set to `False`, this method omits automatic loading of reference impedances, by default True

        Returns
        -------
        ResultItem
            _description_
        """
        temp: "cst.results.ResultItem" = self._rm.get_result_item(
            treepath, run_id, load_impedances
        )
        return ResultItem.init(temp)

    def get_run_ids(
        self, treepath: str, skip_nonparametric: bool = False
    ) -> list[int]:
        """Get all existing run ids for a tree item.

        Parameters
        ----------
        treepath : str
            _description_
        skip_nonparametric : bool, optional
            if `True`, it enforces run id = 0 to be excluded from the list, by default False

        Returns
        -------
        list[int]
            all existing run ids
        """
        _logger.info(
            "%s",
            f"Getting run ids for treepath: {treepath}, skip_nonparametric={skip_nonparametric}",
        )
        return self._rm.get_run_ids(treepath, skip_nonparametric)

    def get_tree_items(self, filter_: str = "0D/1D") -> list[str]:
        """List navigation tree items.

        Parameters
        ----------
        filter : str, optional
            filter, by default '0D/1D'

        Returns
        -------
        list[str]
            navigation tree items
        """
        _logger.info("Getting tree items with filter: %s", filter_)
        return self._rm.get_tree_items(filter_)


class ResultItem:
    """提供与`cst.results.ResultItem`的接口。

    This class represents the result data of a navigation tree item of a CST
    project for a single parameter combination.
    """

    def __init__(self):
        self._ri = None
        return

    @classmethod
    def init(cls, ri: "cst.results.ResultItem"):
        """从 `cst.results.ResultItem` 对象创建 ResultItem 接口。

        Parameters
        ----------
        rm : cst.results.ResultItem
            cst库的ResultModule对象

        Returns
        -------
        ResultItem
            mzcst库的接口对象
        """
        _new = cls()
        _new._ri = ri
        return _new

    def __str__(self):
        return str(self._ri)

    def __repr__(self):
        return repr(self._ri)

    def get_data(self) -> list[tuple] | float:
        """The data as list of tuples, or a double value."""
        _logger.info("Getting data")
        return self._ri.get_data()

    def get_parameter_combination(self) -> dict[str, float]:
        """The parameter combination which was used to generate the result."""
        _logger.info("Getting parameter combination")
        return self._ri.get_parameter_combination()

    def get_ref_imp_data(self) -> list[complex]:
        """The reference impedance of the result."""
        _logger.info("Getting reference impedance data")
        return self._ri.get_ref_imp_data()

    @property
    def reference_impedance_list(self) -> list[complex]:
        """The reference impedance of the result."""
        return self._ri.get_ref_imp_data()

    def get_xdata(self) -> list[float]:
        """The x-axis of the result."""
        return self._ri.get_xdata()

    @property
    def xdata(self) -> list[float]:
        """The x-axis of the result."""
        return self._ri.get_xdata()

    def get_ydata(self) -> list[complex]:
        """The y-axis of the result."""
        _logger.info("Getting Y data")
        return self._ri.get_ydata()

    @property
    def ydata(self) -> list:
        """The y-axis of the result."""
        return self._ri.get_ydata()

    @property
    def length(self) -> int:
        """The number of points returned by ‘get_ydata’."""
        return self._ri.length

    @property
    def run_id(self) -> int:
        """The run id of the result."""
        return self._ri.run_id

    @property
    def title(self) -> str:
        """The title of the result."""
        return self._ri.title

    @property
    def treepath(self) -> str:
        """The navigation tree path of the result."""
        return self._ri.treepath

    @property
    def xlabel(self) -> str:
        """The x-label of the result."""
        return self._ri.xlabel

    @property
    def ylabel(self) -> str:
        """The y-label of the result."""
        return self._ri.ylabel


if __name__ == "__main__":
    a = cst.results.ProjectFile
    pass
