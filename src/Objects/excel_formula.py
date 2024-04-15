import re
import json
from cell_range import CellRange
from cell_reference import CellReference

'''
## TODO: This code should be utilizing the logic from the 
ExcelFunction class but I am too tired to know how to properly implement
it right now. If it ain't broke then don't fix it! haha. But seriously...
This should be reworked a little to support that class otherwise it's just
kinda useless sitting there.
'''


class ExcelFormula:
    def __init__(self, input_data):
        if isinstance(input_data, str):
            if not input_data.startswith('='):
                raise ValueError("Formula must start with an '=' sign.")
            self.original_formula = input_data
            self.parsed_formula = self.parse_expression(input_data[1:])  # Skip the '='
        elif isinstance(input_data, dict):
            self.original_formula = None  # No original formula string
            self.parsed_formula = input_data  # Assume the input data is already a parsed JSON

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
        # Check for standalone parentheses
        if '(' in expr and not re.match(r"^\w+\(.*\)$", expr.strip()):
            return self.parse_standalone_parentheses(expr)
        if '(' in expr:
            return self.parse_function(expr)
        if '+' in expr or '-' in expr or '*' in expr or '/' in expr:
            return {"expression": self.parse_operators(expr)}
        if re.match(r"([A-Z]+\d+):([A-Z]+\d+)", expr):
            return {"cell_range": str(CellRange(expr))}
        if re.match(r"([A-Z]+\d+)", expr):
            return {"cell_reference": str(CellReference(expr))}
        return {"constant": expr}

    def parse_function(self, expr):
        func_name, args_str = re.match(r"(\w+)\((.*)\)$", expr).groups()
        arguments = self.parse_arguments(args_str)
        return {"function": func_name, "arguments": arguments}

    def parse_operators(self, expr):
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

    def parse_standalone_parentheses(self, expr):
        # This method handles expressions enclosed in parentheses that aren't part of a function call
        inner_expr = re.search(r'\((.*)\)', expr).group(1)
        return self.parse_expression(inner_expr)

    def to_dict(self):
        return self.parsed_formula
    
    def reconstruct_formula(self):
        return f"={self._reconstruct(self.parsed_formula)}"

    def _reconstruct(self, json_data):
        if 'function' in json_data:
            func_name = json_data['function']
            args = [self._reconstruct(arg) for arg in json_data['arguments']]
            return f"{func_name}({', '.join(args)})"
        elif 'expression' in json_data:
            return ''.join(self._reconstruct(part) for part in json_data['expression'])
        elif 'operator' in json_data:
            return f" {json_data['operator']} "
        elif 'cell_reference' in json_data:
            return json_data['cell_reference']
        elif 'cell_range' in json_data:
            return json_data['cell_range']
        elif 'constant' in json_data:
            return json_data['constant']
        return ''
    

    def _list_items(self, data, item_type, as_objects=False):
        result = []
        if isinstance(data, dict):
            if item_type in data:
                if item_type == "cell_reference" and as_objects:
                    # Return actual CellReference objects
                    result.append(CellReference(data[item_type]))
                else:
                    result.append(data[item_type])
            for key in data:
                result.extend(self._list_items(data[key], item_type, as_objects))
        elif isinstance(data, list):
            for item in data:
                result.extend(self._list_items(item, item_type, as_objects))
        return result

    def update_cell_reference(self, old_ref, new_ref):
        def update(data):
            if isinstance(data, dict):
                if 'cell_reference' in data:
                    cell = CellReference(data['cell_reference'])
                    if str(cell) == old_ref:
                        new_cell = CellReference(new_ref)  # Create a new CellReference with the new reference
                        cell.update_column_letter(new_cell.column_letter)
                        cell.update_row_number(new_cell.row_number)
                        data['cell_reference'] = str(cell)  # Update the dictionary with new reference string
                for key in data:
                    update(data[key])
            elif isinstance(data, list):
                for item in data:
                    update(item)
        update(self.parsed_formula)

    def __str__(self):
        return self.reconstruct_formula()

if __name__ == "__main__":
    # Example usage
    try:
        parsed_formula = ExcelFormula("=SUM(A1, MAX(B1 + C1, 'Sheet2'!B2), 3 * (A2 + 4))")
        formula_dict = parsed_formula.to_dict()
        print(json.dumps(formula_dict, indent=4))
    except ValueError as e:
        print(e)

    # Example Usage
    try:
        # Pass a formula string
        formula_instance = ExcelFormula("=SUM(A1, MAX(B1 + C1, 'Sheet2'!B2), 3 * (A2 + 4))")
        print(formula_instance.reconstruct_formula())  # Reconstruct the formula from parsed JSON

        # Pass JSON directly
        json_input = {
            "function": "SUM",
            "arguments": [
                {
                    "cell_reference": "A1"
                },
                {
                    "function": "MAX",
                    "arguments": [
                        {
                            "expression": [
                                {
                                    "cell_reference": "B1"
                                },
                                {
                                    "operator": "+"
                                },
                                {
                                    "cell_reference": "C1"
                                }
                            ]
                        },
                        {
                            "constant": "'Sheet2'!B2"
                        }
                    ]
                },
                {
                    "expression": [
                        {
                            "cell_reference": "A2"
                        },
                        {
                            "operator": "+"
                        },
                        {
                            "constant": "4"
                        }
                    ]
                }
            ]
        }
        json_instance = ExcelFormula(json_input)
        print(json_instance.reconstruct_formula())  # Should output the same reconstructed formula
    except ValueError as e:
        print(e)