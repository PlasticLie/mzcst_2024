"""实现与CST 2024交互的接口。包括`cst.interface`、`cst.results`、`cst.eda`、
`cst.asymptotic`、`cst.radar`、`cst.units`。


开发本包的主要目的是：规避CST内置Python接口的类型提示缺失问题。

使用本包后就不再需要直接调用官方的`cst`包。

至少本包内其他模块都通过本模块的接口间接与CST交互。

注意：本模块基于 `Python 3.10.16`、`CST Studio Suite 2024 SP5` 环境开发和调试，未在
其它环境测试过。


CST Python Libraries
====================
Some features of the CST Studio Suite tools can be controlled via CST Python
Libraries.

Overview
--------------------
The cst package provides a Python interface to the CST Studio Suite.

- `cst.interface` - Allows controlling a running CST Studio Suite.
- `cst.results` - Provides access to 0D/1D Results of a cst file.
- `cst.eda` - Provides an interface to a Printed Circuit Board (PCB).
- `cst.asymptotic` - Provides an interface to the Asymptotic Solver.
- `cst.radar` - Provides routines for automotive RADAR post processing.
- `cst.units` - Provides methods to work with units supported by CST Studio Suite.

What’s New in This Version
--------------------
Support for Python 3.6.x (64-bit) and Python 3.7.x (64-bit) is deprecated and
will be removed in the next CST Studio Suite release.

New package cst.radar available.

New package cst.units available.

cst.results opens project files generated with CST Studio Suite 2023 or CST
Studio Suite 2024.

cst.results available as separately installable wheel.

Setup
====================
Bundled Python interpreter
--------------------
The CST Studio Suite installation comes with Python 3.9 (64-bit), which requires
no further setup to start using it with the CST Python Libraries. Various
packages like numpy and scipy are pre-installed.

Custom Python interpreter
--------------------
The CST Python Libraries can also be used from external Python environments. We
strive to support all the Python versions that have not reached the end-of-life
as indicated here and were released before the release of this CST Studio Suite
version. The items marked as deprecated in the list below will be removed in the
next CST Studio Suite release. Please upgrade your Python interpreter
accordingly and avoid using the deprecated versions.

Supported Python versions:

- Python 3.11.x (64-bit)
- Python 3.10.x (64-bit)
- Python 3.9.x (64-bit)
- Python 3.8.x (64-bit)
- Python 3.7.x (64-bit) (end-of-life, deprecated)
- Python 3.6.x (64-bit) (end-of-life, deprecated)

32-bit versions of Python are not supported.

To make sure your interpreter is able to load the CST Python Libraries, a
minimal package can be installed that links to the actual CST Studio Suite
installation::

    pip install --no-index --find-links "<CST_STUDIO_SUITE_FOLDER>/Library/Python/repo/simple" cst-studio-suite-link

where `CST_STUDIO_SUITE_FOLDER` should be replaced with the path to the CST
Studio Suite installation on your system. Do not install this package if you
don’t have CST Studio Suite installed on the same machine as the python
interpreter.

Note: Under linux The above package requires you to set an environment variable
named `CST_STUDIO_SUITE_LINK_INSTALLPATH_2024` pointing to the installation path
of the CST Studio Suite. Consult your operating system user manual on how to set
environment variables.

Note: Although not recommended, but if desired, instead of installing the
`cst-studio-suite-link` package, you can add or modify the `PYTHONPATH` system
environment variable to include:

- Windows: `CST_STUDIO_SUITE_FOLDER/AMD64/python_cst_libraries`
- Linux: `CST_STUDIO_SUITE_FOLDER/LinuxAMD64/python_cst_libraries`

or add it in-script via::

    >>> import sys
    >>> sys.path.append(r"<PATH_TO_CST_AMD64>/python_cst_libraries")

Please replace `PATH_TO_CST_AMD64` with the system dependent paths indicated
above (i.e. under Windows use: `CST_STUDIO_SUITE_FOLDER/AMD64` under Linux:
`CST_STUDIO_SUITE_FOLDER/LinuxAMD64`).

You have succesfully set up your Python environment when you are able to execute
the following code without error::

    >>> import cst
    >>> print(cst.__file__) # should print '<PATH_TO_CST_AMD64>/python_cst_libraries/cst/__init__.py'


"""

# __version__ = "2025.5"

import sys

sys.path.append(r"C:\Program Files (x86)\CST Studio Suite 2024\AMD64\python_cst_libraries")

import importlib_metadata

__version__ = importlib_metadata.version("mzcst-2024")

from . import asymptotic  # cst.asymptotic
from . import eda  # cst.eda
from . import interface  # cst.interface
from . import radar  # cst.radar
from . import results  # cst.results
from . import units  # cst.units
from . import (  # cst.asymptotic; _global,
    common,
    component,
    construction_curve,
    construction_face,
    curves,
    group,
    material,
    math_,
    plot,
    profiles_to_shapes,
    shape_operations,
    shapes,
    solver,
    sources_and_ports,
    transformations_and_picks,
)
from ._global import BaseObject, Parameter, Units, VbaObject, change_solver_type
