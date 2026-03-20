BCD_2421_TABLE = {
    0: [0, 0, 0, 0],
    1: [0, 0, 0, 1],
    2: [0, 0, 1, 0],
    3: [0, 0, 1, 1],
    4: [0, 1, 0, 0],
    5: [1, 0, 1, 1],
    6: [1, 1, 0, 0],
    7: [1, 1, 0, 1],
    8: [1, 1, 1, 0],
    9: [1, 1, 1, 1],
}


BCD_2421_REVERSE_TABLE = {
    (0, 0, 0, 0): 0,
    (0, 0, 0, 1): 1,
    (0, 0, 1, 0): 2,
    (0, 0, 1, 1): 3,
    (0, 1, 0, 0): 4,
    (1, 0, 1, 1): 5,
    (1, 1, 0, 0): 6,
    (1, 1, 0, 1): 7,
    (1, 1, 1, 0): 8,
    (1, 1, 1, 1): 9,
}


def digit_to_2421(digit: int) -> list[int]:
    if digit < 0 or digit > 9:
        raise ValueError("Цифра должна быть от 0 до 9")

    return BCD_2421_TABLE[digit]


def code_2421_to_digit(bits: list[int]) -> int:
    bits_tuple = tuple(bits)

    if bits_tuple not in BCD_2421_REVERSE_TABLE:
        raise ValueError("Недопустимая тетрада 2421 BCD")

    return BCD_2421_REVERSE_TABLE[bits_tuple]


def number_to_2421(number: int) -> list[list[int]]:
    if number < 0:
        raise ValueError("В этой реализации число должно быть неотрицательным")

    digits = [int(symbol) for symbol in str(number)]

    result = []
    for digit in digits:
        result.append(digit_to_2421(digit))

    return result


def bcd_2421_to_string(groups: list[list[int]]) -> str:
    parts = []

    for group in groups:
        part = ""
        for bit in group:
            part += str(bit)
        parts.append(part)

    return " ".join(parts)


def bcd_2421_to_decimal(groups: list[list[int]]) -> int:
    digits = []

    for group in groups:
        digits.append(str(code_2421_to_digit(group)))

    return int("".join(digits))


def add_numbers_2421(number_1: int, number_2: int) -> list[list[int]]:
    if number_1 < 0 or number_2 < 0:
        raise ValueError("В этой реализации числа должны быть неотрицательными")

    digits_1 = [int(symbol) for symbol in str(number_1)]
    digits_2 = [int(symbol) for symbol in str(number_2)]

    max_len = max(len(digits_1), len(digits_2))

    digits_1 = [0] * (max_len - len(digits_1)) + digits_1
    digits_2 = [0] * (max_len - len(digits_2)) + digits_2

    carry = 0
    result_digits = []

    for i in range(max_len - 1, -1, -1):
        total = digits_1[i] + digits_2[i] + carry

        if total >= 10:
            result_digits.append(total - 10)
            carry = 1
        else:
            result_digits.append(total)
            carry = 0

    if carry == 1:
        result_digits.append(1)

    result_digits.reverse()

    result_codes = []
    for digit in result_digits:
        result_codes.append(digit_to_2421(digit))

    return result_codes