import json
from Objects.cell_reference import CellReference
from Objects.excel_function import ExcelFunction
from Objects.cell_range import CellRange
from Objects.expression import Expression
from Objects.constant import Constant


class FormulaParser:

    def __init__(self, formula_str):
        if not formula_str.startswith('='):
            raise ValueError("Formula must start with an '=' sign.")
        self.formula = formula_str[1:]  # Skip the '=' sign for internal parsing
        self.full_formula = formula_str

    @property
    def reconstructed_formula(self):
        return f"={self.reconstruct()}"

    def parse(self):
        return self.parse_expression(self.formula)

    def parse_expression(self, expr):
        if isinstance(expr, dict):
            # Handle nested parsed expressions
            if 'function' in expr:
                # Re-parse each argument
                expr['arguments'] = [self.parse_expression(arg) for arg in expr['arguments']]
            elif 'expression' in expr:
                # Single expression re-parse
                expr = self.parse_expression(expr['expression'])
            return expr
        elif isinstance(expr, str):
            expr = expr.strip()

            # Delegate function parsing to ExcelFunction if it matches the function pattern
            if ExcelFunction.is_function_string(expr):
                func = ExcelFunction(expr)
                func.parse_arguments()  # Ensure arguments are parsed within ExcelFunction
                return {
                    "function": func.name,
                    "arguments": [self.parse_expression(arg) for arg in func.args]
                }

            # Parse ranges and references using the respective classes
            elif CellRange.is_valid_range(expr):
                range_obj = CellRange(expr)
                return {
                    "cell_range": {
                        "start": range_obj.start_cell.to_dict(),
                        "end": range_obj.end_cell.to_dict()
                    }
                }

            elif CellReference.is_valid_reference(expr):
                ref = CellReference(expr)
                return ref.to_dict()

            # Constants can be parsed directly if they're valid
            elif Constant.is_valid_constant(expr):
                const = Constant(expr)
                return const.to_dict()

            # Catch-all for handling expressions that are not recognized as complete functions
            # or other specific types above.
            elif Expression.is_valid_expression(expr):
                expression_obj = Expression(expr)
                return {
                    "expression": [self.parse_expression(part) for part in expression_obj.expression]
                }

            elif any(op in expr for op in Expression.operators) and len(expr) == 1:
                return {"operator": expr}

            else:
                return {"Unknown Value": expr}

        else:
            return {"Unknown Value": expr}
        

    def to_dict(self):
        return self.parse()

    def __str__(self):
        # Provides a JSON string representation of the parsed formula
        parsed_formula = self.parse()
        return json.dumps(parsed_formula, indent=4)
    
    def reconstruct(self, json_obj=None):
        if json_obj is None:
            json_obj = self.to_dict()
        
        if 'function' in json_obj:
            args_str = ', '.join(self.reconstruct(arg) for arg in json_obj['arguments'])
            return f"{json_obj['function']}({args_str})"
        elif 'cell_reference' in json_obj:
            cell_ref = json_obj['cell_reference']
            sheet_name = cell_ref['sheet_name']
            if not sheet_name:
                return f"{cell_ref['column_letter']}{cell_ref['row_number']}"
            else:
                return f"'{sheet_name}'!{cell_ref['column_letter']}{cell_ref['row_number']}"
        elif 'expression' in json_obj:
            expression_parts = ' '.join(self.reconstruct(part) for part in json_obj['expression'])
            return f"({expression_parts})"
        elif 'operator' in json_obj:
            return json_obj['operator']
        elif 'constant' in json_obj:
            return str(json_obj['constant'])
        else:
            return json_obj['value']
    
    @staticmethod
    def get_all_keys_with_counts(d, keys_count=None):
        """
        Recursively collect and count keys from nested dictionaries if they are within acceptable keys.
        
        Args:
        d (dict): The dictionary to inspect.
        keys_count (dict): A dictionary to collect and count all unique acceptable keys. If None, a new dictionary will be created.

        Returns:
        dict: A dictionary with counts of all acceptable keys found in the dictionary, including nested ones.
        """
        acceptable_keys = {"function", "arguments", "expression",
                        "cell_range", "cell_reference", "constant",
                        "operator", "Unknown Value"}
        if keys_count is None:
            keys_count = {}
        
        for key, value in d.items():
            if key in acceptable_keys:
                if key in keys_count:
                    keys_count[key] += 1
                else:
                    keys_count[key] = 1
            if isinstance(value, dict):
                FormulaParser.get_all_keys_with_counts(value, keys_count)
            elif isinstance(value, list):
                # If the value is a list, iterate over elements that are dictionaries
                for item in value:
                    if isinstance(item, dict):
                        FormulaParser.get_all_keys_with_counts(item, keys_count)

        return keys_count



# Example usage of the FormulaParser class
if __name__ == "__main__":
    # formula = "=SUM(A1, MAX(B1, C1 + D1))"
    # formula = "=AVERAGE(SUM(A1:A10, B1), MAX(C1:C10), MIN(D1 + D2, E1))"
    formula = "=IF(AND(A1 > 0, B1 < 0), SUM(PRODUCT(A1, B2, MAX(C1, C2)), 10), 100)"
    parser = FormulaParser(formula)
    #print(parser)  # Show parsed formula
    print(formula)
    reconstructed_formula = parser.reconstructed_formula  # Reconstruct the formula from parsed JSON
    print(reconstructed_formula)

    print(formula.replace("(", "").replace(")", "") == reconstructed_formula.replace("(", "").replace(")", ""))
    # keys = FormulaParser.get_all_keys_with_counts(parser.parse())
    # print(keys)
    # print("Unknown Value" in keys)  # Check if any unknown values were found
