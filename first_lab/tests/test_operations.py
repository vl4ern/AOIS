import unittest

from src.constants import TOTAL_BITS
from src.operations import binary_sum, to_additional, from_additional, add_additional


class TestOperations(unittest.TestCase):
    def test_binary_sum_same_length(self):
        self.assertEqual(binary_sum([1, 0, 1], [0, 1, 1]), [1, 0, 0, 0])

    def test_binary_sum_with_padding(self):
        self.assertEqual(binary_sum([1, 1], [1]), [1, 0, 0])

    def test_to_additional_positive(self):
        bits = to_additional(5)
        self.assertEqual(len(bits), TOTAL_BITS)
        self.assertEqual(bits[0], 0)
        self.assertEqual(from_additional(bits), 5)

    def test_to_additional_negative(self):
        bits = to_additional(-5)
        self.assertEqual(len(bits), TOTAL_BITS)
        self.assertEqual(bits[0], 1)
        self.assertEqual(from_additional(bits), -5)

    def test_add_additional_positive_and_negative(self):
        a = to_additional(5)
        b = to_additional(-3)
        result_bits = add_additional(a, b)
        self.assertEqual(from_additional(result_bits), 2)

    def test_add_additional_two_negative_numbers(self):
        a = to_additional(-2)
        b = to_additional(-3)
        result_bits = add_additional(a, b)
        self.assertEqual(from_additional(result_bits), -5)


if __name__ == "__main__":
    unittest.main()