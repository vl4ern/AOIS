from parser import (get_variables, to_postfix, tokenize, is_operator, priority)
from evaluator import (apply_operator, evaluate_postfix)
from truth_table import (build_truth_table, print_truth_table)
from normal_forms import (build_sdnf, build_sknf, build_numeric_sdnf, build_numeric_sknf,
                          build_maxterm, build_index_binary, build_index_decimal, build_minterm)
from post_classes import (belongs_to_l, belongs_to_m, belongs_to_s, belongs_to_t0, belongs_to_t1)
from polinom_zhegalkina import (build_zheg, get_monom_degree, get_zheg_coef_from_table, belongs_to_l)
from fictive_perem import different_only_in_one_variables


def main():
    expression = "a | (b -> c)"
    variables = get_variables(expression)
    table = build_truth_table(expression)
    print("---The trurh table---")
    print("Variables", variables)
    print_truth_table(table, variables)
    print("---SDNF/SKNF---")
    print("SDNF:", build_sdnf(table, variables))
    print("SKNF:", build_sknf(table, variables))
    print("Numeric SDNF:", build_numeric_sdnf(table, variables))
    print("Numeric SKNF:", build_numeric_sknf(table, variables))
    print("Index binary:", build_index_binary(table))
    print("Index demical:", build_index_decimal(table))
    print("---Post classes---")
    print("T0:", belongs_to_t0(table))
    print("T1:", belongs_to_t1(table))
    print("S:", belongs_to_s(table))
    print("M:", belongs_to_m(table, variables))
    coef = get_zheg_coef_from_table(table)
    print("Polinom Zhegalkin:", build_zheg(table, variables))
    print("L:", belongs_to_l(coef))
if __name__ == "__main__":
    main()