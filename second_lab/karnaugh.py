from itertools import combinations
from minimization import term_to_expression


def gray_code(bits_count: int) -> list[str]:
    if bits_count == 1:
        return ["0", "1"]

    if bits_count == 2:
        return ["00", "01", "11", "10"]

    raise ValueError("Gray code supports only 1 or 2 bits")


def get_karnaugh_axes(variables: list[str]) -> tuple[list[str], list[str]]:
    count = len(variables)

    if count == 2:
        return [variables[0]], [variables[1]]

    if count == 3:
        return [variables[0]], [variables[1], variables[2]]

    if count == 4:
        return [variables[0], variables[1]], [variables[2], variables[3]]

    raise ValueError("Karnaugh map supports only 2, 3 or 4 variables")


def build_karnaugh_map(
    table: list[dict[str, int]],
    variables: list[str]
) -> tuple[list[str], list[str], list[list[int]], list[str], list[str]]:
    row_variables, col_variables = get_karnaugh_axes(variables)

    row_labels = gray_code(len(row_variables))
    col_labels = gray_code(len(col_variables))

    lookup = {}

    for row in table:
        key = tuple(row[var] for var in variables)
        lookup[key] = row["result"]

    grid = []

    for row_bits in row_labels:
        current_row = []

        for col_bits in col_labels:
            bits = row_bits + col_bits
            key = tuple(int(bit) for bit in bits)
            current_row.append(lookup[key])

        grid.append(current_row)

    return row_labels, col_labels, grid, row_variables, col_variables


def print_karnaugh_map(
    row_labels: list[str],
    col_labels: list[str],
    grid: list[list[int]],
    row_variables: list[str],
    col_variables: list[str]
) -> None:
    print(f"Karnaugh map ({''.join(row_variables)} \\ {''.join(col_variables)})")
    print(" " * 8, end="")

    for col_label in col_labels:
        print(col_label.rjust(4), end="")

    print()

    for i in range(len(row_labels)):
        print(row_labels[i].ljust(8), end="")

        for value in grid[i]:
            print(str(value).rjust(4), end="")

        print()


def get_group_sizes(rows_count: int, cols_count: int) -> list[tuple[int, int]]:
    sizes = []

    for height in [1, 2, 4]:
        if height > rows_count:
            continue

        for width in [1, 2, 4]:
            if width > cols_count:
                continue

            area = height * width

            if area > 0 and (area & (area - 1)) == 0:
                sizes.append((height, width))

    sizes.sort(key=lambda item: item[0] * item[1], reverse=True)
    return sizes


def get_group_cells(
    start_row: int,
    start_col: int,
    height: int,
    width: int,
    rows_count: int,
    cols_count: int
) -> frozenset[tuple[int, int]]:
    cells = []

    for dr in range(height):
        for dc in range(width):
            row = (start_row + dr) % rows_count
            col = (start_col + dc) % cols_count
            cells.append((row, col))

    return frozenset(cells)


def all_cells_are_ones(group_cells: frozenset[tuple[int, int]], grid: list[list[int]]) -> bool:
    for row, col in group_cells:
        if grid[row][col] != 1:
            return False

    return True


def get_all_one_groups(grid: list[list[int]]) -> list[frozenset[tuple[int, int]]]:
    rows_count = len(grid)
    cols_count = len(grid[0])

    groups = set()
    sizes = get_group_sizes(rows_count, cols_count)

    for height, width in sizes:
        for row in range(rows_count):
            for col in range(cols_count):
                group = get_group_cells(
                    row,
                    col,
                    height,
                    width,
                    rows_count,
                    cols_count
                )

                if all_cells_are_ones(group, grid):
                    groups.add(group)

    return list(groups)


def cell_to_bits(
    cell: tuple[int, int],
    row_labels: list[str],
    col_labels: list[str]
) -> str:
    row, col = cell
    return row_labels[row] + col_labels[col]


def group_to_implicant(
    group_cells: frozenset[tuple[int, int]],
    row_labels: list[str],
    col_labels: list[str],
    variables: list[str]
) -> str:
    bit_strings = []

    for cell in group_cells:
        bit_strings.append(cell_to_bits(cell, row_labels, col_labels))

    implicant = ""

    for index in range(len(variables)):
        bits_here = {bits[index] for bits in bit_strings}

        if len(bits_here) == 1:
            implicant += bit_strings[0][index]
        else:
            implicant += "-"

    return implicant


def remove_subgroups(groups: list[frozenset[tuple[int, int]]]) -> list[frozenset[tuple[int, int]]]:
    result = []

    for current in groups:
        is_subgroup = False

        for other in groups:
            if current == other:
                continue

            if current.issubset(other):
                is_subgroup = True
                break

        if not is_subgroup:
            result.append(current)

    return result


def get_one_cells(grid: list[list[int]]) -> set[tuple[int, int]]:
    result = set()

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == 1:
                result.add((row, col))

    return result


def covers(implicant: str, minterm: str) -> bool:
    for i in range(len(implicant)):
        if implicant[i] == "-":
            continue

        if implicant[i] != minterm[i]:
            return False

    return True


def get_minterms_from_table(
    table: list[dict[str, int]],
    variables: list[str]
) -> list[str]:
    minterms = []

    for row in table:
        if row["result"] == 1:
            bits = ""

            for variable in variables:
                bits += str(row[variable])

            minterms.append(bits)

    return minterms


def find_essential_implicants(
    implicants: list[str],
    minterms: list[str]
) -> list[str]:
    essential = []

    for minterm in minterms:
        covering = []

        for implicant in implicants:
            if covers(implicant, minterm):
                covering.append(implicant)

        if len(covering) == 1 and covering[0] not in essential:
            essential.append(covering[0])

    return essential


def choose_additional_implicants(
    implicants: list[str],
    essential: list[str],
    minterms: list[str]
) -> list[str]:
    covered = set()

    for implicant in essential:
        for minterm in minterms:
            if covers(implicant, minterm):
                covered.add(minterm)

    uncovered = [m for m in minterms if m not in covered]

    if not uncovered:
        return essential

    remaining = [imp for imp in implicants if imp not in essential]

    best_choice = None

    for size in range(1, len(remaining) + 1):
        for combo in combinations(remaining, size):
            temp_covered = set(covered)

            for implicant in combo:
                for minterm in minterms:
                    if covers(implicant, minterm):
                        temp_covered.add(minterm)

            if all(minterm in temp_covered for minterm in minterms):
                best_choice = list(combo)
                break

        if best_choice is not None:
            break

    if best_choice is None:
        return essential

    return essential + best_choice


def minimize_by_karnaugh_map(
    table: list[dict[str, int]],
    variables: list[str]
) -> tuple[list[str], list[str], list[list[int]], list[str], list[str], list[str], str]:
    row_labels, col_labels, grid, row_variables, col_variables = build_karnaugh_map(
        table,
        variables
    )

    all_groups = get_all_one_groups(grid)
    prime_groups = remove_subgroups(all_groups)

    implicants = []

    for group in prime_groups:
        implicant = group_to_implicant(group, row_labels, col_labels, variables)

        if implicant not in implicants:
            implicants.append(implicant)

    implicants.sort()

    minterms = get_minterms_from_table(table, variables)
    essential = find_essential_implicants(implicants, minterms)
    selected = choose_additional_implicants(implicants, essential, minterms)

    expression_parts = []

    for implicant in selected:
        expression_parts.append(term_to_expression(implicant, variables))

    expression = " | ".join(expression_parts)

    return (
        row_labels,
        col_labels,
        grid,
        row_variables,
        col_variables,
        selected,
        expression
    )