def get_result_vector(table: list[dict[str,int]]) -> list[int]:
    result_vector = []

    for row in table:
        result_vector.append(row["result"])

    return result_vector

def build_difference_triangle(values: list[int]) -> list[list[int]]:
    triangle = [values]

    while len(triangle[-1]) > 1:
        current_row = triangle[-1]
        next_row = []

        for i in range(len(current_row) - 1):
            next_value = current_row[i] ^ current_row[i+1]
            next_row.append(next_value)

        triangle.append(next_row)

    return triangle

def geta_zheg_coef(triangle: list[list[int]]) -> list[int]:
    coef = []

    for row in triangle:
        coef.append(row[0])

    return coef

def build_monom(index: int, variables: list[str]) -> str:
    if index ==0:
        return "1"
    
    binary = bin(index)[2:].zfill(len(variables))
    parts = []

    for i in range(len(variables)):
        if binary[i] == "1":
            parts.append(variables[i])

    return "".join(parts)

def build_zheg_polyn(coef: list[int], variables: list[str]) -> str:
    terms = []
    for index in range(len(coef)):
        if coef[index] == 1:
            terms.append(build_monom(index, variables))
    if not terms:
        return "0"
    return " ^ ".join(terms)

def build_zheg(table: list[dict[str, int]], variables: list[str]) -> str:
    result_vector = get_result_vector(table)
    triangle = build_difference_triangle(result_vector)
    coef = geta_zheg_coef(triangle)

    return build_zheg_polyn(coef, variables)