from src.constants import MODULE_BITS, TOTAL_BITS
from src.converters import (
    convert_to_binary, pad_to_all_bits, add_sign, binary_to_decimal
)

def multiplication_of_numbers(number_1:int, number_2:int):
    sign_first = 1 if number_1 < 0 else 0
    sign_second = 1 if number_2 < 0 else 0
    sign_result = sign_first ^ sign_second

    abs_number_1 = abs(number_1)
    abs_number_2 = abs(number_2)

    multiple_abs = abs_number_1 * abs_number_2

    bits_number_1 = add_sign(number_1, pad_to_all_bits(convert_to_binary(number_1)))
    bits_number_2 = add_sign(number_2, pad_to_all_bits(convert_to_binary(number_2)))

    multiple_bits = convert_to_binary(multiple_abs)
    padded_abs = pad_to_all_bits(multiple_bits)
    result_bits = add_sign(-1 if sign_result else 1, padded_abs)

    print("Прямой код первого числа:", bits_number_1)
    print("Прямой код второго числа: ", bits_number_2)
    print("Произведение в прямом коде:", result_bits)

    result_value = multiple_abs if sign_result == 0 else -multiple_abs
    print("Произведение в десятичном:  ", result_value)