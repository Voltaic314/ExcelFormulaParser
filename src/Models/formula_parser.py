import json
from Models.reference import Reference
from Models.function import Function
from Models.range import CellRange
from Models.expression import Expression
from Models.constant import Constant


class FormulaParser:

    def __init__(self, formula_str):
        if not formula_str.startswith('='):
            raise ValueError("Formula must start with an '=' sign.")
        if not Expression.has_balanced_parentheses(formula_str):
            raise ValueError("Unbalanced parentheses in formula.")
        self.formula = formula_str[1:]  # Skip the '=' sign for internal parsing
        self.full_formula = formula_str

    @property
    def reconstructed_formula(self):
        return f"={FormulaParser.json_to_string(self.parse())}"

    def parse(self):
        return self.parse_expression(self.formula)

    def parse_expression(self, expr):
        if isinstance(expr, dict):
            # Handle nested parsed expressions
            if 'function' in expr:
                # Re-parse each argument
                expr['components']['arguments'] = [self.parse_expression(arg) for arg in expr['components']['arguments']]
            elif 'expression' in expr:
                # Single expression re-parse
                expr = self.parse_expression(expr['components'])
            return expr
        elif isinstance(expr, str):
            expr = expr.strip()

            # Delegate function parsing to ExcelFunction if it matches the function pattern
            if Function.is_function_string(expr):
                func = Function(expr)
                func.parse_arguments()  # Ensure arguments are parsed within ExcelFunction
                return {
                    "function": str(func), 
                    "components": {
                        "name": func.name,
                        "arguments": [self.parse_expression(arg) for arg in func.args]
                }}

            # Parse ranges and references using the respective classes
            elif CellRange.is_valid_range(expr):
                range_obj = CellRange(expr)
                return range_obj.to_dict()

            elif Reference.is_valid_reference(expr):
                ref = Reference(expr)
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
                    "expression": str(expression_obj),
                    "components": [self.parse_expression(part) for part in expression_obj.expression]
                }

            elif any(op in expr for op in Expression.operators) and len(expr) == 1:
                return {"operator": expr}
        

    def to_dict(self):
        return self.parse()

    def __str__(self):
        # Provides a JSON string representation of the parsed formula
        parsed_formula = self.parse()
        return json.dumps(parsed_formula, indent=4)
    
    @staticmethod
    def json_to_string(json_obj):
        
        if 'function' in json_obj:
            func = json_obj['components']
            args_str = ', '.join(FormulaParser.json_to_string(arg) for arg in json_obj['arguments'])
            return f"{func['name']}({args_str})"
        
        elif 'reference' in json_obj:
            cell_ref = json_obj['components']
            sheet_name = cell_ref['sheet_name']
            if not sheet_name:
                return f"{cell_ref['column_letter']}{cell_ref['row_number']}"
            else:
                return f"'{sheet_name}'!{cell_ref['column_letter']}{cell_ref['row_number']}"
        
        elif 'range' in json_obj:
            range_obj = json_obj['components']
            return f"{range_obj['start']}:{range_obj['end']}"
        
        elif 'expression' in json_obj:
            components = json_obj['components']
            expression_parts = ' '.join(FormulaParser.json_to_string(part) for part in components)
            return f"({expression_parts})"
        
        elif 'operator' in json_obj:
            return json_obj['operator']
        
        elif 'constant' in json_obj:
            return str(json_obj['constant'])
    
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
                        "range", "reference", "constant",
                        "operator"}
        if keys_count is None:
            keys_count = {}
        
        # Function to handle dictionary counting recursively
        def count_keys(item, keys_count):
            for key, value in item.items():
                if key in acceptable_keys:
                    keys_count[key] = keys_count.get(key, 0) + 1
                
                # Recurse into dictionaries
                if isinstance(value, dict):
                    count_keys(value, keys_count)
                # Recurse into each dictionary in a list
                elif isinstance(value, list):
                    for sub_item in value:
                        if isinstance(sub_item, dict):
                            count_keys(sub_item, keys_count)

        count_keys(d, keys_count)
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
