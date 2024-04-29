import json
from Models.reference import Reference
from Models.function import Function
from Models.range import Range
from Models.expression import Expression
from Models.constant import Constant


class Parser:

    def __init__(self, formula_str):
        if not formula_str.startswith('='):
            raise ValueError("Formula must start with an '=' sign.")
        if not Expression.has_balanced_parentheses(formula_str):
            raise ValueError("Unbalanced parentheses in formula.")
        self.formula = formula_str[1:]  # Skip the '=' sign for internal parsing
        self.full_formula = formula_str
        self.parsed_formula = self.parse()

    @property
    def reconstructed_formula(self):
        parsed_formula = self.parse()
        return f"={Parser.json_to_string(parsed_formula)}"

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
            elif Range.is_valid_range(expr):
                range_obj = Range(expr)
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
        return self.parsed_formula

    def __str__(self):
        # Provides a JSON string representation of the parsed formula
        parsed_formula = self.parse()
        return json.dumps(parsed_formula, indent=4)
    
    @staticmethod
    def json_to_string(json_obj):
        
        if 'function' in json_obj:
            func = json_obj['components']
            args_str = ', '.join(Parser.json_to_string(arg) for arg in func['arguments'])
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
            expression_parts = ' '.join(Parser.json_to_string(part) for part in components)
            
            '''
            The reason we put parenthesis around the expression is because 
            we want to ensure precision in the order of operations in the formula string.
            If this isn't done, information could be lost in translation between 
            the two data types of strings and dictionary structures.
            '''
            return f"({expression_parts})"
        
        elif 'operator' in json_obj:
            return json_obj['operator']
        
        elif 'constant' in json_obj:
            return str(json_obj['constant'])
    
    @staticmethod
    def get_all_keys_with_counts(d, keys_count=None, label=None):
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
        if label:
            acceptable_keys = {label}
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
    

    def translate(self, from_cell, to_cell):
        from_ref = Reference(from_cell)
        to_ref = Reference(to_cell)

        # Calculate shifts
        col_shift = to_ref.column_number - from_ref.column_number
        row_shift = to_ref.row_number - from_ref.row_number

        # Apply translation to the parsed formula
        self.parsed_formula = self.recurse_translate(self.parse(), col_shift, row_shift)

    def recurse_translate(self, data, col_shift, row_shift):
        if isinstance(data, list):
            return [self.recurse_translate(item, col_shift, row_shift) for item in data]
        composite_data_types = ['function', 'expression', 'range'] # also formulas but that doesn't matter here
        data_type = [dt for dt in composite_data_types if dt in data]
        if data_type:
            data_type = data_type[0]
        
        if not data_type and not 'reference' in data:
            return data

        # this whole section feels a little hard coded, 
        # but there's only a few cases so I guess it's okay. 
        if 'reference' in data:
            ref = Reference(data['reference'])
            ref.update_column_number(ref.column_number + col_shift)
            ref.update_row_number(ref.row_number + row_shift)
            data.update(ref.to_dict())

        elif any(data_type):
            # recursively translate all the components of the composite type
            # then update it's dictionary (using the update method) with whatever the changes were if any
            if data_type == 'function':
                arg_updates = [self.recurse_translate(arg, col_shift, row_shift) for arg in data['components']['arguments']]
                data['components']['arguments'] = arg_updates
                if arg_updates:
                    func = Function.from_dict(data)
                    data['function'] = str(func)
            elif data_type == 'expression':
                updated_components = [self.recurse_translate(comp, col_shift, row_shift) for comp in data['components']]
                data.update({"components": updated_components})
                expr = Expression.from_dict(data)
                data.update({"expression": str(expr)})
            elif data_type == 'range':
                data['components']['start'].update(self.recurse_translate(data['components']['start'], col_shift, row_shift))
                data['components']['end'].update(self.recurse_translate(data['components']['end'], col_shift, row_shift))

        return data


# Example usage of the FormulaParser class
if __name__ == "__main__":
    # formula = "=SUM(A1, MAX(B1, C1 + D1))"
    # formula = "=AVERAGE(SUM(A1:A10, B1), MAX(C1:C10), MIN(D1 + D2, E1))"
    formula = "=IF(AND(A1 > 0, B1 < 0), SUM(PRODUCT(A1, B2, MAX(C1, C2)), 10), 100)"
    parser = Parser(formula)
    #print(parser)  # Show parsed formula
    print(formula)
    reconstructed_formula = parser.reconstructed_formula  # Reconstruct the formula from parsed JSON
    print(reconstructed_formula)

    print(formula.replace("(", "").replace(")", "") == reconstructed_formula.replace("(", "").replace(")", ""))
    # keys = FormulaParser.get_all_keys_with_counts(parser.parse())
    # print(keys)
    # print("Unknown Value" in keys)  # Check if any unknown values were found


    # testing formula translation
    formula = "=SUM(A1, B2)"
    # formula = '=A1 + B2'
    parser = Parser(formula)
    parser.translate('A1', 'C3')  # Example: Translate all references as if 'A1' moved to 'C3'
    expected_output = {
        "function": "SUM(C3, D4)",
        "components": {
            "name": "SUM",
            "arguments": [
                {
                    'reference': 'C3', 
                    'components': {
                        'column_letter': 'C', 
                        'row_number': 3,
                        'sheet_name': None,
                        'column_number': 3
                    }
                },
                {
                    'reference': 'D4', 
                    'components': {
                        'column_letter': 'D', 
                        'row_number': 4,
                        'sheet_name': None,
                        'column_number': 4
                    }
                }
            ]
        }
    }
    output_dict = parser.to_dict()
    assert output_dict == expected_output, "Translation should correctly adjust cell references"
