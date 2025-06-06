from itertools import product


def truth_table(expression, variables):
    table = []
    expression = expression.replace("!", "not ").replace("&", " and ").replace("|", " or ")

    for values in product([0, 1], repeat=len(variables)):
        env = {var: bool(val) for var, val in zip(variables, values)}
        result = eval(expression, {}, env)
        table.append((values, result))
    return table


def to_sdnf(table, variables):
    terms = []
    for row, result in table:
        if result:
            term = [f"!{var}" if val == 0 else var for var, val in zip(variables, row)]
            terms.append(" & ".join(term))
    return " | ".join(terms)


def combine_terms(term1, term2):
    diffs = [i for i in range(len(term1)) if term1[i] != term2[i]]
    if len(diffs) == 1:
        index = diffs[0]
        return term1[:index] + "-" + term1[index + 1:]
    return None


def minimize_sdnf_by_calculation_spreadsheet_method(expression_str):
    variables = sorted(set(filter(str.isalpha, expression_str)))
    table = truth_table(expression_str, variables)
    sdnf = to_sdnf(table, variables)
    print("Таблица истинности:")
    print(" ".join(variables) + " | F")
    print("-" * (len(variables) * 2 + 4))
    for row, result in table:
        print(" ".join(map(str, row)) + f" | {int(result)}")

    minterms = [row for row, result in table if result]
    minterm_strs = ["".join(str(v) for v in row) for row in minterms]
    print("\nНачальные минтермы:", minterm_strs)

    stages = []
    while minterm_strs:
        new_terms = set()
        used = set()
        for i in range(len(minterm_strs)):
            for j in range(i + 1, len(minterm_strs)):
                combined = combine_terms(minterm_strs[i], minterm_strs[j])
                if combined:
                    new_terms.add(combined)
                    used.add(minterm_strs[i])
                    used.add(minterm_strs[j])

        remaining = set(minterm_strs) - used
        stages.append((minterm_strs, list(new_terms), list(remaining)))
        if not new_terms:
            break
        minterm_strs = list(new_terms)

    print("\nСтадии склеивания:")
    for i, (prev, new, remaining) in enumerate(stages):
        print(f"Шаг {i + 1}:")
        print("  Исходные: ", prev)
        print("  Новые: ", new)
        print("  Остались: ", remaining)
        print()

    minimized_terms = set()
    for _, _, remaining in stages:
        minimized_terms.update(remaining)
    minimized = " | ".join(
        " & ".join(var if bit == "1" else f"!{var}" for var, bit in zip(variables, term) if bit != "-") for term in
        minimized_terms)
    print('СДНФ расчетно-табличным методом, стадии склеивания', sdnf)
    return minimized
