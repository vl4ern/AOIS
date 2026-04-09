def different_only_in_one_variables(row1: dict[str, int], row2: dict[str,int], target_variable: str, variables: list[str]) -> bool:
    for variable in variables:
        if variable == target_variable:
            continue

        if row1[variable] != row2[variable]:
            return False
        
    return row1[target_variable] != row2[target_variable]