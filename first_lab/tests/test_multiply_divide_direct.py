import io
import unittest
from contextlib import redirect_stdout

from src.multiply_direct import multiplication_of_numbers
from src.divide_direct import devide_direct


class TestDirectOperations(unittest.TestCase):
    def test_multiplication_of_numbers_output(self):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            multiplication_of_numbers(-3, 4)
        output = buffer.getvalue()

        self.assertIn("Прямой код первого числа:", output)
        self.assertIn("Прямой код второго числа:", output)
        self.assertIn("Произведение в прямом коде:", output)
        self.assertIn("Произведение в десятичном:", output)
        self.assertIn("-12", output)

    def test_devide_direct_output(self):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            devide_direct(7, 2)
        output = buffer.getvalue()

        self.assertIn("Прямой код первого числа:", output)
        self.assertIn("Прямой код второго числа:", output)
        self.assertIn("Результат деления (с точностью до 5 знаков):", output)
        self.assertIn("3.50000", output)

    def test_devide_direct_by_zero_returns_none_and_prints_nothing(self):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            result = devide_direct(7, 0)
        output = buffer.getvalue()

        self.assertIsNone(result)
        self.assertEqual(output, "")


if __name__ == "__main__":
    unittest.main()