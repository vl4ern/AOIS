def different_only_in_one_variables(row1: dict[str, int], row2: dict[str,int], target_variable: str, variables: list[str]) -> bool:
    for variable in variables:
        if variable == target_variable:
            continue

        if row1[variable] != row2[variable]:
            return False
        
    return row1[target_variable] != row2[target_variable]

def is_factive_variables(table: list[dict[str,int]], variable: str, variables: list[str]) -> bool:
    for i in range(len(table)):
        for j in range(i+1, len(table)):
            if different_only_in_one_variables(table[i],table[j],variable,variables):
                if table[i]["result"] != table[j]["result"]:
                    return False
                
    return True

def find_fictive_perem(table: list[dict[str,int]], variables: list[str]) -> list[str]:
    fictive_perem = []

    for variable in variables:
        if is_factive_variables(table, variable, variables):
            fictive_perem.append(variable)

    return fictive_perem