import re
import json
from Objects.cell_reference import CellReference
from Objects.excel_function import ExcelFunction
from Objects.cell_range import CellRange
from Objects.expression import Expression  # Import the Expression class

class FormulaParser:
    operator_pattern = r'(\+|\-|\*|\/)'  # Regex pattern for splitting by operators

    def __init__(self, formula_str):
        if not formula_str.startswith('='):
            raise ValueError("Formula must start with an '=' sign.")
        self.formula = formula_str[1:]  # Skip the '=' sign for internal parsing

    def parse(self):
        return self.parse_expression(self.formula)

    def parse_expression(self, expr):
        expr = str(expr).strip()

        # Delegate function parsing to ExcelFunction if it matches the function pattern
        if ExcelFunction.is_function_string(expr):
            func = ExcelFunction(expr)
            return {
                "function": func.name, 
                "arguments": [func.arguments]
            }

        # Utilize the Expression class to handle and validate expressions
        if Expression.is_valid_expression(expr):
            expression_obj = Expression(expr)
            return {
                "expression": [self.parse_expression(part) for part in expression_obj.components]
            }

        # Parse ranges and references using the respective classes
        if CellRange.is_valid_range(expr):
            return {"cell_range": str(CellRange(expr))}
        
        if CellReference.is_valid_reference(expr):
            return {"cell_reference": str(CellReference(expr))}
        
        if expr in ['+', '-', '*', '/']:
            return {"operator": expr}
        
        # Treat any other type as a constant
        return {"constant": expr}

    def __str__(self):
        # This provides a basic string representation of the parsed formula as JSON
        return str(self.parse())
    

    def __repr__(self):
        return json.dumps(str(self), indent=4)


# Example usage of the FormulaParser class
if __name__ == "__main__":
    formula = "=SUM(A1, MAX(B1, C1 + D1))"
    formula_parser = FormulaParser(formula)
    parsed_output = formula_parser.parse()
    print(parsed_output)  # Should show components like ['A1', '+', '5']
