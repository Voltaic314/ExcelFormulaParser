import re
import json
from cell_range import CellRange
from cell_reference import CellReference
from excel_function import ExcelFunction

class ExcelFormula:
    def __init__(self, formula_str):
        if not formula_str.startswith('='):
            raise ValueError("Formula must start with an '=' sign.")
        
        self.original_formula = formula_str
        self.parsed_formula = self.parse_formula(formula_str[1:])  # Skip the '=' for parsing

    def parse_formula(self, formula_str):
        return self.parse_expression(formula_str)

    def parse_arguments(self, args_str):
        args = []
        brackets = 0
        current_arg = []
        for char in args_str:
            if char == '(':
                brackets += 1
            elif char == ')':
                brackets -= 1
            if char == ',' and brackets == 0 and current_arg:
                args.append(''.join(current_arg).strip())
                current_arg = []
            else:
                current_arg.append(char)
        if current_arg:  # Ensure the last argument is added
            args.append(''.join(current_arg).strip())
        return [self.parse_expression(arg) for arg in args]

    def parse_expression(self, expr):
        if '(' in expr:
            if re.match(r"(\w+)\((.*)\)$", expr):
                return self.parse_function(expr)
        if '+' in expr or '-' in expr or '*' in expr or '/' in expr:
            return {"expression": self.parse_operators(expr)}
        if re.match(r"([A-Z]+\d+):([A-Z]+\d+)", expr):
            return self.parse_range(expr)
        if re.match(r"([A-Z]+\d+)", expr):
            return {"cell_reference": str(CellReference(expr))}
        return {"constant": expr}

    def parse_function(self, expr):
        func_name = re.findall(r"(\w+)", expr)[0]
        args_str = re.findall(r"\((.*)\)$", expr)[0]
        arguments = self.parse_arguments(args_str)
        return {"function": func_name, "arguments": arguments}

    def parse_operators(self, expr):
        # This method should ideally split the expression based on operators and parse each component
        parts = re.split(r'(\+|\-|\*|/)', expr)
        processed_parts = []
        for part in parts:
            if part.strip() in ['+', '-', '*', '/']:
                processed_parts.append({"operator": part})
            elif re.match(r"^\d+$", part.strip()):
                processed_parts.append({"constant": part.strip()})
            else:
                processed_parts.append({"cell_reference": str(CellReference(part.strip()))})
        return processed_parts

    def to_dict(self):
        # This method converts the parsed formula into a dictionary format
        return self.parsed_formula

    def __str__(self):
        return json.dumps(self.parsed_formula, indent=4)
    
if __name__ == "__main__":
    # Example usage
    try:
        parsed_formula = ExcelFormula("=SUM(A1, MAX(B1 + C1, 'Sheet2'!B2), 3 * 4)")
        formula_dict = parsed_formula.to_dict()
        print(json.dumps(formula_dict, indent=4))
    except ValueError as e:
        print(e)
