import random
import string

from hash_table import Hash_Table


def print_menu() -> None:
    print("\nМеню:")
    print("1. Добавить запись")
    print("2. Найти запись")
    print("3. Обновить запись")
    print("4. Удалить запись")
    print("5. Показать хеш-таблицу")
    print("6. Показать коэффициент заполнения")
    print("7. Показать коллизии")
    print("0. Выход")


def print_add_menu() -> None:
    print("\nДобавление записи:")
    print("1. Добавить вручную")
    print("2. Добавить рандомно")
    print("0. Назад")


def read_non_empty_input(message: str) -> str:
    while True:
        value = input(message).strip()

        if value:
            return value

        print("Значение не может быть пустым.")


def read_positive_int(message: str) -> int:
    while True:
        value = input(message).strip()

        if not value.isdigit():
            print("Введите целое положительное число.")
            continue

        number = int(value)

        if number <= 0:
            print("Число должно быть больше 0.")
            continue

        return number


def add_manually(hash_table: Hash_Table) -> None:
    key = read_non_empty_input("Введите ключ: ")
    value = read_non_empty_input("Введите значение: ")
    hash_table.add(key, value)


def generate_random_records(count: int) -> list[tuple[str, str]]:
    records = []
    pair_number = 1

    while len(records) < count:
        first_letter = random.choice(string.ascii_lowercase)
        second_letter = random.choice(string.ascii_lowercase)

        while second_letter == first_letter:
            second_letter = random.choice(string.ascii_lowercase)

        key_1 = f"{first_letter}{second_letter}{pair_number}"
        key_2 = f"{second_letter}{first_letter}{pair_number}"

        value_1 = f"random value {pair_number}.1"
        value_2 = f"random value {pair_number}.2"

        records.append((key_1, value_1))

        if len(records) < count:
            records.append((key_2, value_2))

        pair_number += 1

    random.shuffle(records)
    return records


def add_randomly(hash_table: Hash_Table) -> None:
    count = read_positive_int("Введите количество записей: ")
    records = generate_random_records(count)

    print("\nРандомная генерация записей:")
    print("-" * 80)

    for key, value in records:
        print(f"\nДобавляется запись: key={key}, value={value}")
        hash_table.add(key, value)

    print("-" * 80)
    print("Рандомное добавление завершено.")


def handle_add_menu(hash_table: Hash_Table) -> None:
    while True:
        print_add_menu()
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            add_manually(hash_table)

        elif choice == "2":
            add_randomly(hash_table)

        elif choice == "0":
            break

        else:
            print("Некорректный пункт меню.")


def main() -> None:
    hash_table = Hash_Table(size=20)

    while True:
        print_menu()
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            handle_add_menu(hash_table)

        elif choice == "2":
            key = read_non_empty_input("Введите ключ для поиска: ")
            result = hash_table.get(key)

            if result is None:
                print("Запись не найдена.")
            else:
                print(f"Найдено значение: {result}")

        elif choice == "3":
            key = read_non_empty_input("Введите ключ для обновления: ")
            new_value = read_non_empty_input("Введите новое значение: ")
            hash_table.update(key, new_value)

        elif choice == "4":
            key = read_non_empty_input("Введите ключ для удаления: ")
            hash_table.delete(key)

        elif choice == "5":
            hash_table.show()

        elif choice == "6":
            print(f"Коэффициент заполнения: {hash_table.load_factor():.2f}")

        elif choice == "7":
            hash_table.show_collisions()

        elif choice == "0":
            print("Программа завершена.")
            break

        else:
            print("Некорректный пункт меню.")


if __name__ == "__main__":
    main()