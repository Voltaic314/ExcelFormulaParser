'''
This houses the Excel Function class which basically just 
tells you the function's name and its list of arguments given. 

## TODO: I really want to add a function type / category feature that can classify
the function type and what data types are valid for arguments. Some functions in 
excel require you to pass in specific kinds of data types into specific positional arguments.
So it would be really nice to be able to encapsulate this logic into python somehow.
For now, the logical structure of this OOP class will just be a bit more basic. lol
'''
import re

class ExcelFunction:
    def __init__(self, function_string):
        # Extract function name and argument string
        match = re.match(r"(\w+)\((.*)\)$", function_string)
        if not match:
            raise ValueError("Invalid function format")

        self.name, args_str = match.groups()
        self.arguments = self.parse_arguments(args_str)

    def parse_arguments(self, args_str):
        args = []
        brackets = 0
        current_arg = []
        for char in args_str:
            if char == '(':
                brackets += 1
            elif char == ')':
                brackets -= 1
            if char == ',' and brackets == 0:
                if current_arg:
                    args.append(''.join(current_arg).strip())
                    current_arg = []
            else:
                current_arg.append(char)
        if current_arg:  # Append the last argument
            args.append(''.join(current_arg).strip())
        return args

    def __str__(self):
        args_str = ', '.join(str(arg) for arg in self.arguments)
        return f"{self.name}({args_str})"

