import re
import json
from Models.parser import Parser

class Formula:
    # Static method to verify if the string is a valid formula
    @staticmethod
    def is_valid_formula(formula_str):
        return isinstance(formula_str, str) and formula_str.startswith('=')

    def __init__(self, input_data):
        if not isinstance(input_data, (str, dict)):
            raise ValueError("Invalid input data type")
        self.parser = Parser(input_data)
        self.parsed_formula = self.parser.parse()

    def __dict__(self):
        return self.parsed_formula
    
    def __str__(self):
        return self.parser.reconstructed_formula
    
    def translate(self, input_cell, output_cell):
        # Translate the formula from input_cell to output_cell
        self.parsed_formula = self.parsed_formula.translate(input_cell, output_cell)


if __name__ == "__main__":
    # Example usage
    try:
        # parsed_formula = ExcelFormula("=SUM(A1, MAX(B1 + C1, 'Sheet2'!B2), 3 * (A2 + 4))")
        parsed_formula = Formula("=SUM(A1, MAX(B1, C1 + D1))")
        formula_dict = dict(parsed_formula)
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