import re
from typing import Dict, List, Optional, Set, Tuple


class WinWrapBasicExpressionValidator:
    """
    一个用于验证WinWrap Basic算术表达式的类。

    主要特性：
    -------------
    支持WinWrap Basic语法：

    算术运算符：`+`, `-`, `*`, `/`, `^`（幂）, `\\`（整除）, `%`（模）, `&`（字符串连接）

    比较运算符：`=`, `<`, `>`, `<=`, `>=`, `<>`

    逻辑运算符：`and`, `or`, `not`, `xor`, `eqv`, `imp`

    支持数据类型：
    -------------

    整数、小数、科学计数法

    字符串字面量（用双引号括起）

    标识符（变量名）

    预定义常量

    支持数学函数：
    --------------

    `sin()`, `cos()`, `tan()`等三角函数

    `sqrt()`, `abs()`, `log()`等数学函数

    支持函数嵌套调用
    ----------------

    验证步骤：
    -------------
    分词：将表达式拆分为令牌

    括号匹配：检查括号是否正确配对

    结构验证：检查运算符和操作数的顺序

    函数调用验证：检查函数参数的有效性

    """

    def __init__(self):
        # 定义合法的算术运算符
        self.operators = {"+", "-", "*", "/", "^", "\\", "%", "&"}
        self.comparison_ops = {"=", "<", ">", "<=", ">=", "<>"}
        self.logical_ops = {"and", "or", "not", "xor", "eqv", "imp"}

        # 内置数学函数（部分）
        self.math_functions = {
            "abs",
            "sqr",
            "sqrt",
            "exp",
            "log",
            "log10",
            "sin",
            "cos",
            "tan",
            "asin",
            "acos",
            "atan",
            "sinh",
            "cosh",
            "tanh",
            "int",
            "fix",
            "round",
            "rnd",
            "randomize",
            "pi",
        }

        # 预定义常量
        self.constants = {"pi", "true", "false", "null", "nothing"}

        # 操作符优先级（数字越大优先级越高）
        self.operator_precedence = {
            "^": 5,
            "*": 4,
            "/": 4,
            "\\": 4,
            "%": 4,
            "+": 3,
            "-": 3,
            "&": 2,
            "=": 1,
            "<": 1,
            ">": 1,
            "<=": 1,
            ">=": 1,
            "<>": 1,
            "not": 0,
            "and": -1,
            "or": -1,
            "xor": -1,
            "eqv": -1,
            "imp": -1,
        }

    def is_valid_identifier(self, identifier: str) -> bool:
        """检查是否为有效的标识符"""
        # WinWrap Basic标识符规则：以字母开头，可包含字母、数字和下划线
        if not identifier:
            return False
        if not identifier[0].isalpha():
            return False
        pattern = r"^[a-zA-Z_][a-zA-Z0-9_]*$"
        return bool(re.match(pattern, identifier))

    def is_number(self, token: str) -> bool:
        """检查是否为有效的数字"""
        # 支持整数、小数、科学计数法
        patterns = [
            r"^\d+$",  # 整数
            r"^\d+\.\d*$",  # 小数
            r"^\d*\.\d+$",  # 小数
            r"^\d+(\.\d+)?[eE][+-]?\d+$",  # 科学计数法
        ]
        return any(re.match(pattern, token) for pattern in patterns)

    def is_string_literal(self, token: str) -> bool:
        """检查是否为字符串字面量"""
        return len(token) >= 2 and token.startswith('"') and token.endswith('"')

    def tokenize(self, expression: str) -> List[str]:
        """将表达式拆分为令牌"""
        tokens = []
        i = 0
        n = len(expression)

        while i < n:
            # 跳过空白字符
            if expression[i].isspace():
                i += 1
                continue

            # 检查多字符运算符
            if i + 1 < n:
                two_char_op = expression[i : i + 2]
                if two_char_op in {"<=", ">=", "<>", "or", "and", "not", "xor"}:
                    # 处理多单词逻辑运算符
                    if two_char_op == "or" and (
                        i == 0 or not expression[i - 1].isalnum()
                    ):
                        tokens.append("or")
                        i += 2
                        continue
                    elif two_char_op in {"<=", ">=", "<>"}:
                        tokens.append(two_char_op)
                        i += 2
                        continue

            # 检查单字符运算符
            if expression[i] in self.operators.union(
                {"=", "<", ">", "(", ")", ","}
            ):
                tokens.append(expression[i])
                i += 1
                continue

            # 标识符或函数名
            if expression[i].isalpha() or expression[i] == "_":
                start = i
                while i < n and (
                    expression[i].isalnum() or expression[i] == "_"
                ):
                    i += 1
                tokens.append(expression[start:i])
                continue

            # 数字
            if expression[i].isdigit() or expression[i] == ".":
                start = i
                while i < n and (
                    expression[i].isdigit()
                    or expression[i] == "."
                    or expression[i].lower() in "e+-"
                ):
                    i += 1
                tokens.append(expression[start:i])
                continue

            # 字符串字面量
            if expression[i] == '"':
                start = i
                i += 1
                while i < n and expression[i] != '"':
                    i += 1
                if i < n:
                    i += 1
                tokens.append(expression[start:i])
                continue

            # 未知字符
            return None

        return tokens

    def validate_parentheses(self, tokens: List[str]) -> bool:
        """检查括号是否匹配"""
        stack = []
        for token in tokens:
            if token == "(":
                stack.append(token)
            elif token == ")":
                if not stack:
                    return False
                stack.pop()
        return len(stack) == 0

    def is_operator(self, token: str) -> bool:
        """检查是否为运算符"""
        return (
            token in self.operators
            or token in self.comparison_ops
            or token.lower() in self.logical_ops
        )

    def validate_expression_structure(
        self, tokens: List[str]
    ) -> Tuple[bool, str]:
        """验证表达式的结构"""
        if not tokens:
            return False, "空表达式"

        n = len(tokens)
        expect_operand = True  # True表示期望操作数，False表示期望运算符

        for i, token in enumerate(tokens):
            token_lower = token.lower()

            # 处理括号
            if token == "(":
                if not expect_operand:
                    return False, f"位置{i}: 运算符后不能直接跟左括号"
                # 检查括号内是否有内容
                if i + 1 < n and tokens[i + 1] == ")":
                    return False, f"位置{i}: 括号内不能为空"
                # 括号内重置期望操作数为True
                expect_operand = True

            elif token == ")":
                if expect_operand:
                    return False, f"位置{i}: 右括号前需要操作数"
                # 右括号后可以接运算符
                expect_operand = False

            # 处理逗号（函数参数分隔符）
            elif token == ",":
                if expect_operand:
                    return False, f"位置{i}: 逗号前需要参数"
                # 逗号后需要新的参数
                expect_operand = True

            # 处理函数调用
            elif (
                (
                    token_lower in self.math_functions
                    or self.is_valid_identifier(token)
                )
                and i + 1 < n
                and tokens[i + 1] == "("
            ):
                if not expect_operand:
                    return False, f"位置{i}: 函数调用前需要运算符"
                # 函数调用本身作为操作数
                expect_operand = False
                # 跳过函数名，让后续处理括号

            # 处理运算符
            elif self.is_operator(token):
                if expect_operand:
                    # 允许一元运算符 +, -, not
                    if token in {"+", "-", "not"} and i + 1 < n:
                        continue  # 一元运算符，仍然期望操作数
                    return False, f"位置{i}: 运算符'{token}'需要左操作数"
                # 运算符后需要操作数
                expect_operand = True

            # 处理操作数（数字、标识符、字符串）
            else:
                if not expect_operand:
                    return False, f"位置{i}: 操作数'{token}'前需要运算符"

                # 验证操作数的有效性
                if (
                    not self.is_number(token)
                    and not self.is_string_literal(token)
                    and not self.is_valid_identifier(token)
                    and token_lower not in self.constants
                ):
                    return False, f"位置{i}: 无效的操作数或标识符'{token}'"

                # 操作数后可以接运算符或右括号
                expect_operand = False

        # 表达式结束时应该期望运算符（即最后是操作数）
        if expect_operand:
            return False, "表达式不能以运算符结束"

        return True, "结构有效"

    def validate_function_calls(self, tokens: List[str]) -> Tuple[bool, str]:
        """验证函数调用"""
        i = 0
        n = len(tokens)

        while i < n:
            token = tokens[i]
            token_lower = token.lower()

            # 检查是否是函数调用
            if (
                (
                    token_lower in self.math_functions
                    or self.is_valid_identifier(token)
                )
                and i + 1 < n
                and tokens[i + 1] == "("
            ):

                # 查找对应的右括号
                paren_count = 1
                j = i + 2
                param_count = 0
                param_start = j

                while j < n and paren_count > 0:
                    if tokens[j] == "(":
                        paren_count += 1
                    elif tokens[j] == ")":
                        paren_count -= 1
                    elif tokens[j] == "," and paren_count == 1:
                        # 参数分隔符
                        param_count += 1
                        # 验证参数
                        param_tokens = tokens[param_start:j]
                        if param_tokens:
                            is_valid, msg = self.validate_expression_structure(
                                param_tokens
                            )
                            if not is_valid:
                                return (
                                    False,
                                    f"函数'{token}'的第{param_count}个参数无效: {msg}",
                                )
                        param_start = j + 1
                    j += 1

                if paren_count > 0:
                    return False, f"函数'{token}'的括号不匹配"

                # 验证最后一个参数
                if param_start < j - 1:
                    param_tokens = tokens[param_start : j - 1]
                    if param_tokens:
                        param_count += 1
                        is_valid, msg = self.validate_expression_structure(
                            param_tokens
                        )
                        if not is_valid:
                            return (
                                False,
                                f"函数'{token}'的第{param_count}个参数无效: {msg}",
                            )

                i = j - 1  # 跳过已处理的函数调用
            i += 1

        return True, "函数调用有效"

    def is_valid_winwrap_expression(self, expression: str) -> Tuple[bool, str]:
        """
        检查输入字符串是否为有效的WinWrap Basic算术表达式

        参数:
            expression: 要检查的字符串表达式

        返回:
            (is_valid, error_message): 元组，包含是否有效和错误信息
        """
        # 1. 基本检查
        if not expression or expression.strip() == "":
            return False, "表达式不能为空"

        # 2. 分词
        tokens = self.tokenize(expression.strip())
        if tokens is None:
            return False, "包含无效字符"

        # 3. 检查括号匹配
        if not self.validate_parentheses(tokens):
            return False, "括号不匹配"

        # 4. 检查表达式结构
        is_valid, msg = self.validate_expression_structure(tokens)
        if not is_valid:
            return False, msg

        # 5. 检查函数调用
        is_valid, msg = self.validate_function_calls(tokens)
        if not is_valid:
            return False, msg

        return True, "表达式有效"
