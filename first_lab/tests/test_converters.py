import unittest

from src.constants import MODULE_BITS, TOTAL_BITS
from src.converters import (
    convert_to_binary,
    pad_to_all_bits,
    add_sign,
    reserve_code,
    additional_code,
    binary_to_decimal,
)


class TestConverters(unittest.TestCase):
    def test_convert_to_binary_positive(self):
        self.assertEqual(convert_to_binary(13), [1, 1, 0, 1])

    def test_convert_to_binary_zero_returns_empty_list(self):
        self.assertEqual(convert_to_binary(0), [])

    def test_pad_to_all_bits(self):
        bits = [1, 0, 1]
        padded = pad_to_all_bits(bits)
        self.assertEqual(len(padded), MODULE_BITS)
        self.assertEqual(padded[-3:], [1, 0, 1])
        self.assertTrue(all(bit == 0 for bit in padded[:-3]))

    def test_add_sign(self):
        payload = [0] * MODULE_BITS
        self.assertEqual(add_sign(5, payload), [0] + payload)
        self.assertEqual(add_sign(-5, payload), [1] + payload)
        self.assertEqual(len(add_sign(-5, payload)), TOTAL_BITS)

    def test_reserve_code(self):
        self.assertEqual(reserve_code([0, 1, 1, 0]), [1, 0, 0, 1])

    def test_additional_code(self):
        self.assertEqual(additional_code([1, 0, 1, 0]), [1, 0, 1, 1])

    def test_binary_to_decimal(self):
        self.assertEqual(binary_to_decimal([1, 1, 0, 1]), 13)
        self.assertEqual(binary_to_decimal([0, 0, 0, 0]), 0)


if __name__ == "__main__":
    unittest.main() 