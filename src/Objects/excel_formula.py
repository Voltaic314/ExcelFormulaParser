import re
import json
from Objects import CellRange, CellReference, ExcelFunction

'''
## TODO: This code should be utilizing the logic from the 
ExcelFunction class but I am too tired to know how to properly implement
it right now. If it ain't broke then don't fix it! haha. But seriously...
This should be reworked a little to support that class otherwise it's just
kinda useless sitting there.
'''

class ExcelFormula:
    
    # this really needs further work to be useful, but for our internal purposes it should be okay.
    @staticmethod
    def is_valid_formula(formula_str):
        return isinstance(formula_str, str) and formula_str.startswith('=')

    def __init__(self, input_data):
        if isinstance(input_data, str):
            if not input_data.startswith('='):
                raise ValueError("Formula must start with an '=' sign.")
            self.original_formula = input_data
            self.parsed_formula = self.parse_expression(input_data[1:])  # Skip the '='
        elif isinstance(input_data, dict):
            self.original_formula = None  # No original formula string
            self.parsed_formula = input_data

    def parse_expression(self, expr):
        expr = str(expr).strip()

        # Check for a function pattern
        if ExcelFunction.is_function_string(expr):
            func = ExcelFunction(expr)
            args = func.arguments
            return {"function": func.name, "arguments": [self.parse_expression(arg) for arg in func.arguments]}
        
        # Check for arithmetic operations
        if any(op in expr for op in ['+', '-', '*', '/']):
            return {"expression": self.parse_operators(expr)}
        
        # Check for a cell range
        if CellRange.is_valid_range(expr):
            return {"cell_range": str(CellRange(str(expr)))}
        
        # Check for a cell reference
        if CellReference.is_valid_reference(expr):
            return {"cell_reference": str(CellReference(str(expr)))}
        
        # Default to constant if no other patterns match
        return {"constant": str(expr)}

    def parse_operators(self, expr):
        parts = re.split(r'(\+|\-|\*|/)', str(expr))
        processed_parts = []
        
        parts = [part for part in parts if part not in ['', ' ', '(', ')'] and part is not None]
        for part in parts:
            part = part.strip()
            if part in ['+', '-', '*', '/']:
                processed_parts.append({"operator": part})
            elif re.match(r"^\d+$", part):
                processed_parts.append({"constant": part})
            else:
                processed_parts.append({"cell_reference": str(CellReference(part))})
        return processed_parts

    def to_dict(self):
        return self.parsed_formula
    
    def reconstruct_formula(self):
        return f"={self._reconstruct(self.parsed_formula)}"

    def _reconstruct(self, json_data):
        if isinstance(json_data, ExcelFunction):
            return str(json_data)
        elif 'expression' in json_data:
            return ' '.join(self._reconstruct(part) for part in json_data['expression'])
        return json_data

    def __str__(self):
        return self.reconstruct_formula()


if __name__ == "__main__":
    # Example usage
    try:
        # parsed_formula = ExcelFormula("=SUM(A1, MAX(B1 + C1, 'Sheet2'!B2), 3 * (A2 + 4))")
        parsed_formula = ExcelFormula("=SUM(A1, MAX(B1, C1 + D1))")
        formula_dict = parsed_formula.to_dict()
        print(json.dumps(formula_dict, indent=4))
    except ValueError as e:
        print(e)

    try:
        # Pass a formula string
        formula_instance = ExcelFormula("=SUM(A1, MAX(B1 + C1, 'Sheet2'!B2), 3 * (A2 + 4))")
        print(formula_instance.reconstruct_formula())  # Reconstruct the formula from parsed JSON

        # Pass JSON directly
        expected_json = {
            "function": "SUM",
            "arguments": [
                {"cell_reference": "A1"},
                {
                    "function": "MAX",
                    "arguments": [
                        {
                            "expression": [
                                {"cell_reference": "B1"},
                                {"operator": "+"},
                                {"cell_reference": "C1"}
                            ]
                        },
                        {"constant": "'Sheet2'!B2"}
                    ]
                },
                {
                    "expression": [
                        {"cell_reference": "A2"},
                        {"operator": "+"},
                        {"constant": "4"}
                    ]
                }
            ]
        }
        json_instance = ExcelFormula(expected_json)
        print(json_instance.reconstruct_formula())  # Should output the same reconstructed formula
    except ValueError as e:
        print(e)