import subprocess
import sys


def main() -> None:
    commands = [
        [sys.executable, "-m", "coverage", "erase"],
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            "-m",
            "unittest",
            "discover",
            "-s",
            "tests",
            "-v",
        ],
        [sys.executable, "-m", "coverage", "report", "-m"],
    ]

    for command in commands:
        result = subprocess.run(command)

        if result.returncode != 0:
            print("\nОшибка при выполнении команды:")
            print(" ".join(command))
            sys.exit(result.returncode)


if __name__ == "__main__":
    main()