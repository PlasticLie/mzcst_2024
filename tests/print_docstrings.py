"""打印 cst.units 中所有类及其方法的 docstring。"""

import cst.interface as ci
import cst.results as cr
import cst.units as cu

import mzcst_2024
from mzcst_2024.utils.docstring_printers import (
    ClassDocstringPrinter,
    ModuleDocstringPrinter,
    ObjectDocstringPrinter,
)

if __name__ == "__main__":

    RESULTS_DIR = "results"
    # with open(
    #     f"{RESULTS_DIR}/units_docstrings.txt", "w", encoding="utf-8"
    # ) as f:
    #     printer = ModuleDocstringPrinter(cu, f, False)
    #     printer.print_all()

    # with open(
    #     f"{RESULTS_DIR}/interface_docstrings.txt", "w", encoding="utf-8"
    # ) as f:
    #     printer = ModuleDocstringPrinter(ci, f, False)
    #     printer.print_all()

    # with open(
    #     f"{RESULTS_DIR}/model3d_docstrings.txt", "w", encoding="utf-8"
    # ) as f:
    #     de = sign_env = ci.DesignEnvironment.connect_to_any_or_new()
    #     prj = de.active_project()
    #     m3d = prj.model3d
    #     printer = ObjectDocstringPrinter(m3d, f, False)
    #     # printer.print_methods()
    #     printer.print_attributes_and_methods()

    # with open(
    #     f"{RESULTS_DIR}/results_docstrings.txt", "w", encoding="utf-8"
    # ) as f:
    #     printer = ModuleDocstringPrinter(cr, f, False)
    #     printer.print_classes_and_methods()
    #     printer.print_functions()

    with open(
        f"{RESULTS_DIR}/mzcst_2024_shape_operations_docstrings.txt", "w", encoding="utf-8"
    ) as f:
        printer = ModuleDocstringPrinter(mzcst_2024.shape_operations, f, False)
        printer.print_all()
    pass
