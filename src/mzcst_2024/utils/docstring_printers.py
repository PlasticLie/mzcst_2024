"""提供用于打印模块、类或对象中成员的 docstring 的实用程序类。"""

import inspect
import sys


class ModuleDocstringPrinter:
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

            attributes = []
            for name, member in inspect.getmembers(cls):
                if name.startswith("_") and self._only_public:
                    continue
                if not callable(member):
                    attributes.append((name, member))
            attributes.sort(key=lambda item: item[0].lower())
            if attributes:
                print("  Attributes:", file=self._file)
                for attr_name, attr in attributes:
                    print(f"    - {attr_name}", file=self._file)
                print(file=self._file)
            else:
                print("  (无公开属性)", file=self._file)
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
            print(
                f"在 {self._module.__name__} 中未找到任何函数。",
                file=self._file,
            )
            return

        for func_name, func in functions:
            print(f"=== Function: {func_name} ===", file=self._file)
            print(
                inspect.getdoc(func) or "(无 function docstring)",
                file=self._file,
            )
            print(file=self._file)


class ClassDocstringPrinter:
    def __init__(self, cls, file=None, only_public=True):
        self._cls = cls
        self._file = sys.stdout if file is None else file
        self._only_public = only_public

    def _iter_public_methods(self, cls: type):
        """返回类的公开可调用成员（尽量覆盖 pybind 暴露的方法）。"""
        for name, member in inspect.getmembers(cls):
            if name.startswith("_") and self._only_public:
                continue
            if callable(member):
                yield name, member

    def print_attributes_and_methods(self):
        print(f"=== Class: {self._cls.__name__} ===", file=self._file)
        print(
            inspect.getdoc(self._cls) or "(无 class docstring)", file=self._file
        )
        print(file=self._file)

        attributes = []
        for name, member in inspect.getmembers(self._cls):
            if name.startswith("_") and self._only_public:
                continue
            if not callable(member):
                attributes.append((name, member))
        attributes.sort(key=lambda item: item[0].lower())
        if attributes:
            print("  Attributes:", file=self._file)
            for attr_name, attr in attributes:
                print(f"    - {attr_name}", file=self._file)
            print(file=self._file)
        else:
            print("  (无公开属性)", file=self._file)
            print(file=self._file)

        methods = sorted(
            self._iter_public_methods(self._cls),
            key=lambda item: item[0].lower(),
        )
        if not methods:
            print("  (无公开方法)", file=self._file)
            print(file=self._file)
            return

        for method_name, method in methods:
            print(f"  - Method: {method_name}", file=self._file)
            print(
                f"    {inspect.getdoc(method) or '(无 method docstring)'}",
                file=self._file,
            )
            print(file=self._file)


class ObjectDocstringPrinter:
    def __init__(self, obj, file=None, only_public=True):
        self._obj = obj
        self._file = sys.stdout if file is None else file
        self._only_public = only_public

    def _iter_public_methods(self, cls: type):
        """返回类的公开可调用成员（尽量覆盖 pybind 暴露的方法）。"""
        for name, member in inspect.getmembers(cls):
            if name.startswith("_") and self._only_public:
                continue
            if callable(member):
                yield name, member

    def print_methods(self):
        print(f"=== Class: {self._obj.__class__.__name__} ===", file=self._file)
        print(
            inspect.getdoc(self._obj.__class__) or "(无 class docstring)",
            file=self._file,
        )
        print(file=self._file)

        methods = sorted(
            self._iter_public_methods(self._obj.__class__),
            key=lambda item: item[0].lower(),
        )
        if not methods:
            print("  (无公开方法)", file=self._file)
            print(file=self._file)
            return

        for method_name, method in methods:
            print(f"  - Method: {method_name}", file=self._file)
            print(
                f"    {inspect.getdoc(method) or '(无 method docstring)'}",
                file=self._file,
            )
            print(file=self._file)

    def print_attributes_and_methods(self):
        print(f"=== Class: {self._obj.__class__.__name__} ===", file=self._file)
        print(
            inspect.getdoc(self._obj.__class__) or "(无 class docstring)",
            file=self._file,
        )
        print(file=self._file)

        attributes = []
        for name, member in inspect.getmembers(self._obj):
            if name.startswith("_") and self._only_public:
                continue
            if not callable(member):
                attributes.append((name, member))
        attributes.sort(key=lambda item: item[0].lower())
        if attributes:
            print("  Attributes:", file=self._file)
            for attr_name, attr in attributes:
                print(f"    - {attr_name}", file=self._file)
            print(file=self._file)
        else:
            print("  (无公开属性)", file=self._file)
            print(file=self._file)

        methods = sorted(
            self._iter_public_methods(self._obj),
            key=lambda item: item[0].lower(),
        )
        if not methods:
            print("  (无公开方法)", file=self._file)
            print(file=self._file)
            return

        for method_name, method in methods:
            print(f"  - Method: {method_name}", file=self._file)
            print(
                f"    {inspect.getdoc(method) or '(无 method docstring)'}",
                file=self._file,
            )
            print(file=self._file)
