from parser import is_operator

def apply_operator(operator: str, stack: list[int]) -> None:
    if operator == "!":
        if not stack:
            raise ValueError("Ошибка: не хватает операнда для '!'")
        
        value = stack.pop()
        stack.append(int(not value))
        return
    
    if len(stack) < 2:
        raise ValueError(f"Ошибка:не хватает операндов для {operator}")
    
    right = stack.pop()
    left = stack.pop()

    if operator == "&":
        stack.append(int(left and right))
    elif operator == "|":
        stack.append(int(left or right))
    elif operator == "->":
        stack.append(int((not left) or right))
    elif operator == "~":
        stack.append(int(left == right))
    else:
        raise ValueError(f"Неизвестный оператор: {operator}")
    
def evaluate_postfix(postfix: list[str], values: dict[str, int]) -> int:
    stack = []
    for token in postfix:
        if token in "abcde":
            if token not in values:
                raise ValueError(f"Для переменной {token} не задано значение")
            stack.append(values[token])
        elif is_operator(token):
            apply_operator(token, stack)
        else:
            raise ValueError(f"Неизвестный токен в постфиксе: {token}")
        
    if len(stack) != 1:
        raise ValueError("Ошибка вычисления выражения")
    return stack[0]