import re
import json
from Models.formula_parser import FormulaParser

class Formula:
    # Static method to verify if the string is a valid formula
    @staticmethod
    def is_valid_formula(formula_str):
        return isinstance(formula_str, str) and formula_str.startswith('=')

    def __init__(self, input_data):
        if not isinstance(input_data, (str, dict)):
            raise ValueError("Invalid input data type")
        self.parsed_formula = FormulaParser(input_data).parse()

    def to_dict(self):
        return self.parsed_formula
    
    def __str__(self):
        return self.parsed_formula.reconstructed_formula


if __name__ == "__main__":
    # Example usage
    try:
        # parsed_formula = ExcelFormula("=SUM(A1, MAX(B1 + C1, 'Sheet2'!B2), 3 * (A2 + 4))")
        parsed_formula = Formula("=SUM(A1, MAX(B1, C1 + D1))")
        formula_dict = parsed_formula.to_dict()
        print(json.dumps(formula_dict, indent=4))
    except ValueError as e:
        print(e)

    # try:
    #     # Pass a formula string
    #     formula_instance = ExcelFormula("=SUM(A1, MAX(B1 + C1, 'Sheet2'!B2), 3 * (A2 + 4))")
    #     print(formula_instance.reconstruct_formula())  # Reconstruct the formula from parsed JSON

    #     # Pass JSON directly
    #     expected_json = {
    #         "function": "SUM",
    #         "arguments": [
    #             {"cell_reference": "A1"},
    #             {
    #                 "function": "MAX",
    #                 "arguments": [
    #                     {
    #                         "expression": [
    #                             {"cell_reference": "B1"},
    #                             {"operator": "+"},
    #                             {"cell_reference": "C1"}
    #                         ]
    #                     },
    #                     {"constant": "'Sheet2'!B2"}
    #                 ]
    #             },
    #             {
    #                 "expression": [
    #                     {"cell_reference": "A2"},
    #                     {"operator": "+"},
    #                     {"constant": "4"}
    #                 ]
    #             }
    #         ]
    #     }
    #     json_instance = ExcelFormula(expected_json)
    #     print(json_instance.reconstruct_formula())  # Should output the same reconstructed formula
    # except ValueError as e:
    #     print(e)