def get_variables(expression: str) -> list[str]:
    variables = set()

    for char in expression:
        if char in "abcde":
            variables.add(char)

    return sorted(variables)

def tokenized(expression: str) -> list[str]:
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

def main():
    print(get_variables("c->a | b"))
    print(tokenized("c -> a | b"))

if __name__ == "__main__":
    main()