import unittest

from src.code_version import (
    digit_to_2421,
    code_2421_to_digit,
    number_to_2421,
    bcd_2421_to_string,
    bcd_2421_to_decimal,
    add_numbers_2421,
)


class TestCodeVersion2421(unittest.TestCase):
    def test_digit_to_2421(self):
        self.assertEqual(digit_to_2421(2), [0, 0, 1, 0])
        self.assertEqual(digit_to_2421(4), [0, 1, 0, 0])
        self.assertEqual(digit_to_2421(6), [1, 1, 0, 0])

    def test_digit_to_2421_invalid(self):
        with self.assertRaises(ValueError):
            digit_to_2421(10)

    def test_code_2421_to_digit(self):
        self.assertEqual(code_2421_to_digit([1, 1, 0, 0]), 6)

    def test_number_to_2421(self):
        self.assertEqual(number_to_2421(27), [[0, 0, 1, 0], [1, 1, 0, 1]])

    def test_bcd_2421_to_string(self):
        self.assertEqual(bcd_2421_to_string(number_to_2421(27)), "0010 1101")

    def test_bcd_2421_to_decimal(self):
        self.assertEqual(bcd_2421_to_decimal([[1, 1, 0, 0], [0, 0, 1, 0]]), 62)

    def test_add_numbers_2421(self):
        result = add_numbers_2421(27, 35)
        self.assertEqual(bcd_2421_to_string(result), "1100 0010")
        self.assertEqual(bcd_2421_to_decimal(result), 62)

    def test_add_numbers_2421_small(self):
        result = add_numbers_2421(2, 4)
        self.assertEqual(bcd_2421_to_string(result), "1100")
        self.assertEqual(bcd_2421_to_decimal(result), 6)


if __name__ == "__main__":
    unittest.main()