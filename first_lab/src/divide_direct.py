from src.constants import MODULE_BITS, TOTAL_BITS
from src.converters import (
    convert_to_binary, pad_to_all_bits, add_sign, binary_to_decimal
)

def devide_direct(number_1:int, number_2:int):
    if number_2 == 0:
        return
    
    sign_first = 1 if number_1 < 0 else 0
    sign_second = 1 if number_2 < 0 else 0
    sign_result = sign_first ^ sign_second

    abs_number_1 = abs(number_1)
    abs_number_2 = abs(number_2)

    devide_abs = abs_number_1 / abs_number_2

    result_devide = round(devide_abs, 5)

    if sign_result:
        result_devide = -result_devide

    bits_number_1 = add_sign(number_1, pad_to_all_bits(convert_to_binary(number_1)))
    bits_number_2 = add_sign(number_2, pad_to_all_bits(convert_to_binary(number_2)))

    print("Прямой код первого числа:", bits_number_1)
    print("Прямой код второго числа: ", bits_number_2)
    print("Результат деления (с точностью до 5 знаков):", format(result_devide, '.5f'))