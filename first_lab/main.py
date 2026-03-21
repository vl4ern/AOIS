from src.converters import (convert_to_binary, pad_to_all_bits, add_sign, reserve_code, additional_code, binary_to_decimal)
from src.operations import (binary_sum, to_additional, from_additional, add_additional)
from src.multiply_direct import (multiplication_of_numbers)
from src.divide_direct import (devide_direct)
from src.ieee import (decimal_to_ieee754, add_positive_ieee754, bits_to_string, change_sign, add_positive_and_negative_ieee754, ieee754_to_decimal, mul_ieee754, div_ieee754)
from src.code_version import (
    number_to_2421, add_numbers_2421, bcd_2421_to_string, bcd_2421_to_decimal,
)

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

#-------------------------------------------------------

x = int(input("Первое число: "))
y = int(input("Второе число: "))

bx = to_additional(x)
by = to_additional(y)

print("Доп. код x:", bx)
print("Доп. код y:", by)

bsum = add_additional(bx, by)
result = from_additional(bsum)

print("Сумма в двоичном:", bsum)
print("Сумма в десятичном:", result)

#-------------------------------------------------------

a = int(input("Введите первое число: "))
b = int(input("Введите второе число: "))

multiplication_of_numbers(a, b)

#-------------------------------------------------------

a = int(input("Введите делимое: "))
b = int(input("Введите делитель: "))

devide_direct(a, b)

#-------------------------------------------------------

print("\nСЛОЖЕНИЕ ДВУХ ПОЛОЖИТЕЛЬНЫХ ЧИСЕЛ IEEE-754")

first_number = float(input("Введите первое число: "))
second_number = float(input("Введите второе число: "))

first_bits = decimal_to_ieee754(first_number)
second_bits = decimal_to_ieee754(second_number)

result_bits = add_positive_ieee754(first_bits, second_bits)

print("Первое число в IEEE-754: ", bits_to_string(first_bits))
print("Второе число в IEEE-754:", bits_to_string(second_bits))
print("Результат в IEEE-754:   ", bits_to_string(result_bits))
print("Результат list:         ", result_bits)
print("Результат в десятичной:   ", ieee754_to_decimal(result_bits))

print("\nВЫЧИТАНИЕ ДВУХ ЧИСЕЛ IEEE-754")

first_number = float(input("Введите первое число: "))
second_number = float(input("Введите второе число: "))

first_bits = decimal_to_ieee754(first_number)
second_bits = decimal_to_ieee754(second_number)

negative_second_bits = change_sign(second_bits)

result_bits = add_positive_and_negative_ieee754(first_bits, negative_second_bits)

print("Первое число в IEEE-754:  ", bits_to_string(first_bits))
print("Второе число в IEEE-754:  ", bits_to_string(second_bits))
print("Второе число со знаком -: ", bits_to_string(negative_second_bits))
print("Результат в IEEE-754:     ", bits_to_string(result_bits))
print("Результат list:           ", result_bits)
print("Результат в десятичной:   ", ieee754_to_decimal(result_bits))

print("\nУМНОЖЕНИЕ ДВУХ ЧИСЕЛ IEEE-754")

first_number = float(input("Введите первое число: "))
second_number = float(input("Введите второе число: "))

first_bits = decimal_to_ieee754(first_number)
second_bits = decimal_to_ieee754(second_number)

result_bits = mul_ieee754(first_bits, second_bits)

print("Первое число в IEEE-754: ", bits_to_string(first_bits))
print("Второе число в IEEE-754:", bits_to_string(second_bits))
print("Результат в IEEE-754:   ", bits_to_string(result_bits))
print("Результат list:         ", result_bits)
print("Результат в десятичной: ", ieee754_to_decimal(result_bits))

print("\nДЕЛЕНИЕ ДВУХ ЧИСЕЛ IEEE-754")

first_number = float(input("Введите первое число: "))
second_number = float(input("Введите второе число: "))

first_bits = decimal_to_ieee754(first_number)
second_bits = decimal_to_ieee754(second_number)

result_bits = div_ieee754(first_bits, second_bits)

print("Первое число в IEEE-754: ", bits_to_string(first_bits))
print("Второе число в IEEE-754:", bits_to_string(second_bits))
print("Результат в IEEE-754:   ", bits_to_string(result_bits))
print("Результат list:         ", result_bits)
print("Результат в десятичной: ", f"{ieee754_to_decimal(result_bits):.5f}")

#-------------------------------------------------------

print("\nСЛОЖЕНИЕ ДВУХ ЧИСЕЛ В 2421 BCD")

first_number = int(input("Введите первое число: "))
second_number = int(input("Введите второе число: "))

first_bcd = number_to_2421(first_number)
second_bcd = number_to_2421(second_number)

result_bcd = add_numbers_2421(first_number, second_number)
result_decimal = bcd_2421_to_decimal(result_bcd)

print("Первое число в 2421 BCD: ", bcd_2421_to_string(first_bcd))
print("Второе число в 2421 BCD:", bcd_2421_to_string(second_bcd))
print("Результат в 2421 BCD:   ", bcd_2421_to_string(result_bcd))
print("Результат в десятичной: ", result_decimal)