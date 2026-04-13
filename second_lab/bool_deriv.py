from itertools import product

def get_res_for_value(values: dict[str,int], table: list[dict[str, int]], variables: list[str]) -> int:
    for row in table:
        matches = True

        for variable in variables:
            if row[variable] != values[variable]:
                matches = False
                break

        if matches: 
            return row["result"]
        
    raise ValueError("Не удалось найти строку таблицы для заданных значений")

def part_deriv(row: dict[str,int], variable: str, table: list[dict[str, int]], variables: list[str]) -> int:
    values_zero = {}
    values_one = {}

    for var in variables:
        values_zero[var] = row[var]
        values_one[var] = row[var]

    values_zero[variable] = 0
    values_one[variable] = 1

    result_zero = get_res_for_value(values_zero, table, variables)
    result_one = get_res_for_value(values_one, table, variables)

    return result_zero ^ result_one

def build_part_deriv_table(table: list[dict[str, int]], variable: str, variables: list[str]) -> list[int]:
    deriv_values = []

    for row in table:
        deriv = part_deriv(row, variable, table, variables)
        deriv_values.append(deriv)

    return deriv_values

def mixed_deriv(row: dict[str, int], target_variables: list[str], table: list[dict[str,int]], variables: list[str]) -> int:
    result = 0

    for combination in product([0,1], repeat = len(target_variables)):
        new_values = {}

        for var in variables:
            new_values[var] = row[var]

        for index in range(len(target_variables)):
            target_variable = target_variables[index]
            new_values[target_variable] = combination[index]

        current_result = get_res_for_value(new_values, table, variables)
        result ^= current_result

    return result

def build_mixed_derivative_table(table: list[dict[str, int]], target_variables: list[str], variables: list[str]) -> list[int]:
    derivative_values = []

    for row in table:
        derivative = mixed_deriv(row, target_variables, table, variables)
        derivative_values.append(derivative)

    return derivative_values