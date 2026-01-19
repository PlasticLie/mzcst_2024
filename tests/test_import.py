import os
import sys

import read_results_official

if __name__ == "__main__":
    # mzcst_path = "../src"
    # abspath = os.path.abspath(mzcst_path)
    # print(f"Adding {abspath} to sys.path")
    # sys.path.append(abspath)

    for i, p in enumerate(sys.path):
        print(f"{i:2d}: {p}")
    import mzcst_2024 as mz

    print(mz.__version__)
    print(mz.__file__)
    

    print(read_results_official.__file__)
    

    pass
