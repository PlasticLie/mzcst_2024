"""打印 cst.units 中所有类及其方法的 docstring。"""

from __future__ import annotations

import inspect
import sys

import cst.interface as ci
import cst.units as cu


class DocstringPrinter:
    """打印模块中所有类及其方法的 docstring。"""

    def __init__(self, module, file=None, only_public=True):
        self._module = module
        self._file = sys.stdout if file is None else file
        self._only_public = only_public

    def _iter_public_methods(self, cls: type):
        """返回类的公开可调用成员（尽量覆盖 pybind 暴露的方法）。"""
        for name, member in inspect.getmembers(cls):
            if name.startswith("_") and self._only_public:
                continue
            if callable(member):
                yield name, member

    def print_classes_and_methods(self) -> None:
        """打印模块中所有类及其方法的 docstring。"""
        classes = []
        for name, obj in inspect.getmembers(self._module):
            if inspect.isclass(obj):
                classes.append((name, obj))

        classes.sort(key=lambda item: item[0].lower())

        if not classes:
            print(f"在 {self._module.__name__} 中未找到任何类。")
            return

        for class_name, cls in classes:
            print(f"=== Class: {class_name} ===", file=self._file)
            print(
                inspect.getdoc(cls) or "(无 class docstring)", file=self._file
            )
            print(file=self._file)

            methods = sorted(
                self._iter_public_methods(cls), key=lambda item: item[0].lower()
            )
            if not methods:
                print("  (无公开方法)", file=self._file)
                print(file=self._file)
                continue

            for method_name, method in methods:
                print(f"  - Method: {method_name}", file=self._file)
                print(
                    f"    {inspect.getdoc(method) or '(无 method docstring)'}",
                    file=self._file,
                )
                print(file=self._file)

    def print_functions(self):
        """打印模块中所有函数的 docstring。"""
        functions = []
        for name, obj in inspect.getmembers(self._module):
            if inspect.isfunction(obj):
                functions.append((name, obj))

        functions.sort(key=lambda item: item[0].lower())

        if not functions:
            print(f"在 {self._module.__name__} 中未找到任何函数。")
            return

        for func_name, func in functions:
            print(f"=== Function: {func_name} ===", file=self._file)
            print(
                inspect.getdoc(func) or "(无 function docstring)",
                file=self._file,
            )
            print(file=self._file)


if __name__ == "__main__":
    with open("results/units_docstrings.txt", "w", encoding="utf-8") as f:
        printer = DocstringPrinter(cu, f)
        printer.print_classes_and_methods()
        printer.print_functions()

    with open("results/interface_docstrings.txt", "w", encoding="utf-8") as f:
        printer = DocstringPrinter(ci, f)
        printer.print_classes_and_methods()
        printer.print_functions()
    pass
