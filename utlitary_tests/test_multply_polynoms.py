from general import multiply_polynomials

import unittest
from typing import List


class TestMultiplyPolinoms(unittest.TestCase):
    def test_simple_multiplication(self):
        self.assertEqual(multiply_polynomials([1, 0, 1], [1, 1]), [1, 1, 1, 1])  # (x^2 + 1) * (x + 1) = x^3 + x + 1

    def test_multiplication_by_zero(self):
        self.assertEqual(multiply_polynomials([1, 0, 1], [0]), [0, 0, 0])  # Любое число на 0 = 0
        self.assertEqual(multiply_polynomials([0], [1, 1, 1]), [0, 0, 0])  # 0 на что угодно = 0

    def test_multiplication_by_one(self):
        self.assertEqual(multiply_polynomials([1, 1, 0, 1], [1]), [1, 1, 0, 1])  # Умножение на 1 не меняет многочлен

    def test_edge_cases(self):
        self.assertEqual(multiply_polynomials([], [1, 1]), [0])
        self.assertEqual(multiply_polynomials([1], [1]), [1])  # 1 * 1 = 1
        self.assertEqual(multiply_polynomials([1], [0]), [0])  # 1 * 0 = 0
        self.assertEqual(multiply_polynomials([0], [0]), [0])  # 0 * 0 = 0


if __name__ == "__main__":
    unittest.main()
