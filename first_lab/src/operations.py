from src.constants import MODULE_BITS, TOTAL_BITS
from src.converters import (
    convert_to_binary, pad_to_all_bits, add_sign,
    reserve_code, additional_code, binary_to_decimal
)

def binary_sum(bits_1: list, bits_2: list[int]) -> list[int]:
    result = []
    ratio = 0

    max_len = max(len(bits_1), len(bits_2))

    bits_1 = [0] * (max_len - len(bits_1)) + bits_1
    bits_2 = [0] * (max_len - len(bits_2)) + bits_2

    for i in range(max_len - 1, -1, -1):
        total = bits_1[i] + bits_2[i] + ratio
        result.append(total % 2)
        ratio = total // 2

    if ratio:
        result.append(ratio)

    result.reverse()
    return result\
    
def to_additional(number: int) -> list[int]:
    abs_bits = pad_to_all_bits(convert_to_binary(abs(number)))
    if number >= 0:
        return add_sign(number, abs_bits)
    else:
        inverted = reserve_code(abs_bits)
        additional_mod = additional_code(inverted)
        return add_sign(number, additional_mod)
    
def from_additional(bits: list[int]) -> int:
    unsigned = binary_to_decimal(bits)
    if bits[0] == 0:
        return unsigned
    else:
        return unsigned - (1 << TOTAL_BITS)
    
def add_additional(a: list[int], b: list[int]) -> list[int]:
    full_sum = binary_sum(a, b)
    if len(full_sum) >= TOTAL_BITS:
        return full_sum[1:]   # берём без первого бита
    else:
        return full_sum
    