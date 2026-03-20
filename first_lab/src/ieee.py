from src.converters import convert_to_binary, binary_to_decimal
from src.operations import binary_sum


def pad_bits(bits: list[int], size: int) -> list[int]:
    return [0] * (size - len(bits)) + bits


def fractional_to_binary(fractional_part: float, limit: int = 40) -> list[int]:
    bits = []

    while fractional_part > 0 and len(bits) < limit:
        fractional_part *= 2

        if fractional_part >= 1:
            bits.append(1)
            fractional_part -= 1
        else:
            bits.append(0)

    if len(bits) == 0:
        return [0]

    return bits


def normalize_binary(integer_bits: list[int], fractional_bits: list[int]) -> tuple[int, list[int]]:
    if integer_bits != [0]:
        exponent = len(integer_bits) - 1
        mantissa_source = integer_bits[1:] + fractional_bits
        return exponent, mantissa_source

    first_one_index = -1
    for i in range(len(fractional_bits)):
        if fractional_bits[i] == 1:
            first_one_index = i
            break

    if first_one_index == -1:
        return 0, [0] * 23

    exponent = -(first_one_index + 1)
    mantissa_source = fractional_bits[first_one_index + 1:]

    return exponent, mantissa_source


def decimal_to_ieee754(number: float) -> list[int]:
    sign = 0
    if number < 0:
        sign = 1
        number = -number

    if number == 0:
        return [sign] + [0] * 31

    integer_part = int(number)
    fractional_part = number - integer_part

    if integer_part == 0:
        integer_bits = [0]
    else:
        integer_bits = convert_to_binary(integer_part)

    fractional_bits = fractional_to_binary(fractional_part, 50)

    exponent, mantissa_source = normalize_binary(integer_bits, fractional_bits)

    exponent_raw = exponent + 127
    exponent_bits = convert_to_binary(exponent_raw)
    exponent_bits = pad_bits(exponent_bits, 8)

    mantissa_bits = (mantissa_source + [0] * 23)[:23]

    return [sign] + exponent_bits + mantissa_bits


def bits_to_string(bits: list[int]) -> str:
    result = ""
    for bit in bits:
        result += str(bit)
    return result


def unpack_positive_ieee754(bits: list[int]) -> tuple[int, list[int]]:
    if bits[0] != 0:
        raise ValueError("Эта функция работает только для положительных чисел")

    exponent_raw = binary_to_decimal(bits[1:9])
    exponent = exponent_raw - 127

    mantissa_field = bits[9:]
    mantissa = [1] + mantissa_field

    return exponent, mantissa


def align_positive_mantissas(
    exponent_1: int,
    mantissa_1: list[int],
    exponent_2: int,
    mantissa_2: list[int]
) -> tuple[int, list[int], list[int]]:
    if exponent_1 > exponent_2:
        shift = exponent_1 - exponent_2
        mantissa_2 = [0] * shift + mantissa_2
        mantissa_2 = mantissa_2[:-shift]
        result_exponent = exponent_1
    elif exponent_2 > exponent_1:
        shift = exponent_2 - exponent_1
        mantissa_1 = [0] * shift + mantissa_1
        mantissa_1 = mantissa_1[:-shift]
        result_exponent = exponent_2
    else:
        result_exponent = exponent_1

    return result_exponent, mantissa_1, mantissa_2


def normalize_positive_result(exponent: int, mantissa: list[int]) -> tuple[int, list[int]]:
    if len(mantissa) == 25:
        mantissa = mantissa[:24]
        exponent += 1

    return exponent, mantissa


def pack_positive_ieee754(exponent: int, mantissa: list[int]) -> list[int]:
    exponent_raw = exponent + 127
    exponent_bits = convert_to_binary(exponent_raw)
    exponent_bits = pad_bits(exponent_bits, 8)

    mantissa_field = mantissa[1:]
    mantissa_field = pad_bits(mantissa_field, 23)

    return [0] + exponent_bits + mantissa_field[:23]


def add_positive_ieee754(bits_1: list[int], bits_2: list[int]) -> list[int]:
    exponent_1, mantissa_1 = unpack_positive_ieee754(bits_1)
    exponent_2, mantissa_2 = unpack_positive_ieee754(bits_2)

    result_exponent, mantissa_1, mantissa_2 = align_positive_mantissas(
        exponent_1,
        mantissa_1,
        exponent_2,
        mantissa_2
    )

    result_mantissa = binary_sum(mantissa_1, mantissa_2)
    result_exponent, result_mantissa = normalize_positive_result(
        result_exponent,
        result_mantissa
    )

    return pack_positive_ieee754(result_exponent, result_mantissa)

def change_sign(bits: list[int]) -> list[int]:
    new_bits = bits[:]

    if new_bits[0] == 0:
        new_bits[0] = 1
    else:
        new_bits[0] = 0

    return new_bits


def is_all_zeros(bits: list[int]) -> bool:
    for bit in bits:
        if bit != 0:
            return False
    return True


def compare_bits(bits_1: list[int], bits_2: list[int]) -> int:
    for i in range(len(bits_1)):
        if bits_1[i] > bits_2[i]:
            return 1
        if bits_1[i] < bits_2[i]:
            return -1

    return 0


def subtract_mantissas(mantissa_1: list[int], mantissa_2: list[int]) -> list[int]:
    result = []
    borrow = 0

    for i in range(len(mantissa_1) - 1, -1, -1):
        current = mantissa_1[i] - mantissa_2[i] - borrow

        if current >= 0:
            result.append(current)
            borrow = 0
        else:
            result.append(current + 2)
            borrow = 1

    result.reverse()
    return result


