import mzcst_2024 as mz
from mzcst_2024 import Parameter, math_


@mz.common.time_decorator
def test_winwrap_basic_expression():
    validator = mz.winwrap_basic.expression.WinWrapBasicExpressionValidator()
    test_cases = [
        # 有效表达式
        ("2 + 3 * 4", True),
        ("(a + b) * c", True),
        ("sin(x) + cos(y)", True),
        ("sqrt(4) + abs(-5)", True),
        ("a + b - c * d / e", True),
        ("x^2 + y^2", True),
        ("(a > b) and (c < d)", True),
        ("not (x = y)", True),
        ('"hello" & "world"', True),
        ("3.14 * r^2", True),
        ("1.23e-5 + 2.34E+3", True),
        # 无效表达式
        ("2 + * 3", False),  # 连续运算符
        ("(a + b", False),  # 括号不匹配
        ("sin(,)", False),  # 函数参数为空
        ("123abc", False),  # 无效标识符
        ("+", False),  # 只有运算符
        ("a +", False),  # 以运算符结束
        ("( )", False),  # 空括号
        ("2 + + 3", False),  # 连续二元运算符
        ("sin(x, , y)", False),  # 缺少参数
        ("123.", False),  # 无效数字格式
    ]
    print("测试WinWrap Basic表达式验证器:")
    print("-" * 50)

    for expr, expected in test_cases:
        is_valid, msg = validator.is_valid_winwrap_expression(expr)
        status = "✓" if is_valid == expected else "✗"
        print(f"{status} 表达式: {expr}")
        print(
            f"  预期: {'有效' if expected else '无效'}, 结果: {'有效' if is_valid else '无效'}"
        )
        if not is_valid:
            print(f"  错误: {msg}")
        print()


@mz.common.time_decorator
def test_parameter_operations():
    a = Parameter("a", 1.5, "test description")
    b = Parameter("b", "2")
    c = Parameter("c", 36)
    d = ((a + b) * c).rename("d").re_describe("new description")
    e = (a + b * c).rename("e")
    f = Parameter(2 / a).rename("f")
    print(repr(d))
    print(repr(e))
    print(repr(f))
    g = a + b
    print(repr(g))
    print(math_.sqrt(2))


if __name__ == "__main__":
    test_winwrap_basic_expression()
    test_parameter_operations()
    pass
