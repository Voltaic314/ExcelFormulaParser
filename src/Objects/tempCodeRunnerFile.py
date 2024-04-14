# Example usage of the ExcelFormula class
try:
    formula = ExcelFormula("=SUM(A1, MAX(B1 + C1, 'Sheet2'!B2), 3 * 4)")
    print(formula)
except ValueError as e:
    print(e)