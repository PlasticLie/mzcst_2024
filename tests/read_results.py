"""测试python读取cst仿真结果

Examples
--------

Introduction
========

The CST Studio Suite installation comes with a Python interpreter, so there is no need to additionally install Python to follow the examples.

Note: For simplicity, the following examples assume a Windows OS. However, Linux is supported as well.

To open a Python console, browse for the `\AMD64\python` subfolder of the CST Studio Suite installation (e.g. `C:\Program Files (x86)\CST STUDIO SUITE 2024\AMD64\python`) and run `python`(`.bat`).

Example 1 - Access S-Parameter data
----------------------------

The following code loads S-Parameter data of a 3D project.

For this example, take any 3D project which contains an S-Parameter S1,1, or create one from scratch. Open the project in CST Studio Suite, save it to an appropriate path (e.g. `C:\demo\project.cst`) and close CST Studio Suite.

Then load the project and address S1,1 via its navigation tree path:

>>> import cst.results
>>> project = cst.results.ProjectFile(r"C:\demo\project.cst")
>>> s11 = project.get_3d().get_result_item(r"1D Results\S-Parameters\S1,1")

The returned object is of the class ResultItem, which offers a variety of functions and properties to have a fine-grained data access to a 0D/1D Result. To get the x-axis data, use get_xdata() and xlabel. The function get_data() returns the data as list of tuples with varying number of entries, or a double value.

>>> s11.get_xdata()
[8.0, 9.0, 10.0]
>>> s11.xlabel
'Frequency / GHz'
>>> s11.get_data()
[(8.0, (0.011821912601590157+0.26499754190444946j), (1066.824324690301+0j)),
(9.0, (0.10851031541824341-0.052459076046943665j), (678.7112974398144+0j)),
(10.0, (-0.007742199115455151-0.06290644407272339j), (568.406116209625+0j))]

In this case, the first tuple entry in the list represents the frequency of the S-Parameter, the second tuple entry represents the complex-valued S-Parameter and the third entry represents the complex-valued Reference Impedance of the S-Parameter.

The returned object type of `get_data()` depends on the type of the loaded result. For 1D Results without Reference Impedance, this will be a list of tuples with two entries, where the second tuple entry may be complex-valued or not. For 0D Results, the method’s return value will not be a list, but a single double value.

In case you want to set up a demo example project from scratch, open an empty CST Studio Suite and select the New and Recent tab. From the `Modules/Tools` section, pick `3D Simulation-> High Frequency`. This will open an empty 3D project. From the Home Ribbon, select `Macros->Construct->Demo Examples->Waveguide T Splitter`. This will run a construction VBA macro. Start the simulation run to obtain 0D/1D Results. Save it and close CST Studio Suite.

Example 2 - Access subproject data
----------------------------

The following example shows how subproject data of a Schematic Task can be accessed.

To set up the example project, please open CST Studio Suite, go to the Component Library and use the search bar in the top right corner to find the “Antenna Reflector Assembly” example. Open it, save it to an appropriate path (e.g. “C:\demo\Antenna Reflector Assembly.cst”) and close CST Studio Suite.

To get the treepaths of all existing 0D/1D Results, the method get_tree_items() of the project’s Schematic ResultModule can be used.

>>> import cst.results
>>> project = cst.results.ProjectFile(r"C:\demo\Antenna Reflector Assembly.cst")
>>> project.get_schematic().get_tree_items()

However, you may notice that the project has more tree items which are not listed here, e.g. below Tasks\\SP1. These results are part of subprojects and need to be opened explicitly. Subprojects are represented by some Generalized Simulation Tasks in the Schematic, e.g. Simulation Project Tasks, Electrical Machine Tasks, Block Simulation Tasks or Hybrid Solver Tasks.

To get the treepaths of all existing subprojects, use the command list_subprojects().

>>> project.list_subprojects()

Using one of the obtained tree paths, the data of the corresponding subproject can be loaded by via load_subproject(). The returned object is again a ProjectFile which can be accessed like any other CST project. To show the tree items of the subproject, call get_tree_items() of the project’s 3D ResultModule.

>>> sub_project = project.load_subproject("Tasks\\SP1")
>>> sub_project.get_3d().get_tree_items()


Example 3 - Access parametric data
----------------------------

The following example shows how existing parametric 0D/1D Results can be accessed.

To set up the example project, please open CST Studio Suite, go to the Component Library and use the search bar in the top right corner to find the “VCO Parameter Sweep” example. Open it, save it to an appropriate path (e.g. `C:/demo/VCO Parameter Sweep.cst`) and close CST Studio Suite.

Typically, CST Studio Suite stores all 0D/1D Results which are calculated during a parameter sweep of simulation runs. This allows studying the relationship of parameters and results. In CST Studio Suite, a parameter combination is represented by an identifier called run id. A detailed description about parametric data handling can be found in the Parametric Results Overview.

In Python, the run id is depicted by an integer.

Note that this is a Circuits & Systems project, therefore the Schematic `ResultModule` needs to be queried. To list all existing run ids, use `get_all_run_ids()`.

>>> import cst.results
>>> project = cst.results.ProjectFile(r"C:/demo/VCO Parameter Sweep.cst")
>>> schematic = project.get_schematic()
>>> schematic.get_all_run_ids()

This show all run ids which were created in the Schematic submodule of the project. However, not all tree entries necessarily have results for all existing run ids, since the project setup allows a fine-grained control about which results are stored during a parameter sweep.

Let’s first query the existing run ids of a Postprocessing Task result item via `get_run_ids()`.

>>> schematic.get_run_ids('Tasks\\Sweep Tuning Voltage\\Tran1\\PP1\\0D\\Oscillation Frequency')

In this case, for all runs there is also a result. Now let’s query the existing runs of the Port1 item in the Transient Task.

>>> schematic.get_run_ids('Tasks\\Sweep Tuning Voltage\\Tran1\\TD Currents\\Port1')

For this tree item, only results are stored which correspond to run id=0. If we try to get the ResultItem for a non-existing run id, we get an error. Note that the method get_result_item() has an argument for the queried run id which defaults to 0.

>>> port1 = schematic.get_result_item('Tasks\\Sweep Tuning Voltage\\Tran1\\TD Currents\\Port1',5)

Querying the existing result with run id=0 works.

>>> port1 = schematic.get_result_item('Tasks\\Sweep Tuning Voltage\\Tran1\\TD Currents\\Port1',0)
>>> port1.length

To resolve a run id to its parameter combination, use `get_parameter_combination()`. This method returns a dictionary which contains the parameter names and values.

>>> schematic.get_parameter_combination(4)
>>> schematic.get_parameter_combination(5)


For convenience, a loaded ResultItem also has a notion about its parameter combination. It offers `run_id` and `get_parameter_combination()`.

>>> f = schematic.get_result_item('Tasks\\Sweep Tuning Voltage\\Tran1\\PP1\\0D\\Oscillation Frequency',5)
>>> f.run_id
>>> f.get_parameter_combination()

In case one is interested in the relationship of parameter “VTUNE” to the result value “Oscillation Frequency”, one can read the data as follows:

>>> tree_item = 'Tasks\\Sweep Tuning Voltage\\Tran1\\PP1\\0D\\Oscillation Frequency'
>>> x = []
>>> y = []
>>> run_ids = schematic.get_run_ids(tree_item,skip_nonparametric=True)
>>> for run in run_ids:
>>>     result = schematic.get_result_item(tree_item,run)
>>>     x.append(result.get_parameter_combination()['VTUNE'])
>>>     y.append(result.get_ydata())
>>>
>>> for i in range(len(x)):
>>>     print (x[i], y[i])

Note that the loaded result “Oscillation Frequency” is a 0D Result, therefore the function `get_ydata()` returns a single double value. Since `run id=0` plays a special role (in particular, a copy of its results may exist with a different run id), we use the function `get_run_ids()` with the argument `skip_nonparametric=True` to exclude it from the list to avoid a potential result duplicate. The obtained x-y data now can be used for further processing or plotting.

"""

