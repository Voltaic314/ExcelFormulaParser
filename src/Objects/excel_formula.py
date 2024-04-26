import re
import json
from Objects.cell_reference import CellReference
from Objects.excel_function import ExcelFunction
from Objects.cell_range import CellRange

class ExcelFormula:
    # Static method to verify if the string is a valid formula
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
            self.original_formula = None
            self.parsed_formula = input_data

    def parse_expression(self, expr):
        expr = expr.strip() if isinstance(expr, str) else expr

        # Delegate function parsing to ExcelFunction if it matches the function pattern
        if ExcelFunction.is_function_string(expr):
            func = ExcelFunction(expr)
            return {
                "function": func.name, 
                "arguments": [func.args]
            }
        
        # If the expression includes operators, parse it as an expression
        if any(op in expr for op in ['+', '-', '*', '/']):
            return {"expression": self.parse_operators(expr)}
        
        # Parse ranges and references using the respective classes
        if CellRange.is_valid_range(expr):
            return {"cell_range": str(CellRange(expr))}
        
        if CellReference.is_valid_reference(expr):
            return {"cell_reference": str(CellReference(expr))}
        
        # Treat any other type as a constant
        return {"constant": expr}

    def parse_operators(self, expr):
        expr = expr.strip() if isinstance(expr, str) else expr
        # Use regular expressions to split the expression by operators, respecting spaces
        parts = re.split(r'(\s*[+\-*/]\s*)', expr)
        processed_parts = []

        for part in parts:
            part = part.strip() if isinstance(part, str) else part
            if part in ['+', '-', '*', '/']:
                processed_parts.append({"operator": part})
            elif re.match(r"^\d+$", part):
                processed_parts.append({"constant": part})
            else:
                # Deeper parsing of non-numeric, non-operator parts
                processed_parts.append(self.parse_expression(part))

        return processed_parts

    def to_dict(self):
        return self.parsed_formula
    
    def reconstruct_formula(self):
        return f"={self._reconstruct(self.parsed_formula)}"

    def _reconstruct(self, json_data):
        if isinstance(json_data, dict):
            if 'function' in json_data:
                func_str = json_data['function'] + '(' + ', '.join(self._reconstruct(arg) for arg in json_data['arguments']) + ')'
                return func_str
            if 'expression' in json_data:
                return ' '.join(self._reconstruct(part) for part in json_data['expression'])
            return json_data.get('constant', json_data.get('cell_reference', json_data.get('cell_range', '')))
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