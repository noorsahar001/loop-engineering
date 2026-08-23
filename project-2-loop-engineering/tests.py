"""tests.py - Intentionally failing unit tests."""
import unittest
from app import add, abs_value, safe_divide


class TestAdd(unittest.TestCase):
    """Tests for the add function."""

    def test_add_positive_numbers(self):
        self.assertEqual(add(2, 3), 5)

    def test_add_negative_numbers(self):
        self.assertEqual(add(-1, -1), -2)


class TestAbsValue(unittest.TestCase):
    """Tests for the abs_value function."""

    def test_positive_number(self):
        self.assertEqual(abs_value(5), 5)

    def test_negative_number(self):
        self.assertEqual(abs_value(-5), 5)


class TestSafeDivide(unittest.TestCase):
    """Tests for the safe_divide function."""

    def test_normal_division(self):
        self.assertEqual(safe_divide(10, 2), 5.0)

    def test_divide_by_zero_returns_none(self):
        self.assertIsNone(safe_divide(10, 0))


if __name__ == "__main__":
    unittest.main()
