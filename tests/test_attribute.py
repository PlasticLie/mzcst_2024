"""Tests for BaseAttribute."""

import unittest

from mzcst_2024 import AttributeList, CSTObjectAttribute


class TestBaseAttribute(unittest.TestCase):
    def test_initialization(self):
        for value, expected in (
            ("value", ["value"]),
            ("", [""]),
            (42, ["42"]),
            (-1.5, ["-1.5"]),
            (["first", "second"], ["first", "second"]),
            ([1, 2.5, "x"], ["1", "2.5", "x"]),
            ([], []),
        ):
            with self.subTest(value=value):
                attribute = CSTObjectAttribute("name", value)
                self.assertEqual(attribute.name, "name")
                self.assertEqual(attribute.value, expected)

    def test_typed_lists(self):
        strings: list[str] = ["x"]
        numbers: list[int] = [1]
        mixed: list[str | int | float] = ["x", 1, 2.5]
        self.assertEqual(CSTObjectAttribute("name", strings).value, ["x"])
        self.assertEqual(CSTObjectAttribute("name", numbers).value, ["1"])
        self.assertEqual(
            CSTObjectAttribute("name", mixed).value, ["x", "1", "2.5"]
        )

    def test_quote_validation(self):
        for name in ('a"b', "a'b"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                CSTObjectAttribute(name, "value")
        for value in ('"', '"start', 'end"', 'in"side', '"a"b"', '""x""'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                CSTObjectAttribute("name", value)
        with self.assertRaises(ValueError):
            CSTObjectAttribute("name", ["valid", 'in"valid'])

        attribute = CSTObjectAttribute("name", ['"quoted"', '""', "unquoted"])
        self.assertEqual(attribute.value, ['"quoted"', '""', "unquoted"])
        self.assertEqual(str(attribute), '.name "quoted", "", "unquoted"')

    def test_value_is_independent(self):
        attribute = CSTObjectAttribute("name", ["original"])
        values = attribute.value
        values[0] = 'in"valid'
        values.append('"')
        self.assertEqual(attribute.value, ["original"])

    def test_conversions_are_independent(self):
        attribute = CSTObjectAttribute("name", [1, 2.5, "x"])
        row = attribute.to_list()
        mapping = attribute.to_dict()
        self.assertEqual(row, ["name", "1", "2.5", "x"])
        self.assertEqual(mapping, {"name": ["1", "2.5", "x"]})
        row[1] = "changed"
        row.append("changed")
        mapping["name"].append("changed")
        self.assertEqual(attribute.value, ["1", "2.5", "x"])

        self.assertEqual(
            CSTObjectAttribute("single", 42).to_list(), ["single", "42"]
        )
        empty = CSTObjectAttribute("empty", [])
        self.assertEqual(empty.to_list(), ["empty"])
        self.assertEqual(empty.to_dict(), {"empty": []})

    def test_str(self):
        self.assertEqual(str(CSTObjectAttribute("name", 42)), '.name "42"')
        self.assertEqual(
            str(CSTObjectAttribute("name", [1, 2.5, "x"])),
            '.name "1", "2.5", "x"',
        )
        self.assertEqual(str(CSTObjectAttribute("name", [])), ".name ")

    def test_repr(self):
        self.assertEqual(
            repr(CSTObjectAttribute("name", 42)),
            'CSTObjectAttribute(name="name", value=["42"])',
        )
        self.assertEqual(
            repr(CSTObjectAttribute("name", [1, 2.5, "x"])),
            'CSTObjectAttribute(name="name", value=["1", "2.5", "x"])',
        )
        self.assertEqual(
            repr(CSTObjectAttribute("name", [])),
            'CSTObjectAttribute(name="name", value=[])',
        )
        self.assertEqual(
            repr(CSTObjectAttribute("name", '"c\\d\nx"')),
            r'CSTObjectAttribute(name="name", value=["\"c\\d\nx\""])',
        )
        self.assertEqual(
            repr(CSTObjectAttribute("名称", "值")),
            'CSTObjectAttribute(name="名称", value=["值"])',
        )


class TestAttributeList(unittest.TestCase):
    def test_initialization_and_access(self):
        first = CSTObjectAttribute("a", 1)
        second = CSTObjectAttribute("b", [2, "x"])
        self.assertEqual(len(AttributeList()), 0)
        self.assertIs(AttributeList(first)[0], first)
        attributes = AttributeList([first, second])
        self.assertEqual(list(attributes), [first, second])
        self.assertIs(attributes["a"], first)
        self.assertIs(attributes[-1], second)
        self.assertEqual(attributes[:1], [first])

        constructed = AttributeList(["a", "b"], [1, [2, "x"]])
        self.assertEqual(constructed.to_dict(), {"a": ["1"], "b": ["2", "x"]})
        with self.assertRaises(ValueError):
            AttributeList(["a", "b"], [1])
        with self.assertRaises(TypeError):
            AttributeList(["a"])  # type: ignore
        with self.assertRaises(KeyError):
            _ = attributes["missing"]
        with self.assertRaises(IndexError):
            _ = attributes[2]

    def test_mutation_and_duplicate_names(self):
        first = CSTObjectAttribute("a", 1)
        second = CSTObjectAttribute("b", 2)
        duplicate = CSTObjectAttribute("a", 3)
        attributes = AttributeList([first, duplicate, second])
        self.assertEqual(list(attributes), [first, duplicate, second])
        attributes.append(CSTObjectAttribute("a", 4))
        self.assertEqual(attributes["a"].value, ["1"])
        self.assertEqual(attributes.to_dict(), {"a": ["1"], "b": ["2"]})
        third = CSTObjectAttribute("c", 3)
        attributes["a"] = third
        self.assertIs(attributes["c"], third)
        attributes[1:] = [
            CSTObjectAttribute("c", 4),
            CSTObjectAttribute("d", 5),
        ]
        self.assertEqual(
            attributes.to_list(), [["c", ["3"]], ["c", ["4"]], ["d", ["5"]]]
        )
        del attributes["c"]
        self.assertEqual(attributes["c"].value, ["4"])
        del attributes[:]
        self.assertEqual(len(attributes), 0)
        with self.assertRaises(KeyError):
            attributes["missing"] = first
        with self.assertRaises(KeyError):
            del attributes["missing"]

    def test_conversions_are_independent(self):
        attributes = AttributeList(["a", "b"], [[1, 2], "x"])
        rows = attributes.to_list()
        mapping = attributes.to_dict()
        self.assertEqual(rows, [["a", ["1", "2"]], ["b", ["x"]]])
        self.assertEqual(mapping, {"a": ["1", "2"], "b": ["x"]})
        mapping["a"].append("changed")
        row_values = rows[0][1]
        self.assertIsInstance(row_values, list)
        if isinstance(row_values, list):
            row_values.append("changed")
        self.assertEqual(attributes["a"].value, ["1", "2"])
        self.assertEqual(AttributeList().to_list(), [])
        self.assertEqual(AttributeList().to_dict(), {})


if __name__ == "__main__":
    unittest.main()
