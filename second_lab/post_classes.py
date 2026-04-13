def belongs_to_t0(table: list[dict[str, int]]) -> bool:
    return table[0]["result"] == 0

def belongs_to_t1(table: list[dict[str,int]]) -> bool:
    return table[-1]["result"] == 1

def belongs_to_s(table: list[dict[str,int]]) -> bool:
    left = 0
    right = len(table) - 1

    while left < right:
        if table[left]["result"] == table[right]["result"]:
            return False
        
        left += 1
        right -= 1

    return True

def is_less_or_equal(row1: dict[str,int], row2: dict[str, int], variables: list[str]) -> bool:
    for variable in variables:
        if row1[variable] > row2[variable]:
            return False
        
    return True

def belongs_to_m(table: list[dict[str,int]], variables: list[str]) -> bool:
    for i in range(len(table)):
        for j in range(len(table)):
            if is_less_or_equal(table[i], table[j], variables):
                if table[i]["result"] > table[j]["result"]:
                    return False
                
    return True
