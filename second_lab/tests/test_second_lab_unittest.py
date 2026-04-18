import io
import os
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

PROJECT_ROOT = Path(__file__).resolve().parents[2] / 'second_lab' / 'second_lab'
sys.path.insert(0, str(PROJECT_ROOT))

import bool_deriv
import evaluator
import fictive_perem
import karnaugh
import main
import minimization
import normal_forms
import parser
import polinom_zhegalkina
import post_classes
import truth_table


class BaseTruthTableMixin:
    @staticmethod
    def build_table(expr: str):
        variables = parser.get_variables(expr)
        table = truth_table.build_truth_table(expr)
        return variables, table


class TestParser(unittest.TestCase):
    def test_get_variables_returns_sorted_unique_variables(self):
        self.assertEqual(parser.get_variables('c & a & b & a'), ['a', 'b', 'c'])

    def test_tokenize_handles_all_supported_tokens(self):
        expr = '!(a & b) -> (c | d) ~ e'
        self.assertEqual(
            parser.tokenize(expr),
            ['!', '(', 'a', '&', 'b', ')', '->', '(', 'c', '|', 'd', ')', '~', 'e'],
        )

    def test_tokenize_raises_for_unknown_symbol(self):
        with self.assertRaises(ValueError):
            parser.tokenize('a + b')

    def test_is_operator_and_priority(self):
        self.assertTrue(parser.is_operator('&'))
        self.assertFalse(parser.is_operator('a'))
        self.assertGreater(parser.priority('!'), parser.priority('&'))
        self.assertGreater(parser.priority('&'), parser.priority('->'))

    def test_to_postfix_builds_expected_postfix(self):
        tokens = parser.tokenize('!(a & b) -> c')
        self.assertEqual(parser.to_postfix(tokens), ['a', 'b', '&', '!', 'c', '->'])

    def test_to_postfix_raises_for_extra_closing_bracket(self):
        with self.assertRaises(ValueError):
            parser.to_postfix(['a', ')'])

    def test_to_postfix_raises_for_unclosed_bracket(self):
        with self.assertRaises(ValueError):
            parser.to_postfix(['(', 'a', '&', 'b'])

    def test_to_postfix_raises_for_unknown_token(self):
        with self.assertRaises(ValueError):
            parser.to_postfix(['a', '?'])


class TestEvaluator(unittest.TestCase):
    def test_apply_operator_not(self):
        stack = [0]
        evaluator.apply_operator('!', stack)
        self.assertEqual(stack, [1])

    def test_apply_operator_not_raises_for_missing_operand(self):
        with self.assertRaises(ValueError):
            evaluator.apply_operator('!', [])

    def test_apply_operator_binary_and(self):
        stack = [1, 0]
        evaluator.apply_operator('&', stack)
        self.assertEqual(stack, [0])

    def test_apply_operator_binary_or(self):
        stack = [0, 1]
        evaluator.apply_operator('|', stack)
        self.assertEqual(stack, [1])

    def test_apply_operator_binary_implication(self):
        stack = [1, 0]
        evaluator.apply_operator('->', stack)
        self.assertEqual(stack, [0])

    def test_apply_operator_binary_equivalence(self):
        stack = [1, 1]
        evaluator.apply_operator('~', stack)
        self.assertEqual(stack, [1])

    def test_apply_operator_binary_raises_for_missing_operands(self):
        with self.assertRaises(ValueError):
            evaluator.apply_operator('&', [1])

    def test_apply_operator_raises_for_unknown_operator(self):
        with self.assertRaises(ValueError):
            evaluator.apply_operator('^', [1, 1])

    def test_evaluate_postfix_returns_result(self):
        postfix = ['a', 'b', '&', 'c', '|']
        self.assertEqual(evaluator.evaluate_postfix(postfix, {'a': 1, 'b': 1, 'c': 0}), 1)

    def test_evaluate_postfix_raises_when_variable_missing(self):
        with self.assertRaises(ValueError):
            evaluator.evaluate_postfix(['a'], {})

    def test_evaluate_postfix_raises_for_unknown_token(self):
        with self.assertRaises(ValueError):
            evaluator.evaluate_postfix(['x'], {})

    def test_evaluate_postfix_raises_for_invalid_stack_state(self):
        with self.assertRaises(ValueError):
            evaluator.evaluate_postfix(['a', 'b'], {'a': 1, 'b': 0})


