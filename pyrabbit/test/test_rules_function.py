import unittest
from pyrabbit.rules import function


class TestRulesFunction(unittest.TestCase):
    def test_function_responsibilities(self):
        self.assertEqual(function.responsibilities(0, 2), 1)
        self.assertEqual(function.responsibilities(1, 2), 0.5)
        self.assertEqual(function.responsibilities(2, 2), 0)
