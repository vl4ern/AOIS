from src.converters import (convert_to_binary, pad_to_all_bits, add_sign, reserve_code, additional_code)
from src.operations import (binary_cum)

number = int(input("Enter number: "))

my_bits = convert_to_binary(abs(number))
print("Перевод в двоичный формат: ", my_bits)

bits_31 = pad_to_all_bits(my_bits)
bits_32 = add_sign(number, bits_31)
print("Переводим в 32-х битный формат: ",bits_32)

rev = reserve_code(bits_31)
rev_bits_32 = add_sign(number, rev)
print("Обратный код: ",rev_bits_32)

add_code = additional_code(bits_32)
print("Дополнительный код: ",add_code)

print("Сумма: ", )