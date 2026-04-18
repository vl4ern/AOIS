def get_minterms(table: list[dict[str, int]], variables: list[str]) -> list[str]:
    minterms = []

    for row in table:
        if row["result"] == 1:
            term = ""

            for variable in variables:
                term += str(row[variable])

            minterms.append(term)

    return minterms

def get_maxterms(table: list[dict[str, int]], variables: list[str]) -> list[str]:
    maxterms = []

    for row in table:
        if row["result"] == 0:
            term = ""

            for variable in variables:
                term += str(row[variable])

            maxterms.append(term)

    return maxterms


def can_combine(term1: str, term2: str) -> bool:
    diff_count = 0

    for i in range(len(term1)):
        if term1[i] != term2[i]:
            diff_count += 1

    return diff_count == 1


def combine_terms(term1: str, term2: str) -> str:
    result = ""

    for i in range(len(term1)):
        if term1[i] == term2[i]:
            result += term1[i]
        else:
            result += "-"

    return result


def combine_all_terms(terms: list[str]) -> tuple[list[str], list[str]]:
    new_terms = []
    used = set()

    for i in range(len(terms)):
        for j in range(i + 1, len(terms)):
            if can_combine(terms[i], terms[j]):
                combined = combine_terms(terms[i], terms[j])
                new_terms.append(combined)

                used.add(terms[i])
                used.add(terms[j])

    new_terms = list(set(new_terms))
    unused_terms = [t for t in terms if t not in used]

    return new_terms, unused_terms


def minimize_by_calculation(terms: list[str]) -> list[str]:
    current_terms = terms
    prime_implicants = []

    while True:
        new_terms, unused = combine_all_terms(current_terms)

        prime_implicants.extend(unused)

        if not new_terms:
            break

        current_terms = new_terms

    return list(set(prime_implicants))


def term_to_expression(term: str, variables: list[str]) -> str:
    parts = []

    for i in range(len(term)):
        if term[i] == "1":
            parts.append(variables[i])
        elif term[i] == "0":
            parts.append("!" + variables[i])

    if not parts:
        return "1"

    return " & ".join(parts)

def term_to_expression_sknf(term: str, variables: list[str]) -> str:
    parts = []

    for i in range(len(term)):
        if term[i] == "0":
            parts.append(variables[i])
        elif term[i] == "1":
            parts.append("!" + variables[i])

    if not parts:
        return "0"

    return "(" + " | ".join(parts) + ")"


def build_expression(terms: list[str], variables: list[str]) -> str:
    expressions = [term_to_expression(t, variables) for t in terms]
    return " | ".join(expressions)

def build_expression_sknf(terms: list[str], variables: list[str]) -> str:
    expressions = [term_to_expression_sknf(t, variables) for t in terms]

    if not expressions:
        return "1"

    return " & ".join(expressions)

def minimize_by_calculation_with_steps(
    terms: list[str]
) -> tuple[list[list[str]], list[str]]:
    stages = []
    current_terms = list(set(terms))
    prime_implicants = []

    while True:
        current_terms = sorted(list(set(current_terms)))
        stages.append(current_terms)

        new_terms, unused = combine_all_terms(current_terms)
        prime_implicants.extend(unused)

        if not new_terms:
            break

        current_terms = new_terms

    prime_implicants = sorted(list(set(prime_implicants)))
    return stages, prime_implicants

def print_minimization_stages(stages: list[list[str]]) -> None:
    for index in range(len(stages)):
        print(f"Stage {index + 1}: {stages[index]}")

def covers(implicant: str, minterm: str) -> bool:
    for i in range(len(implicant)):
        if implicant[i] == "-":
            continue

        if implicant[i] != minterm[i]:
            return False

    return True

def build_coverage_table(
    prime_implicants: list[str],
    minterms: list[str]
) -> dict[str, list[str]]:
    coverage_table = {}

    for implicant in prime_implicants:
        covered_minterms = []

        for minterm in minterms:
            if covers(implicant, minterm):
                covered_minterms.append(minterm)

        coverage_table[implicant] = covered_minterms

    return coverage_table

def print_coverage_table(
    coverage_table: dict[str, list[str]],
    minterms: list[str]
) -> None:
    print("Implicant".ljust(12), end="")
    for minterm in minterms:
        print(minterm.rjust(6), end="")
    print()

    for implicant, covered in coverage_table.items():
        print(implicant.ljust(12), end="")

        for minterm in minterms:
            mark = "X" if minterm in covered else "."
            print(mark.rjust(6), end="")

        print()

def find_essential_implicants(
    coverage_table: dict[str, list[str]],
    minterms: list[str]
) -> list[str]:
    essential = []

    for minterm in minterms:
        covering_implicants = []

        for implicant, covered in coverage_table.items():
            if minterm in covered:
                covering_implicants.append(implicant)

        if len(covering_implicants) == 1:
            essential.append(covering_implicants[0])

    return sorted(list(set(essential)))

def minimize_by_tabular_method(
    minterms: list[str]
) -> tuple[list[list[str]], list[str], dict[str, list[str]], list[str]]:
    stages, prime_implicants = minimize_by_calculation_with_steps(minterms)
    coverage_table = build_coverage_table(prime_implicants, minterms)
    essential_implicants = find_essential_implicants(coverage_table, minterms)

    return stages, prime_implicants, coverage_table, essential_implicants