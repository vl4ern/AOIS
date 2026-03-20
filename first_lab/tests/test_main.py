import subprocess
import sys
import unittest
from pathlib import Path


class TestMainScript(unittest.TestCase):
    def test_main_smoke(self):
        project_root = Path(__file__).resolve().parents[1]
        main_path = project_root / "main.py"

        user_input = "\n".join([
            "5",      # base number for converters block
            "5",      # x
            "-3",     # y
            "-3",     # multiply a
            "4",      # multiply b
            "7",      # divide a
            "2",      # divide b
            "5.5",    # ieee add first
            "6.75",   # ieee add second
            "6.75",   # ieee sub first
            "5.5",    # ieee sub second
            "2.5",    # ieee mul first
            "1.5",    # ieee mul second
            "6.0",    # ieee div first
            "1.5",    # ieee div second
            "27",     # bcd first
            "35",     # bcd second
        ]) + "\n"

        result = subprocess.run(
            [sys.executable, str(main_path)],
            input=user_input,
            capture_output=True,
            text=True,
            cwd=str(project_root),
            timeout=20,
        )

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("Перевод в двоичный формат:", result.stdout)
        self.assertIn("Сумма в десятичном: 2", result.stdout)
        self.assertIn("Произведение в десятичном:   -12", result.stdout)
        self.assertIn("Результат деления (с точностью до 5 знаков): 3.50000", result.stdout)
        self.assertIn("Результат в десятичной:    12.25", result.stdout)
        self.assertIn("Результат в десятичной:    1.25", result.stdout)
        self.assertIn("Результат в десятичной:  3.75", result.stdout)
        self.assertIn("Результат в десятичной:  4.0", result.stdout)
        self.assertIn("Результат в десятичной:  62", result.stdout)


if __name__ == "__main__":
    unittest.main()