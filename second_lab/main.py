from parser import (get_variables, to_postfix, tokenize, is_operator, priority)
from evaluator import (apply_operator, evaluate_postfix)
from truth_table import (build_truth_table, print_truth_table)
from normal_forms import (build_sdnf, build_sknf, build_numeric_sdnf, build_numeric_sknf,
                          build_maxterm, build_index_binary, build_index_decimal, build_minterm)
from post_classes import (belongs_to_m, belongs_to_s, belongs_to_t0, belongs_to_t1)
from polinom_zhegalkina import (build_zheg, get_monom_degree, get_zheg_coef_from_table, belongs_to_l)
from fictive_perem import find_fictive_perem
from bool_deriv import (build_part_deriv_table, build_mixed_derivative_table)
from minimization import (get_minterms, get_maxterms, minimize_by_calculation_with_steps, print_minimization_stages, build_expression,
                            build_expression_sknf, minimize_by_tabular_method, print_coverage_table)
from karnaugh import minimize_by_karnaugh_map, print_karnaugh_map, build_karnaugh_map
def main():
    expression = "((a&b&!c&!d)|!e)|((a&b&!c&!d)|!e)"
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
    fictive_variables = find_fictive_perem(table, variables)
    print("Fictive variables:", fictive_variables)

    for variable in variables:
        derivative_values = build_part_deriv_table(table, variable, variables)
        print(f"Partial derivative by {variable}: {derivative_values}")

    if len(variables) >= 2:
        derivative_ab = build_mixed_derivative_table(table, ["a", "b"], variables)
        print("Mixed derivative by a, b:", derivative_ab)

    if len(variables) >= 3:
        derivative_abc = build_mixed_derivative_table(table, ["a", "b", "c"], variables)
        print("Mixed derivative by a, b, c:", derivative_abc)

    print("---Minimization (calculation method)---")
    minterms = get_minterms(table, variables)
    print("Minterms:", minterms)

    stages, prime_implicants = minimize_by_calculation_with_steps(minterms)
    print_minimization_stages(stages)
    print("Prime implicants:", prime_implicants)
    print("Calculation result:", build_expression(prime_implicants, variables))

    print("---Minimization (tabular-calculation method)---")
    stages, prime_implicants, coverage_table, essential_implicants = minimize_by_tabular_method(minterms)
    print_minimization_stages(stages)
    print("Prime implicants:", prime_implicants)
    print_coverage_table(coverage_table, minterms)
    print("Essential implicants:", essential_implicants)
    print("Tabular-calculation result:", build_expression(essential_implicants, variables))

    print("---Minimization (Karnaugh map method)---")

    if 2 <= len(variables) <= 5:
        if len(variables) <= 4:
            (
                row_labels,
                col_labels,
                grid,
                row_variables,
                col_variables,
                prime_implicants,
                karnaugh_result
            ) = minimize_by_karnaugh_map(table, variables)

            print_karnaugh_map(
                [""],
                row_labels,
                col_labels,
                [grid],
                [],
                row_variables,
                col_variables
            )

            print("Prime implicants:", prime_implicants)
            print("Karnaugh result:", karnaugh_result)
        else:
            (
                layer_labels,
                row_labels,
                col_labels,
                grids,
                layer_variables,
                row_variables,
                col_variables
            ) = build_karnaugh_map(table, variables)

            print_karnaugh_map(
                layer_labels,
                row_labels,
                col_labels,
                grids,
                layer_variables,
                row_variables,
                col_variables
            )

            print("Karnaugh minimization for 5 variables is not implemented yet")
    else:
        print("Karnaugh map supports only 2, 3, 4 or 5 variables")

    print("---Minimization of SKNF (calculation method)---")
    maxterms = get_maxterms(table, variables)
    print("Maxterms:", maxterms)

    stages, prime_implicants = minimize_by_calculation_with_steps(maxterms)
    print_minimization_stages(stages)
    print("Prime implicants:", prime_implicants)
    print("Calculation SKNF result:", build_expression_sknf(prime_implicants, variables))

    print("---Minimization of SKNF (tabular-calculation method)---")
    stages, prime_implicants, coverage_table, essential_implicants = minimize_by_tabular_method(maxterms)
    print_minimization_stages(stages)
    print("Prime implicants:", prime_implicants)
    print_coverage_table(coverage_table, maxterms)
    print("Essential implicants:", essential_implicants)
    print("Tabular-calculation SKNF result:", build_expression_sknf(essential_implicants, variables))


if __name__ == "__main__":
    main()