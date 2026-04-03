def get_variables(expression: str) -> list[str]:
    variables = set()

    for char in expression:
        if char in "abcde":
            variables.add(char)

    return sorted(variables)

def tokenize(expression: str) -> list[str]:
    tokens = []
    i = 0

    while i < len(expression):
        char = expression[i]

        if char == " ":
            i += 1
            continue

        if char in "abcde()!&|~":
            tokens.append(char)
            i+= 1
            continue

        if char == "-" and i + 1 < len(expression) and expression[i+1] == ">":
            tokens.append("->")
            i+=2
            continue

        raise ValueError(f"Неизвестный символ: {char}")
    
    return tokens

def is_operator(token: str) -> bool:
    return token in {"!","&","->","|","~"}

def priority(operator: str) -> int:
    priorities = {"!": 5, "&": 4, "|": 3, "->": 2, "~": 1}
    return priorities[operator]

def to_postfix(tokens: list[str]) -> list[str]:
    output = []
    operators = []

    for token in tokens:
        if token in "abcde":
            output.append(token)

        elif token == "(":
            operators.append(token)

        elif token == ")":
            while operators and operators[-1] != "(":
                output.append(operators.pop())

            if not operators:
                raise ValueError("Ошибка: лишняя закрывающаяся скобка.")
            
            operators.pop()

        elif is_operator(token):
            while (
                operators
                and operators[-1] != "("
                and is_operator(operators[-1])
                and priority(operators[-1]) >= priority(token)
            ):
                output.append(operators.pop())

            operators.append(token)

        else:
            raise ValueError(f"Неизвестный токен: {token}")
        
    while operators:
        if operators[-1] == "(":
            raise ValueError("Ошибка: не закрытая скобка")
        
        output.append(operators.pop())

    return output