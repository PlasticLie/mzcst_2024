"""Tests for ParameterList without requiring a running CST project."""

import unittest
from unittest.mock import Mock, call

from mzcst_2024 import Parameter, ParameterList


class TestParameterList(unittest.TestCase):
    def test_initialization_and_list_operations(self):
        first = Parameter("a", "1", "first")
        second = Parameter("b", "a + 1")
        self.assertEqual(len(ParameterList()), 0)
        self.assertIs(ParameterList(first)[0], first)
        parameters = ParameterList([first, second])
        self.assertNotIsInstance(parameters, list)
        self.assertEqual(len(parameters), 2)
        self.assertIs(parameters["a"], first)
        self.assertIs(parameters[-1], second)
        self.assertEqual(parameters[:1], [first])

        third = Parameter("c", 3)
        parameters.append(third)
        replacement = Parameter("d", 4)
        parameters["a"] = replacement
        del parameters["b"]
        self.assertEqual(list(parameters), [replacement, third])
        third.rename("renamed")
        self.assertIs(parameters["renamed"], third)
        with self.assertRaises(KeyError):
            _ = parameters["a"]
        with self.assertRaises(IndexError):
            _ = parameters[10]
        parameters[0] = first
        parameters[1:] = [second]
        del parameters[0]
        self.assertEqual(list(parameters), [second])
        with self.assertRaises(KeyError):
            parameters["missing"] = first
        with self.assertRaises(KeyError):
            del parameters["missing"]

    def test_names_and_values(self):
        parameters = ParameterList(["a", "b"], [1, "a + 1"])
        self.assertEqual(
            [(p.name, p.expression) for p in parameters],
            [("a", "1"), ("b", "a + 1")],
        )
        with self.assertRaises(ValueError):
            ParameterList(["a", "b"], [1])
        with self.assertRaises(TypeError):
            ParameterList(["a"])

    def test_does_not_expose_other_list_methods(self):
        parameters = ParameterList()
        for name in (
            "extend", "insert", "pop", "remove", "clear", "index", "count",
            "sort", "reverse",
        ):
            with self.subTest(name=name):
                self.assertFalse(hasattr(parameters, name))
        with self.assertRaises(TypeError):
            parameters + []

    def test_duplicate_names_are_preserved(self):
        first, second = Parameter("a", 1), Parameter("a", 2)
        with self.assertNoLogs("mzcst_2024.global_", level="WARNING"):
            parameters = ParameterList([first, second])
        self.assertIs(parameters["a"], first)
        self.assertIs(parameters[1], second)
        self.assertEqual(parameters.to_dict(), {"a": "1"})
        with self.assertNoLogs("mzcst_2024.global_", level="WARNING"):
            parameters.append(Parameter("a", 3))
            parameters[1] = Parameter("a", 4)
            parameters[1:] = [Parameter("a", 5), Parameter("b", 6)]
            parameters[2].rename("a")
        self.assertEqual(parameters.to_list(), [["a", "1"], ["a", "5"], ["a", "6"]])
        del parameters["a"]
        self.assertEqual(parameters.to_list(), [["a", "5"], ["a", "6"]])
        parameters = ParameterList(["a", "b", "a"], ["1", "2", "3"])
        self.assertEqual(parameters.to_list(), [["a", "1"], ["b", "2"], ["a", "3"]])

    def test_conversions(self):
        parameters = ParameterList([
            Parameter("a", "1", "description"),
            Parameter("b", "a + 1"),
        ])
        rows = parameters.to_list()
        self.assertEqual(rows, [["a", "1"], ["b", "a + 1"]])
        self.assertEqual(parameters.to_dict(), {"a": "1", "b": "a + 1"})
        self.assertEqual(list(parameters.to_dict()), ["a", "b"])
        rows[0][0] = "changed"
        self.assertEqual(parameters[0].name, "a")
        parameters[0].rename("renamed")
        self.assertEqual(parameters.to_dict(), {"renamed": "1", "b": "a + 1"})
        self.assertEqual(ParameterList().to_list(), [])
        self.assertEqual(ParameterList().to_dict(), {})

    def test_store_preserves_order_and_descriptions(self):
        modeler = Mock()
        parameters = ParameterList(
            [Parameter("a", 1, "first"), Parameter("b", "a + 1")]
        )
        self.assertIs(parameters.store(modeler), parameters)
        self.assertEqual(
            modeler.add_to_history.call_args_list,
            [
                call("Store parameter: a", 'MakeSureParameterExists("a", "1")'),
                call(
                    "Set parameter description: a",
                    'SetParameterDescription("a","first")',
                ),
                call("Store parameter: b", 'MakeSureParameterExists("b", "a + 1")'),
            ],
        )

    def test_store_propagates_failure(self):
        modeler = Mock()
        modeler.add_to_history.side_effect = RuntimeError("CST error")
        with self.assertRaisesRegex(RuntimeError, "CST error"):
            ParameterList([Parameter("a", 1), Parameter("b", 2)]).store(modeler)
        self.assertEqual(modeler.add_to_history.call_count, 1)


if __name__ == "__main__":
    unittest.main()
