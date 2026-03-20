import shutil
import subprocess


def main() -> None:
    coverage_executable = shutil.which("coverage")

    if coverage_executable is None:
        print("Пакет coverage не найден.")
        print("Установи его командой:")
        print("python3 -m pip install coverage")
        return

    print("Очистка старых данных покрытия...\n")
    erase_result = subprocess.run([coverage_executable, "erase"])
    if erase_result.returncode != 0:
        print("Не удалось очистить старые данные coverage.")
        return

    print("Запуск unit-тестов...\n")
    test_result = subprocess.run([
        coverage_executable,
        "run",
        "--source=src,main",
        "-m",
        "unittest",
        "discover",
        "-s",
        "tests",
        "-v",
    ])

    if test_result.returncode != 0:
        print("\nНекоторые тесты завершились с ошибкой.")
        print("Показываю отчет покрытия для уже выполненного кода:\n")
    else:
        print("\nВсе тесты успешно выполнены.\n")

    print("Отчет покрытия:\n")
    report_result = subprocess.run([
        coverage_executable,
        "report",
        "-m",
        "--omit=*/tests/*,*/test_*"
    ])

    if report_result.returncode != 0:
        print("Не удалось вывести отчет покрытия.")
        return

    print("\nГотово.")


if __name__ == "__main__":
    main()