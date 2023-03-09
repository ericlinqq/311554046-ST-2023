import unittest
from calculator import Calculator
import math


class ApplicationTest(unittest.TestCase):


    def test_add(self):
        valid = [(0, 1), ('abdfdfs', 'dafdfsdv'), (-124, 0), (999999, 3432.3), (-3.235432, 3452.523)]
        invalid = [('adga', 341235)]

        for p1, p2 in valid:
            with self.subTest():
                self.assertEqual(p1+p2, Calculator.add(p1, p2))

        for p1, p2 in invalid:
            with self.subTest():
                self.assertRaises(TypeError, Calculator.add(p1, p2))

    def test_divide(self):
        valid = [(1, 1), (1.0354, 234233), (-12353, 7), (9999, 34.5984), (0, 3243214)]
        invalid = [(3423, 0)]
        for p1, p2 in valid:
            with self.subTest():
                self.assertEqual(p1/p2, Calculator.divide(p1, p2))

        for p1, p2 in invalid:
            with self.subTest():
                self.assertRaises(ZeroDivisionError, Calculator.divide(p1, p2))

    def test_sqrt(self):
        valid = [1, 0, 25, 0.9347853, 1233234]
        invalid = [-2453]
        for p1 in valid:
            with self.subTest():
                self.assertEqual(math.sqrt(p1), Calculator.sqrt(p1))

        for p1 in invalid:
            with self.subTest():
                self.assertRaises(ValueError, Calculator.sqrt(p1))

    def test_exp(self):
        valid = [0, 1, -32, 57, 0.3432]
        invalid = [2347]
        for p1 in valid:
            with self.subTest():
                self.assertEqual(math.exp(p1), Calculator.exp(p1))

        for p1 in invalid:
            with self.subTest():
                self.assertRaises(OverflowError, Calculator.exp(p1))
if __name__ == '__main__':
    unittest.main()
