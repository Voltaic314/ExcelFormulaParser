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
        self.parsed_formula = parser.Parser(input_data).parse()

    def to_dict(self):
        return self.parsed_formula
    
    def __str__(self):
        return self.reconstructed_formula


if __name__ == "__main__":
    # Example usage
    try:
        # parsed_formula = Formula("=SUM(A1, MAX(B1 + C1, 'Sheet2'!B2), 3 * (A2 + 4))")
        parsed_formula = Formula("=SUM(A1, A2)")
        formula_dict = parsed_formula.to_dict()
        print(json.dumps(formula_dict, indent=4))
    except ValueError as e:
        print(e)