def normalize_after_subtract(exponent: int, mantissa: list[int]) -> tuple[int, list[int]]:
    if is_all_zeros(mantissa):
        return 0, mantissa

    while mantissa[0] == 0:
        mantissa = mantissa[1:] + [0]
        exponent -= 1

    return exponent, mantissa

def add_positive_and_negative_ieee754(bits_1: list[int], bits_2: list[int]) -> list[int]:
    if bits_1[0] != 0:
        raise ValueError("Первое число должно быть положительным")
    if bits_2[0] != 1:
        raise ValueError("Второе число должно быть отрицательным")

    positive_bits = bits_1
    negative_bits = change_sign(bits_2)

    exponent_1, mantissa_1 = unpack_positive_ieee754(positive_bits)
    exponent_2, mantissa_2 = unpack_positive_ieee754(negative_bits)

    result_exponent, mantissa_1, mantissa_2 = align_positive_mantissas(
        exponent_1,
        mantissa_1,
        exponent_2,
        mantissa_2
    )

    compare_result = compare_bits(mantissa_1, mantissa_2)

    if compare_result == 0:
        return [0] * 32

    if compare_result == 1:
        result_sign = 0
        result_mantissa = subtract_mantissas(mantissa_1, mantissa_2)
    else:
        result_sign = 1
        result_mantissa = subtract_mantissas(mantissa_2, mantissa_1)

    result_exponent, result_mantissa = normalize_after_subtract(
        result_exponent,
        result_mantissa
    )

    result_bits = pack_positive_ieee754(result_exponent, result_mantissa)
    result_bits[0] = result_sign

    return result_bits

def ieee754_to_decimal(bits: list[int]) -> float:
    if bits == [0] * 32:
        return 0.0

    sign = bits[0]
    exponent_raw = binary_to_decimal(bits[1:9])

    if exponent_raw == 0:
        return 0.0

    exponent = exponent_raw - 127

    mantissa_field = bits[9:]
    mantissa_int = (1 << 23) + binary_to_decimal(mantissa_field)
    mantissa_value = mantissa_int / (1 << 23)

    result = mantissa_value * (2 ** exponent)

    if sign == 1:
        result = -result

    return result

def make_positive(bits: list[int]) -> list[int]:
    new_bits = bits[:]
    new_bits[0]= 0
    return new_bits

def multiply_mantissas(mantissa_1: list[int], mantissa_2: list[int]) -> list[int]:
    mantissa_1_int = binary_to_decimal(mantissa_1)
    mantissa_2_int = binary_to_decimal(mantissa_2)

    product_int = (mantissa_1_int * mantissa_2_int) >> 23

    product_bits = convert_to_binary(product_int)

    return product_bits

def normalize_after_multiply(exponent: int, mantissa: list[int]) -> tuple[int, list[int]]:
    if len(mantissa) == 25:
        mantissa = mantissa[:-1]
        exponent += 1

    if len(mantissa) < 24:
        mantissa = [0] * (24 - len(mantissa)) + mantissa

    return exponent, mantissa

def mul_ieee754(bits_1: list[int], bits_2: list[int]) -> list[int]:
    result_sign = bits_1[0] ^ bits_2[0]

    positive_bits_1 = make_positive(bits_1)
    positive_bits_2 = make_positive(bits_2)

    exponent_1, mantissa_1 = unpack_positive_ieee754(positive_bits_1)
    exponent_2, mantissa_2 = unpack_positive_ieee754(positive_bits_2)

    result_exponent = exponent_1 + exponent_2

    result_mantissa = multiply_mantissas(mantissa_1, mantissa_2)
    result_exponent, result_mantissa = normalize_after_multiply(
        result_exponent,
        result_mantissa
    )

    result_bits = pack_positive_ieee754(result_exponent, result_mantissa)
    result_bits[0] = result_sign

    return result_bits

def divide_mantissas(mantissa_1: list[int], mantissa_2: list[int]) -> list[int]:
    mantissa_1_int = binary_to_decimal(mantissa_1)
    mantissa_2_int = binary_to_decimal(mantissa_2)

    if mantissa_2_int == 0:
        raise ZeroDivisionError("Деление на ноль")

    quotient_int = (mantissa_1_int << 23) // mantissa_2_int
    quotient_bits = convert_to_binary(quotient_int)

    return quotient_bits


def normalize_after_divide(exponent: int, mantissa: list[int]) -> tuple[int, list[int]]:
    if len(mantissa) > 24:
        mantissa = mantissa[:24]
        exponent += 1

    if len(mantissa) < 24:
        mantissa = [0] * (24 - len(mantissa)) + mantissa

    while mantissa[0] == 0 and not is_all_zeros(mantissa):
        mantissa = mantissa[1:] + [0]
        exponent -= 1

    return exponent, mantissa


def div_ieee754(bits_1: list[int], bits_2: list[int]) -> list[int]:
    positive_bits_1 = make_positive(bits_1)
    positive_bits_2 = make_positive(bits_2)

    exponent_1, mantissa_1 = unpack_positive_ieee754(positive_bits_1)
    exponent_2, mantissa_2 = unpack_positive_ieee754(positive_bits_2)

    if is_all_zeros(mantissa_2):
        raise ZeroDivisionError("Деление на ноль")

    result_sign = bits_1[0] ^ bits_2[0]
    result_exponent = exponent_1 - exponent_2

    result_mantissa = divide_mantissas(mantissa_1, mantissa_2)
    result_exponent, result_mantissa = normalize_after_divide(
        result_exponent,
        result_mantissa
    )

    result_bits = pack_positive_ieee754(result_exponent, result_mantissa)
    result_bits[0] = result_sign

    return result_bits