import logging
import math
import os
import sys
import time

import matplotlib.pyplot as plt
import numpy as np

import mzcst_2024 as mz
from mzcst_2024 import common

if __name__ == "__main__":

    #######################################
    # region 开始计时
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

    time_all_start: float = time.perf_counter()

    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    #######################################
    # region 设置
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

    time_stamps: list[float] = [time_all_start]
    current_time: str = common.current_time_string()

    CURRENT_PATH: str = os.path.dirname(
        os.path.abspath(__file__)
    )  # 获取当前py文件所在文件夹
    PARENT_PATH: str = os.path.dirname(CURRENT_PATH)

    results_demo_path = "D:/CST-2024-local/cst-results-demos"

    # 阶段计时
    time_stamps.append(time.perf_counter())

    LOG_PATH: str = os.path.join(PARENT_PATH, "logs")
    LOG_FILE_NAME: str = f"read-results-demo-{current_time}.log"
    LOG_LEVEL = logging.INFO
    FMT = "%(asctime)s.%(msecs)-3d %(name)s - %(levelname)s - %(message)s"
    DATEFMT = r"%Y-%m-%d %H:%M:%S"
    LOG_FORMATTER = logging.Formatter(FMT, DATEFMT)
    common.create_folder(LOG_PATH)
    logging.basicConfig(
        format=FMT, datefmt=DATEFMT, level=LOG_LEVEL, force=True
    )
    root_logger = logging.getLogger()
    root_logger.setLevel(LOG_LEVEL)
    logger = logging.getLogger(__name__)
    logger.setLevel(LOG_LEVEL)
    file_handler = logging.FileHandler(os.path.join(LOG_PATH, LOG_FILE_NAME))
    file_handler.setFormatter(LOG_FORMATTER)
    file_handler.setLevel(LOG_LEVEL)
    root_logger.addHandler(file_handler)
    logger.info("Start logging.")

    time_stamps.append(time.perf_counter())
    logger.info(
        "warm up: %s",
        common.time_to_string(time_stamps[-1] - time_stamps[-2]),
    )
    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    #######################################
    # region 文件处理
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

    project_path = os.path.join(results_demo_path, "Dual Patch Antenna.cst")
    project = mz.results.ProjectFile(
        filepath=project_path, allow_interactive=True
    )
    s11 = project.get_3d().get_result_item(r"1D Results\S-Parameters\S1,1")
    # print("S11 Result Item of Dual Patch Antenna.cst:")
    # print(s11)
    s11_xdata = s11.get_xdata()
    s11_data = s11.get_data()
    # print("S11 data Item of Dual Patch Antenna.cst:")
    # print(s11_data)

    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    #######################################
    # region 官方案例1
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

    eg1_path = os.path.join(results_demo_path, "project.cst")
    eg1 = mz.results.ProjectFile(eg1_path, allow_interactive=True)
    eg1_s11 = eg1.get_3d().get_result_item(r"1D Results\S-Parameters\S1,1")
    # eg1_s11_data = eg1_s11.get_data()
    # print(eg1_s11_data)

    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    #######################################
    # region 官方案例2
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
    eg2_path = os.path.join(results_demo_path, "Antenna Reflector Assembly.cst")
    eg2 = mz.results.ProjectFile(eg2_path, allow_interactive=True)
    eg2_tree_items = eg2.get_schematic().get_tree_items()
    eg2_subprojects_list = eg2.list_subprojects()
    # print("eg2_tree_items:")
    # print(eg2_tree_items)
    # print("eg2 subprojects:")
    # print(eg2_subprojects_list)
    eg2_subproject = eg2.load_subproject("Tasks\\Sweep1\\SP1")
    eg2_sub1_tree_items = eg2_subproject.get_3d().get_tree_items()
    # print("eg2_sub1_tree_items:")
    # print(eg2_sub1_tree_items)
    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    #######################################
    # region 官方案例3
    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
    eg3_path = os.path.join(results_demo_path, "VCO Parameter Sweep.cst")
    eg3 = mz.results.ProjectFile(eg3_path, allow_interactive=True)
    eg3_schematic = eg3.get_schematic()
    eg3_schematic_all_runids = eg3_schematic.get_all_run_ids()
    # print("eg3_schematic_all_runids:")
    # print(eg3_schematic_all_runids)
    eg3_schematic_runid_port1 = eg3_schematic.get_run_ids(
        "Tasks\\Sweep Tuning Voltage\\Tran1\\TD Currents\\Port1"
    )
    # print("eg3_schematic_runid_port1:")
    # print(eg3_schematic_runid_port1)
    # port1 = eg3_schematic.get_result_item('Tasks\\Sweep Tuning Voltage\\Tran1\\TD Currents\\Port1',5)
    port1 = eg3_schematic.get_result_item(
        "Tasks\\Sweep Tuning Voltage\\Tran1\\TD Currents\\Port1", 0
    )
    print(f"port1 length: {port1.length}")
    print("eg3_schematic.get_parameter_combination(4):")
    print(eg3_schematic.get_parameter_combination(4))
    print("eg3_schematic.get_parameter_combination(5):")
    print(eg3_schematic.get_parameter_combination(5))
    f = eg3_schematic.get_result_item(
        "Tasks\\Sweep Tuning Voltage\\Tran1\\PP1\\0D\\Oscillation Frequency", 5
    )
    print(f"f.run_id: {f.run_id}")
    print(f"f.get_parameter_combination(): {f.get_parameter_combination()}")
    tree_item = (
        "Tasks\\Sweep Tuning Voltage\\Tran1\\PP1\\0D\\Oscillation Frequency"
    )
    x = []
    y = []
    run_ids = eg3_schematic.get_run_ids(tree_item, skip_nonparametric=True)
    for run in run_ids:
        result = eg3_schematic.get_result_item(tree_item, run)
        x.append(result.get_parameter_combination()["VTUNE"])
        y.append(result.get_ydata())

    for i in range(len(x)):
        print(x[i], y[i])
    # endregion
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
    pass
