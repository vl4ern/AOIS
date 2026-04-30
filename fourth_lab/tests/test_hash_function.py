import unittest

from hash_function import calculate_V, calculate_hash


class TestHashFunction(unittest.TestCase):
    def test_calculate_v_returns_sum_of_symbol_codes(self) -> None:
        result = calculate_V("ab")

        self.assertEqual(result, 195)

    def test_calculate_hash_returns_correct_index(self) -> None:
        result = calculate_hash("ab", 20)

        self.assertEqual(result, 15)

    def test_calculate_v_raises_error_for_empty_key(self) -> None:
        with self.assertRaises(ValueError):
            calculate_V("")

    def test_calculate_hash_raises_error_for_invalid_table_size(self) -> None:
        with self.assertRaises(ValueError):
            calculate_hash("ab", 0)


if __name__ == "__main__":
    unittest.main()