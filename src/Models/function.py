import re
from Models.expression import Expression

class Function:
    pattern = r"^([a-zA-Z_]+)\((.*)\)$"  # Matches function name and its arguments

    @staticmethod
    def is_function_string(function_string):
        return bool(re.match(Function.pattern, function_string.strip() if isinstance(function_string, str) else ""))

    def __init__(self, function_string):
        function_string = function_string.strip() if isinstance(function_string, str) else ""
        if not Function.is_function_string(function_string):
            raise ValueError("Invalid function format")
        
        if not Expression.has_balanced_parentheses(function_string):
            raise ValueError("Unbalanced parentheses in function")

        self.name, self.args_str = re.match(Function.pattern, function_string).groups()
        self.args = []

    def parse_arguments(self):
        args, brackets, current_arg = [], 0, []
        for char in self.args_str:
            if char == '(':
                brackets += 1
            elif char == ')':
                brackets -= 1

            if char == ',' and brackets == 0:
                args.append(''.join(current_arg).strip())
                current_arg = []
            else:
                current_arg.append(char)
        
        if current_arg:
            args.append(''.join(current_arg).strip())

        if brackets != 0:
            raise ValueError("Unbalanced parentheses in function arguments")

        self.args = [self.parse_arg(arg) for arg in args]

    def parse_arg(self, arg):
        if Function.is_function_string(arg):
            nested_function = Function(arg)
            nested_function.parse_arguments()
            return nested_function.to_dict()
        return arg  # Treat as plain string if not a function

    def to_dict(self):
        # Ensure arguments are parsed before converting to dictionary
        if not self.args:  # Parse only if not already parsed
            self.parse_arguments()
        return {"function": str(self),
        "components": {
            "name": self.name,
            "arguments": self.args
        }}

    def __str__(self):
        # Ensure arguments are parsed before generating the string representation
        if not self.args:
            self.parse_arguments()
        args_str = ', '.join(str(arg) if isinstance(arg, str) else f"{arg['components']['name']}({', '.join(arg['components']['arguments'])})" for arg in self.args)
        return f"{self.name}({args_str})"


# Example usage to test functionality
if __name__ == "__main__":
        nested_function = Function("AVERAGE(1, 2, SUM(4, 5))")
        nested_function.parse_arguments()  # Parse to ensure correct representation
        print(str(nested_function) == "AVERAGE(1, 2, SUM(4, 5))")