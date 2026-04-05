from parser import (tokenize, get_variables, to_postfix)
from evaluator import evaluate_postfix

def generate_combinations(variables: list[str]) -> list[dict[str, int]]:
    combinations = []
    count_variables = len(variables)
    total_rows = 2 ** count_variables

    for number in range(total_rows):
        binary = bin(number)[2:].zfill(count_variables)
        row = {}

        for i in range(count_variables):
            row[variables[i]] = int(binary[i])

        combinations.append(row)

    return combinations

def build_truth_table(expression: str) -> list[dict[str, int]]:
    variables = get_variables(expression)
    combinations = generate_combinations(variables)

    tokens = tokenize(expression)
    postfix = to_postfix(tokens)

    table = []

    for row in combinations:
        result = evaluate_postfix(postfix, row)

        full_row = row.copy()
        full_row["result"] = result
        table.append(full_row)

    return table

def print_truth_table(table: list[dict[str,int]], variables: list[str]) -> None:
    print(*variables, "F")

    for row in table:
        values = [row[var] for var in variables]
        print(*values, row["result"])

