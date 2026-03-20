from src.constants import (MODULE_BITS, SIGN_BIT, TOTAL_BITS)

def convert_to_binary(number: int)->list[int]: #переводим в бинарный
    bits = []
    while number > 0:
        bit = number % 2
        bits.append(bit)
        number //= 2

    bits.reverse()

    return bits

def pad_to_all_bits(bits: list[int]) -> list[int]: #до 31 бита
    count_bits = MODULE_BITS - len(bits)
    return [0]*count_bits + bits

def add_sign(number: int, bits: list[int]) -> list[int]: #добавили знак
    if number < 0:
        return [1] + bits
    else:
        return [0] + bits
    
def reserve_code(bits: list[int]) -> list[int]: #обратный код
    reverse_bits = []
    for bit in bits:
        if bit == 0:
            reverse_bits.append(1)
        else: 
            reverse_bits.append(0)

    return reverse_bits

def additional_code(bits: list[int]) -> list[int]: #дополнительный код
    result = bits[:]
    index = len(result) - 1

    while index >= 0:
        if result[index] == 0:
            result[index] = 1
            break
        else:
            result[index] = 0
            index -= 1

    return result

def binary_to_decimal(bits: list[int]) -> int: #перевод обратно в десятеричную
    result = 0
    for bit in bits:
        result = result * 2 + bit

    return result