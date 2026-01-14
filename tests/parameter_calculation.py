import mzcst_2024 as mz
from mzcst_2024 import Parameter, math_

if __name__ == "__main__":
    a = Parameter("a", 1.5, "test description")
    b = Parameter("b", "2")
    c = Parameter("c", 36)
    d = ((a + b) * c).rename("d").re_describe("new description")
    e = (a + b * c).rename("e")
    f = Parameter(2 / a).rename("f")
    print(repr(d))
    print(repr(e))
    print(repr(f))

    print(math_.sqrt(2))
    pass
