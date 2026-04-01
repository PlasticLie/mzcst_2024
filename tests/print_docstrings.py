"""打印 cst.units 中所有类及其方法的 docstring。"""

from __future__ import annotations

import inspect

import cst.units as cu


def _iter_public_methods(cls: type):
    """返回类的公开可调用成员（尽量覆盖 pybind 暴露的方法）。"""
    for name, member in inspect.getmembers(cls):
        if name.startswith("_"):
            continue
        if callable(member):
            yield name, member


def print_classes_and_methods() -> None:
    classes = []
    for name, obj in inspect.getmembers(cu):
        if inspect.isclass(obj):
            classes.append((name, obj))

    classes.sort(key=lambda item: item[0].lower())

    if not classes:
        print("在 cst.units 中未找到任何类。")
        return

    for class_name, cls in classes:
        print(f"=== Class: {class_name} ===")
        print(inspect.getdoc(cls) or "(无 class docstring)")
        print()

        methods = sorted(
            _iter_public_methods(cls), key=lambda item: item[0].lower()
        )
        if not methods:
            print("  (无公开方法)")
            print()
            continue

        for method_name, method in methods:
            print(f"  - Method: {method_name}")
            print(f"    {inspect.getdoc(method) or '(无 method docstring)'}")
            print()


class DocstringPrinter:
    """打印模块中所有类及其方法的 docstring。"""

    def __init__(self, module, file=None):
        self._module = module
        self._file = file
        self._only_public = True

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
            print(f"=== Class: {class_name} ===")
            print(inspect.getdoc(cls) or "(无 class docstring)")
            print()

            methods = sorted(
                self._iter_public_methods(cls), key=lambda item: item[0].lower()
            )
            if not methods:
                print("  (无公开方法)")
                print()
                continue

            for method_name, method in methods:
                print(f"  - Method: {method_name}")
                print(
                    f"    {inspect.getdoc(method) or '(无 method docstring)'}"
                )
                print()


if __name__ == "__main__":
    printer = DocstringPrinter(cu)
    printer.print_classes_and_methods()
