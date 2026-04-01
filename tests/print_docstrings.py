"""打印 cst.units 中所有类及其方法的 docstring。"""



import cst.interface as ci
import cst.units as cu

from mzcst_2024.utils.docstring_printers import (
    ClassDocstringPrinter,
    ModuleDocstringPrinter,
    ObjectDocstringPrinter,
)

if __name__ == "__main__":
    with open("results/units_docstrings.txt", "w", encoding="utf-8") as f:
        printer = ModuleDocstringPrinter(cu, f, False)
        printer.print_classes_and_methods()
        printer.print_functions()

    with open("results/interface_docstrings.txt", "w", encoding="utf-8") as f:
        printer = ModuleDocstringPrinter(ci, f, False)
        printer.print_classes_and_methods()
        printer.print_functions()

    with open("results/model3d_docstrings.txt", "w", encoding="utf-8") as f:
        de = sign_env = ci.DesignEnvironment.connect_to_any_or_new()
        prj = de.active_project()
        m3d = prj.model3d
        printer = ObjectDocstringPrinter(m3d, f, False)
        # printer.print_methods()
        printer.print_attributes_and_methods()
    pass
