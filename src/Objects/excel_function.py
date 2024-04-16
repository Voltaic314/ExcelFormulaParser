import re
from Objects.expression import Expression


class ExcelFunction(Expression):
    pattern = r"([a-zA-Z_]+)\((.*)\)$"  # Function name pattern

    @staticmethod
    def is_function_string(function_string):
        return bool(re.fullmatch(ExcelFunction.pattern, function_string.strip()))
    
    def __init__(self, function_string):
        if not ExcelFunction.is_function_string(function_string):
            raise ValueError("Invalid function format")
        name, args_str = re.match(ExcelFunction.pattern, function_string.strip()).groups()
        super().__init__(args_str)
        self.name = name
        self.arguments = self.parse_arguments(self.expression)

    def parse_arguments(self, args_str):
        args, brackets, current_arg = [], 0, []
        for char in args_str:
            if char == '(':
                brackets += 1
            elif char == ')':
                brackets -= 1
            if char == ',' and brackets == 0:
                if current_arg:
                    arg = ''.join(current_arg).strip()
                    if not self.is_valid_expression(arg):
                        raise ValueError(f"Invalid argument format: {arg}")
                    args.append(arg)
                    current_arg = []
            else:
                current_arg.append(char)
        if current_arg:
            arg = ''.join(current_arg).strip()
            if not self.is_valid_expression(arg):
                raise ValueError(f"Invalid argument format: {arg}")
            args.append(arg)

        if brackets != 0:
            raise ValueError("Unbalanced parentheses in arguments")
        
        return args

    def __str__(self):
        args_str = ', '.join(str(arg) for arg in self.arguments)
        return f"{self.name}({args_str})"



if __name__ == "__main__":
    invalid_func_strs = ['INVALID(1, 2, 3', "(1, 2, 3)", 
                         "MISSINGPARENTHESIS", "SUM((1, 2))", 
                         "SUM(1, 2, 3)"]
    
    for func_str in invalid_func_strs:
        try:
            function = ExcelFunction(func_str)
            print(f"Successfully created function: {function}")
        except ValueError as e:
            print(f"Error creating function {func_str}: {e}")