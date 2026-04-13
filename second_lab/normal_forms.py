def build_minterm(row: dict[str,int], variables: list[str]) -> str:
    parts = []

    for variable in variables:
        if row[variable] == 1:
            parts.append(variable)
        else:
            parts.append(f"!{variable}")

    return "(" + " & ".join(parts) + ")"

def build_sdnf(table: list[dict[str,int]], variables: list[str]) -> str:
    minterms_sdnf = []

    for row in table:
        if row["result"] == 1:
            minterm_sdnf = build_minterm(row, variables)
            minterms_sdnf.append(minterm_sdnf)

    if not minterms_sdnf:
        return "0"
    
    return " | ".join(minterms_sdnf)

def build_maxterm(row: dict[str, int], variables: list[str]) -> str:
    parts = []

    for variable in variables:
        if row[variable] == 0:
            parts.append(variable)
        else:
            parts.append(f"!{variable}")

    return "(" + " | ".join(parts) + ")"

def build_sknf(table: list[dict[str,int]], variables: list[str]) -> str:
    maxterms = []

    for row in table:
        if row["result"] == 0:
            maxterm = build_maxterm(row, variables)
            maxterms.append(maxterm)

    if not maxterms:
        return "1"
    
    return " & ".join(maxterms)

def get_row_index(row: dict[str,int], variables: list[str]) -> int:
    binary = ""

    for variable in variables:
        binary += str(row[variable])

    return int(binary,2)

def build_numeric_sdnf(table: list[dict[str, int]], variables: list[str]) -> str:
    indexes = []

    for row in table:
        if row["result"] == 1:
            indexes.append(get_row_index(row, variables))

    if not indexes:
        return "Σ()"
    
    return "Σ(" + ", ".join(map(str,indexes)) + ")"

def build_numeric_sknf(table: list[dict[str, int]], variables: list[str]) -> str:
    indexes = []

    for row in table:
        if row["result"] == 0:
            indexes.append(get_row_index(row, variables))

    if not indexes:
        return "Π()"
    
    return "Π(" + ", ".join(map(str,indexes)) + ")"

def build_index_binary(table: list[dict[str,int]]) -> str:
    bits = []

    for row in table:
        bits.append(str(row["result"]))

    return "".join(bits)

def build_index_decimal(table: list[dict[str,int]]) -> int:
    binary_index = build_index_binary(table)
    return int(binary_index, 2)