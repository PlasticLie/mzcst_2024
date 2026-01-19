import os
import sys

if __name__ == "__main__":
    # mzcst_path = "../src"
    # abspath = os.path.abspath(mzcst_path)
    # print(f"Adding {abspath} to sys.path")
    # sys.path.append(abspath)

    for i, p in enumerate(sys.path):
        print(f"{i:2d}: {p}")

    try:
        import mzcst_2024 as mz

        print(mz.__version__)
        print(mz.__file__)
    except ImportError as e:
        print(f"ImportError: {e}")

    pass
