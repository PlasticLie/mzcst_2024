"""Tests for BaseAttribute."""

import unittest

from mzcst_2024.global_ import CSTObjectAttribute


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
                self.assertEqual(attribute._name, "name")
                self.assertEqual(attribute._value, expected)

    def test_typed_lists(self):
        strings: list[str] = ["x"]
        numbers: list[int] = [1]
        mixed: list[str | int | float] = ["x", 1, 2.5]
        self.assertEqual(CSTObjectAttribute("name", strings).value, ["x"])
        self.assertEqual(CSTObjectAttribute("name", numbers).value, ["1"])
        self.assertEqual(CSTObjectAttribute("name", mixed).value, ["x", "1", "2.5"])


if __name__ == "__main__":
    unittest.main()
