def generate_combinations(variables: list[int]) -> list[dict[str, int]]:
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