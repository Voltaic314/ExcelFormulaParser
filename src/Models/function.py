import re
from Models.expression import Expression

class Function:
    pattern = r"^([a-zA-Z_]+)\((.*)\)$"  # Matches function name and its arguments

    @staticmethod
    def from_dict(function_dict):
        """Reconstruct the function from its dictionary representation."""
        name = function_dict['components']['name']
        raw_args = function_dict['components']['arguments']
        args = []
        
        for arg in raw_args:
            if isinstance(arg, dict) and 'function' in arg:
                # Recursively reconstruct nested functions
                nested_function = Function.from_dict(arg)
                args.append(nested_function)
            else:
                args.append(arg)

        # Join args into a function string
        args_str = ', '.join(str(a) if isinstance(a, Function) else str(a) for a in args)
        function_str = f"{name}({args_str})"
        return Function(function_str)

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

        def format_arg(arg):
            """Recursively format arguments to string."""
            if isinstance(arg, str):
                return arg
            elif isinstance(arg, dict):
                # Recursively format nested functions or components
                nested_args = ', '.join(format_arg(a) for a in arg['components']['arguments'])
                return f"{arg['components']['name']}({nested_args})"

        args_str = ', '.join(format_arg(arg) for arg in self.args)
        return f"{self.name}({args_str})"


# Example usage to test functionality
if __name__ == "__main__":
        nested_function = Function("AVERAGE(1, 2, SUM(4, 5))")
        nested_function.parse_arguments()  # Parse to ensure correct representation
        print(str(nested_function) == "AVERAGE(1, 2, SUM(4, 5))")
