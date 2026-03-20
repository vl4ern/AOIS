import unittest

from src.ieee import (
    pad_bits,
    fractional_to_binary,
    normalize_binary,
    decimal_to_ieee754,
    bits_to_string,
    unpack_positive_ieee754,
    add_positive_ieee754,
    change_sign,
    is_all_zeros,
    compare_bits,
    subtract_mantissas,
    normalize_after_subtract,
    add_positive_and_negative_ieee754,
    ieee754_to_decimal,
    make_positive,
    multiply_mantissas,
    normalize_after_multiply,
    mul_ieee754,
    divide_mantissas,
    normalize_after_divide,
    div_ieee754,
)


class TestIEEE(unittest.TestCase):
    def test_pad_bits(self):
        self.assertEqual(pad_bits([1, 0, 1], 5), [0, 0, 1, 0, 1])

    def test_fractional_to_binary_half(self):
        self.assertEqual(fractional_to_binary(0.5, 10), [1])

    def test_fractional_to_binary_quarter(self):
        self.assertEqual(fractional_to_binary(0.25, 10), [0, 1])

    def test_fractional_to_binary_zero(self):
        self.assertEqual(fractional_to_binary(0.0, 10), [0])

    def test_normalize_binary_integer_not_zero(self):
        exponent, mantissa = normalize_binary([1, 0, 1], [1])
        self.assertEqual(exponent, 2)
        self.assertEqual(mantissa[:3], [0, 1, 1])

    def test_normalize_binary_fraction_only(self):
        exponent, mantissa = normalize_binary([0], [0, 1, 0, 0])
        self.assertEqual(exponent, -2)
        self.assertEqual(mantissa[0], 0)

    def test_decimal_to_ieee754_for_5_5(self):
        bits = decimal_to_ieee754(5.5)
        self.assertEqual(bits_to_string(bits), "01000000101100000000000000000000")

    def test_decimal_to_ieee754_for_negative_2_5(self):
        bits = decimal_to_ieee754(-2.5)
        self.assertEqual(bits_to_string(bits), "11000000001000000000000000000000")

    def test_decimal_to_ieee754_zero(self):
        bits = decimal_to_ieee754(0.0)
        self.assertEqual(bits, [0] * 32)

    def test_bits_to_string(self):
        self.assertEqual(bits_to_string([1, 0, 1, 1]), "1011")

    def test_unpack_positive_ieee754(self):
        exponent, mantissa = unpack_positive_ieee754(decimal_to_ieee754(5.5))
        self.assertEqual(exponent, 2)
        self.assertEqual(len(mantissa), 24)
        self.assertEqual(mantissa[:4], [1, 0, 1, 1])

    def test_change_sign(self):
        bits = decimal_to_ieee754(1.25)
        changed = change_sign(bits)
        self.assertEqual(changed[0], 1)
        self.assertEqual(changed[1:], bits[1:])

    def test_is_all_zeros_true(self):
        self.assertTrue(is_all_zeros([0, 0, 0]))

    def test_is_all_zeros_false(self):
        self.assertFalse(is_all_zeros([0, 1, 0]))

    def test_compare_bits_greater(self):
        self.assertEqual(compare_bits([1, 0, 1], [1, 0, 0]), 1)

    def test_compare_bits_less(self):
        self.assertEqual(compare_bits([1, 0, 0], [1, 0, 1]), -1)

    def test_compare_bits_equal(self):
        self.assertEqual(compare_bits([1, 0, 1], [1, 0, 1]), 0)

    def test_subtract_mantissas(self):
        self.assertEqual(
            subtract_mantissas([1, 0, 1, 1], [0, 1, 1, 0]),
            [0, 1, 0, 1]
        )

    def test_normalize_after_subtract(self):
        exponent, mantissa = normalize_after_subtract(2, [0, 1, 0, 1] + [0] * 20)
        self.assertEqual(exponent, 1)
        self.assertEqual(mantissa[0], 1)

    def test_normalize_after_subtract_zero(self):
        exponent, mantissa = normalize_after_subtract(2, [0] * 24)
        self.assertEqual(exponent, 0)
        self.assertEqual(mantissa, [0] * 24)

    def test_add_positive_ieee754(self):
        result_bits = add_positive_ieee754(
            decimal_to_ieee754(5.5),
            decimal_to_ieee754(6.75),
        )
        self.assertAlmostEqual(ieee754_to_decimal(result_bits), 12.25, places=6)

    def test_add_positive_and_negative_ieee754(self):
        first_bits = decimal_to_ieee754(6.75)
        second_bits = change_sign(decimal_to_ieee754(5.5))
        result_bits = add_positive_and_negative_ieee754(first_bits, second_bits)
        self.assertAlmostEqual(ieee754_to_decimal(result_bits), 1.25, places=6)

    def test_add_positive_and_negative_ieee754_zero_result(self):
        first_bits = decimal_to_ieee754(5.5)
        second_bits = change_sign(decimal_to_ieee754(5.5))
        result_bits = add_positive_and_negative_ieee754(first_bits, second_bits)
        self.assertEqual(result_bits, [0] * 32)

    def test_ieee754_to_decimal(self):
        self.assertAlmostEqual(ieee754_to_decimal(decimal_to_ieee754(3.75)), 3.75, places=6)

    def test_make_positive(self):
        bits = decimal_to_ieee754(-2.5)
        positive_bits = make_positive(bits)
        self.assertEqual(positive_bits[0], 0)
        self.assertEqual(positive_bits[1:], bits[1:])

    def test_multiply_mantissas(self):
        _, mantissa_1 = unpack_positive_ieee754(decimal_to_ieee754(2.5))
        _, mantissa_2 = unpack_positive_ieee754(decimal_to_ieee754(1.5))
        product_bits = multiply_mantissas(mantissa_1, mantissa_2)
        self.assertTrue(len(product_bits) >= 24)

    def test_normalize_after_multiply_short(self):
        exponent, mantissa = normalize_after_multiply(1, [1, 0, 1])
        self.assertEqual(exponent, 1)
        self.assertEqual(len(mantissa), 24)

    def test_mul_ieee754(self):
        result_bits = mul_ieee754(decimal_to_ieee754(2.5), decimal_to_ieee754(1.5))
        self.assertAlmostEqual(ieee754_to_decimal(result_bits), 3.75, places=6)

    def test_mul_ieee754_negative(self):
        result_bits = mul_ieee754(decimal_to_ieee754(-2.5), decimal_to_ieee754(1.5))
        self.assertAlmostEqual(ieee754_to_decimal(result_bits), -3.75, places=6)

    def test_divide_mantissas(self):
        _, mantissa_1 = unpack_positive_ieee754(decimal_to_ieee754(6.0))
        _, mantissa_2 = unpack_positive_ieee754(decimal_to_ieee754(1.5))
        quotient_bits = divide_mantissas(mantissa_1, mantissa_2)
        self.assertTrue(len(quotient_bits) > 0)

    def test_normalize_after_divide(self):
        exponent, mantissa = normalize_after_divide(2, [0, 1, 0, 0] + [0] * 20)
        self.assertEqual(mantissa[0], 1)
        self.assertEqual(exponent, 1)

    def test_div_ieee754(self):
        result_bits = div_ieee754(decimal_to_ieee754(6.0), decimal_to_ieee754(1.5))
        self.assertAlmostEqual(ieee754_to_decimal(result_bits), 4.0, places=6)

    def test_div_ieee754_negative(self):
        result_bits = div_ieee754(decimal_to_ieee754(-8.0), decimal_to_ieee754(2.0))
        self.assertAlmostEqual(ieee754_to_decimal(result_bits), -4.0, places=6)


if __name__ == "__main__":
    unittest.main()