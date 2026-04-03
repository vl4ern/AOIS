from parser import (get_variables, to_postfix, tokenize, is_operator, priority)
from evaluator import (apply_operator, evaluate_postfix)

def main():
    expression = "(!a | b) & (c -> (d | !e))"
    tokens = tokenize(expression)
    postfix = to_postfix(tokens)
    values = {"a": 0, "b": 0, "c": 1, "d": 0, "e": 1}

    print(tokens)
    print(postfix)
    print(evaluate_postfix(postfix, values))

if __name__ == "__main__":
    main()