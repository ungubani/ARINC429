from LR_1.coder import sum_polynomials

import unittest
from typing import List


class TestSumPolynomials(unittest.TestCase):
    def test_simple_addition(self):
        self.assertEqual(sum_polynomials([1, 0, 1], [1, 1, 0]), [0, 1, 1])  # (x² + 1) + (x² + x) = x + 1

    def test_addition_with_zero(self):
        self.assertEqual(sum_polynomials([1, 0, 1], [0, 0, 0]), [1, 0, 1])  # Любое число + 0 = само число
        self.assertEqual(sum_polynomials([0, 0, 0], [1, 1, 1]), [1, 1, 1])  # 0 + что угодно = то же самое

    def test_addition_of_identical_polynomials(self):
        self.assertEqual(sum_polynomials([1, 0, 1], [1, 0, 1]), [0, 0, 0])  # Любое число + само себя = 0

    def test_different_lengths(self):
        self.assertEqual(sum_polynomials([1, 1], [1]), [0, 1])  # (x + 1) + 1 = x
        self.assertEqual(sum_polynomials([1], [1, 1]), [0, 1])

    def test_edge_cases(self):
        self.assertEqual(sum_polynomials([], [1, 1]), [1, 1])  # Пустой массив + что-то = то же самое
        self.assertEqual(sum_polynomials([1], []), [1])  # Аналогично
        self.assertEqual(sum_polynomials([], []), [])  # Два пустых массива = пустой массив


if __name__ == "__main__":
    unittest.main()