class TestTruthTable(unittest.TestCase):
    def test_generate_combinations_for_two_variables(self):
        self.assertEqual(
            truth_table.generate_combinations(['a', 'b']),
            [
                {'a': 0, 'b': 0},
                {'a': 0, 'b': 1},
                {'a': 1, 'b': 0},
                {'a': 1, 'b': 1},
            ],
        )

    def test_build_truth_table_for_and_expression(self):
        table = truth_table.build_truth_table('a & b')
        self.assertEqual([row['result'] for row in table], [0, 0, 0, 1])

    def test_print_truth_table_outputs_header_and_rows(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            truth_table.print_truth_table(
                [{'a': 0, 'b': 1, 'result': 1}, {'a': 1, 'b': 0, 'result': 0}],
                ['a', 'b'],
            )
        output = buf.getvalue()
        self.assertIn('a b F', output)
        self.assertIn('0 1 1', output)
        self.assertIn('1 0 0', output)


class TestNormalForms(unittest.TestCase, BaseTruthTableMixin):
    def test_build_minterm_and_maxterm(self):
        row = {'a': 0, 'b': 1, 'result': 1}
        self.assertEqual(normal_forms.build_minterm(row, ['a', 'b']), '(!a & b)')
        self.assertEqual(normal_forms.build_maxterm(row, ['a', 'b']), '(a | !b)')

    def test_build_sdnf_and_sknf(self):
        variables, table = self.build_table('a & b')
        self.assertEqual(normal_forms.build_sdnf(table, variables), '(a & b)')
        self.assertEqual(
            normal_forms.build_sknf(table, variables),
            '(a | b) & (a | !b) & (!a | b)',
        )

    def test_build_sdnf_returns_zero_when_no_true_rows(self):
        table = [{'a': 0, 'result': 0}, {'a': 1, 'result': 0}]
        self.assertEqual(normal_forms.build_sdnf(table, ['a']), '0')

    def test_build_sknf_returns_one_when_no_false_rows(self):
        table = [{'a': 0, 'result': 1}, {'a': 1, 'result': 1}]
        self.assertEqual(normal_forms.build_sknf(table, ['a']), '1')

    def test_numeric_forms_and_indexes(self):
        variables, table = self.build_table('a | b')
        self.assertEqual(normal_forms.build_numeric_sdnf(table, variables), 'Σ(1, 2, 3)')
        self.assertEqual(normal_forms.build_numeric_sknf(table, variables), 'Π(0)')
        self.assertEqual(normal_forms.build_index_binary(table), '0111')
        self.assertEqual(normal_forms.build_index_decimal(table), 7)
        self.assertEqual(normal_forms.get_row_index({'a': 1, 'b': 0}, variables), 2)

    def test_numeric_forms_empty_cases(self):
        self.assertEqual(normal_forms.build_numeric_sdnf([{'a': 0, 'result': 0}], ['a']), 'Σ()')
        self.assertEqual(normal_forms.build_numeric_sknf([{'a': 0, 'result': 1}], ['a']), 'Π()')


class TestPostClasses(unittest.TestCase, BaseTruthTableMixin):
    def test_belongs_to_t0_t1_s_for_xor(self):
        variables, table = self.build_table('a | b')
        self.assertTrue(post_classes.belongs_to_t0(table))
        self.assertTrue(post_classes.belongs_to_t1(table))
        self.assertFalse(post_classes.belongs_to_s(table))
        self.assertTrue(post_classes.is_less_or_equal({'a': 0, 'b': 1}, {'a': 1, 'b': 1}, variables))

    def test_belongs_to_m_true_for_and(self):
        variables, table = self.build_table('a & b')
        self.assertTrue(post_classes.belongs_to_m(table, variables))

    def test_belongs_to_m_false_for_not_a(self):
        variables, table = self.build_table('!a')
        self.assertFalse(post_classes.belongs_to_m(table, variables))


class TestZhegalkin(unittest.TestCase, BaseTruthTableMixin):
    def test_result_vector_triangle_and_coefficients(self):
        _, table = self.build_table('a ^ b'.replace('^', '~'))
        # Expression replacement is only to build a stable sample table; coefficients are tested separately below.
        triangle = polinom_zhegalkina.build_difference_triangle([0, 1, 1, 0])
        self.assertEqual(triangle, [[0, 1, 1, 0], [1, 0, 1], [1, 1], [0]])
        self.assertEqual(polinom_zhegalkina.geta_zheg_coef(triangle), [0, 1, 1, 0])

    def test_build_monom_and_polynomial(self):
        self.assertEqual(polinom_zhegalkina.build_monom(0, ['a', 'b']), '1')
        self.assertEqual(polinom_zhegalkina.build_monom(3, ['a', 'b']), 'ab')
        self.assertEqual(
            polinom_zhegalkina.build_zheg_polyn([1, 0, 1, 0], ['a', 'b']),
            '1 ^ a',
        )
        self.assertEqual(polinom_zhegalkina.build_zheg_polyn([0, 0, 0], ['a', 'b']), '0')

    def test_build_zheg_and_related_helpers(self):
        variables, table = self.build_table('a | b')
        coef = polinom_zhegalkina.get_zheg_coef_from_table(table)
        self.assertEqual(polinom_zhegalkina.get_result_vector(table), [0, 1, 1, 1])
        self.assertEqual(coef, [0, 1, 1, 1])
        self.assertEqual(polinom_zhegalkina.build_zheg(table, variables), 'b ^ a ^ ab')
        self.assertEqual(polinom_zhegalkina.get_monom_degree(3), 2)
        self.assertFalse(polinom_zhegalkina.belongs_to_l(coef))
        self.assertTrue(polinom_zhegalkina.belongs_to_l([1, 1, 0, 0]))


class TestFictiveVariables(unittest.TestCase):
    def test_different_only_in_one_variable(self):
        row1 = {'a': 0, 'b': 1, 'result': 1}
        row2 = {'a': 1, 'b': 1, 'result': 1}
        self.assertTrue(fictive_perem.different_only_in_one_variables(row1, row2, 'a', ['a', 'b']))
        self.assertFalse(fictive_perem.different_only_in_one_variables(row1, {'a': 1, 'b': 0}, 'a', ['a', 'b']))

    def test_find_fictive_perem_detects_unused_variable(self):
        table = [
            {'a': 0, 'b': 0, 'result': 0},
            {'a': 0, 'b': 1, 'result': 1},
            {'a': 1, 'b': 0, 'result': 0},
            {'a': 1, 'b': 1, 'result': 1},
        ]
        self.assertTrue(fictive_perem.is_factive_variables(table, 'a', ['a', 'b']))
        self.assertFalse(fictive_perem.is_factive_variables(table, 'b', ['a', 'b']))
        self.assertEqual(fictive_perem.find_fictive_perem(table, ['a', 'b']), ['a'])


class TestBooleanDerivatives(unittest.TestCase, BaseTruthTableMixin):
    def test_get_res_for_value_returns_matching_result(self):
        variables, table = self.build_table('a & b')
        result = bool_deriv.get_res_for_value({'a': 1, 'b': 1}, table, variables)
        self.assertEqual(result, 1)

    def test_get_res_for_value_raises_for_missing_row(self):
        with self.assertRaises(KeyError):
            bool_deriv.get_res_for_value({'a': 0}, [{'b': 0, 'result': 0}], ['a'])

    def test_part_derivative_and_table(self):
        variables, table = self.build_table('a & b')
        row = {'a': 0, 'b': 1, 'result': 0}
        self.assertEqual(bool_deriv.part_deriv(row, 'a', table, variables), 1)
        self.assertEqual(bool_deriv.build_part_deriv_table(table, 'a', variables), [0, 1, 0, 1])

    def test_mixed_derivative_and_table(self):
        variables, table = self.build_table('a & b')
        row = {'a': 0, 'b': 0, 'result': 0}
        self.assertEqual(bool_deriv.mixed_deriv(row, ['a', 'b'], table, variables), 1)
        self.assertEqual(bool_deriv.build_mixed_derivative_table(table, ['a', 'b'], variables), [1, 1, 1, 1])


class TestMinimization(unittest.TestCase, BaseTruthTableMixin):
    def test_get_minterms_and_term_helpers(self):
        variables, table = self.build_table('a | b')
        self.assertEqual(minimization.get_minterms(table, variables), ['01', '10', '11'])
        self.assertTrue(minimization.can_combine('01', '11'))
        self.assertFalse(minimization.can_combine('00', '11'))
        self.assertEqual(minimization.combine_terms('01', '11'), '-1')
        self.assertEqual(minimization.term_to_expression('-1', variables), 'b')
        self.assertEqual(minimization.term_to_expression('--', variables), '1')

    def test_combine_all_terms_and_calculation(self):
        new_terms, unused = minimization.combine_all_terms(['00', '01', '11'])
        self.assertEqual(sorted(new_terms), ['-1', '0-'])
        self.assertEqual(unused, [])
        self.assertEqual(sorted(minimization.minimize_by_calculation(['01', '10', '11'])), ['-1', '1-'])

    def test_build_expression_and_steps(self):
        stages, prime = minimization.minimize_by_calculation_with_steps(['01', '10', '11'])
        self.assertEqual(stages, [['01', '10', '11'], ['-1', '1-']])
        self.assertEqual(prime, ['-1', '1-'])
        self.assertEqual(minimization.build_expression(prime, ['a', 'b']), 'b | a')

    def test_print_minimization_stages_and_coverage_table(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            minimization.print_minimization_stages([['01'], ['0-']])
            minimization.print_coverage_table({'0-': ['00', '01']}, ['00', '01'])
        output = buf.getvalue()
        self.assertIn("Stage 1: ['01']", output)
        self.assertIn('Implicant', output)
        self.assertIn('X', output)

    def test_coverage_and_tabular_method(self):
        coverage = minimization.build_coverage_table(['-1', '1-'], ['01', '10', '11'])
        self.assertEqual(coverage, {'-1': ['01', '11'], '1-': ['10', '11']})
        self.assertTrue(minimization.covers('-1', '01'))
        self.assertFalse(minimization.covers('1-', '01'))
        self.assertEqual(
            minimization.find_essential_implicants(coverage, ['01', '10', '11']),
            ['-1', '1-'],
        )
        stages, prime, coverage_table, essential = minimization.minimize_by_tabular_method(['01', '10', '11'])
        self.assertEqual(stages, [['01', '10', '11'], ['-1', '1-']])
        self.assertEqual(prime, ['-1', '1-'])
        self.assertEqual(coverage_table, coverage)
        self.assertEqual(essential, ['-1', '1-'])


class TestKarnaugh(unittest.TestCase, BaseTruthTableMixin):
    def test_gray_code_and_axes(self):
        self.assertEqual(karnaugh.gray_code(1), ['0', '1'])
        self.assertEqual(karnaugh.gray_code(2), ['00', '01', '11', '10'])
        with self.assertRaises(ValueError):
            karnaugh.gray_code(3)
        self.assertEqual(karnaugh.get_karnaugh_axes(['a', 'b']), (['a'], ['b']))
        self.assertEqual(karnaugh.get_karnaugh_axes(['a', 'b', 'c']), (['a'], ['b', 'c']))
        self.assertEqual(karnaugh.get_karnaugh_axes(['a', 'b', 'c', 'd']), (['a', 'b'], ['c', 'd']))
        with self.assertRaises(ValueError):
            karnaugh.get_karnaugh_axes(['a'])

    def test_build_karnaugh_map_and_print(self):
        variables, table = self.build_table('a | b')
        row_labels, col_labels, grid, row_vars, col_vars = karnaugh.build_karnaugh_map(table, variables)
        self.assertEqual(row_labels, ['0', '1'])
        self.assertEqual(col_labels, ['0', '1'])
        self.assertEqual(grid, [[0, 1], [1, 1]])
        self.assertEqual(row_vars, ['a'])
        self.assertEqual(col_vars, ['b'])

        buf = io.StringIO()
        with redirect_stdout(buf):
            karnaugh.print_karnaugh_map(row_labels, col_labels, grid, row_vars, col_vars)
        output = buf.getvalue()
        self.assertIn('Karnaugh map (a \\ b)', output)
        self.assertIn('0', output)
        self.assertIn('1', output)

    def test_group_helpers(self):
        grid = [[1, 1], [1, 1]]
        self.assertEqual(karnaugh.get_group_sizes(2, 2), [(2, 2), (1, 2), (2, 1), (1, 1)])
        self.assertEqual(karnaugh.get_group_cells(1, 1, 2, 2, 2, 2), frozenset({(1, 1), (1, 0), (0, 1), (0, 0)}))
        self.assertTrue(karnaugh.all_cells_are_ones(frozenset({(0, 0), (0, 1)}), grid))
        self.assertEqual(karnaugh.get_one_cells([[0, 1], [1, 0]]), {(0, 1), (1, 0)})

    def test_groups_implicants_and_reduction(self):
        variables, table = self.build_table('a | b')
        row_labels, col_labels, grid, *_ = karnaugh.build_karnaugh_map(table, variables)
        all_groups = karnaugh.get_all_one_groups(grid)
        self.assertIn(frozenset({(0, 1), (1, 1)}), all_groups)
        self.assertIn(frozenset({(1, 0), (1, 1)}), all_groups)
        self.assertEqual(karnaugh.cell_to_bits((1, 0), row_labels, col_labels), '10')
        self.assertEqual(karnaugh.group_to_implicant(frozenset({(0, 1), (1, 1)}), row_labels, col_labels, variables), '-1')
        reduced = karnaugh.remove_subgroups([
            frozenset({(0, 1)}),
            frozenset({(0, 1), (1, 1)}),
        ])
        self.assertEqual(reduced, [frozenset({(0, 1), (1, 1)})])

    def test_covering_and_selection_helpers(self):
        implicants = ['-1', '1-']
        minterms = ['01', '10', '11']
        self.assertTrue(karnaugh.covers('-1', '11'))
        self.assertFalse(karnaugh.covers('1-', '01'))
        self.assertEqual(karnaugh.find_essential_implicants(implicants, minterms), ['-1', '1-'])
        self.assertEqual(karnaugh.choose_additional_implicants(implicants, ['-1', '1-'], minterms), ['-1', '1-'])
        self.assertEqual(karnaugh.choose_additional_implicants(['0-', '-0'], [], ['00', '01', '10']), ['0-', '-0'])

    def test_minimize_by_karnaugh_map(self):
        variables, table = self.build_table('a | b')
        result = karnaugh.minimize_by_karnaugh_map(table, variables)
        row_labels, col_labels, grid, row_vars, col_vars, selected, expression = result
        self.assertEqual((row_labels, col_labels), (['0', '1'], ['0', '1']))
        self.assertEqual(grid, [[0, 1], [1, 1]])
        self.assertEqual((row_vars, col_vars), (['a'], ['b']))
        self.assertEqual(selected, ['-1', '1-'])
        self.assertEqual(expression, 'b | a')


class TestMain(unittest.TestCase):
    def test_main_runs_and_prints_key_sections(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            main.main()
        output = buf.getvalue()
        self.assertIn('---The trurh table---', output)
        self.assertIn('---SDNF/SKNF---', output)
        self.assertIn('---Post classes---', output)
        self.assertIn('---Minimization (Karnaugh map method)---', output)
        self.assertIn('Karnaugh result:', output)


if __name__ == '__main__':
    unittest.main()
