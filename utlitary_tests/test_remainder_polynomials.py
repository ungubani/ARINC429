from LR_1.coder import remainder_polynomials

import unittest


class TestCalculateRemainder(unittest.TestCase):
    def test_with_remainder(self):
        divisible = [1, 0, 1, 1, 0]
        divider = [1, 0, 1]
        expected_remainder = [0, 1]
        self.assertEqual(remainder_polynomials(divisible, divider), expected_remainder)

    def test_no_remainder(self):
        divisible = [1, 1, 0, 1, 1]
        divider = [1, 0, 1]
        expected_remainder = [0, 0]
        self.assertEqual(remainder_polynomials(divisible, divider), expected_remainder)

    def test_divisible_smaller_than_divider(self):
        divisible = [1, 0, 1]
        divider = [1, 0, 1, 1]
        expected_remainder = [1, 0, 1]
        self.assertEqual(remainder_polynomials(divisible, divider), expected_remainder)

    def test_divisible_equal_power_divider(self):
        divisible = [1, 0, 0, 1]
        divider = [1, 0, 1, 1]
        expected_remainder = [0, 0, 1]
        self.assertEqual(remainder_polynomials(divisible, divider), expected_remainder)

    def test_empty_divisible(self):
        divisible = []
        divider = [1, 0, 1]
        expected_remainder = [0, 0]
        self.assertEqual(remainder_polynomials(divisible, divider), expected_remainder)


    def test_radi_testa(self):
        divisible = [0, 0, 0, 0, 0, 0, 0, 1]
        divider = [1, 1, 0, 1]
        expected_remainder = [1, 0, 0]
        self.assertEqual(remainder_polynomials(divisible, divider), expected_remainder)
    # def test_single_bit_division(self):
    #     divisible = [1]
    #     divider = [1]
    #     expected_remainder = []
    #     self.assertEqual(calculate_remainder(divisible, divider), expected_remainder)


if __name__ == "__main__":
    unittest.main()
