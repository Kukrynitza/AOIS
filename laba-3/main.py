
import string
from sorse.table_create import table_create
from sorse.binary_to_decimal import binary_to_decimal
from sorse.process_expression import process_expression
from sorse.minimized_pcnf_by_calculation_method import minimize_sknf_by_calculation_method
from sorse.minimized_pdnf_by_calculation_method import minimize_sdnf_by_calculation_method


if __name__ == '__main__':
    expr = str(input("Введите логическую функцию:"))
    vars, rpn = process_expression(expr)
    print(f"\nВыражение: {expr}")
    print("Переменные:", vars)
    print("RPN:", rpn),
    table_info = table_create(expr, rpn, vars)
    decimal = binary_to_decimal(table_info['index'])
    print(f"{decimal} - Индексная форма: {table_info['index']}")
    print(f"Числовая форма СДНФ: {table_info['pdnf']}")
    print(f"Числовая форма СКНФ: {table_info['pcnf']}")
    print(f"Совершенная дизъюнктивная нормальная форма (СДНФ): {table_info['pdnf_exp_list']}")
    print(f"Совершенная конъюнктивная нормальная форма (СKНФ): {table_info['pcnf_exp_list']}")
    minimized_pdnf_by_calculation_method = minimize_sdnf_by_calculation_method(table_info['pdnf_exp_list'])
    minimized_pcnf_by_calculation_method = minimize_sknf_by_calculation_method(table_info['pcnf_exp_list'])
    print(f"Минимизированная форма (СДНФ) расчетным методом: {minimized_pdnf_by_calculation_method}")
    print(f"Минимизированная форма (СКНФ) расчетным методом: {minimized_pcnf_by_calculation_method}")
    # minimized_pdnf_by_calculation_spreadsheet_method = minimize_sdnf_by_calculation_spreadsheet_method(table_info['pdnf_exp_list'])
    # minimized_pсnf_by_calculation_spreadsheet_method = minimize_sсnf_by_calculation_spreadsheet_method(table_info['pсnf_exp_list'])
    # print(f"Минимизированная форма (СДНФ) расчетно-табличным методом: {minimized_pdnf_by_calculation_spreadsheet_method}")
    # print(f"Минимизированная форма (СКНФ) расчетно-табличным методом: {minimized_pсnf_by_calculation_spreadsheet_method}")

