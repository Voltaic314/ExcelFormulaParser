import re

class ExcelFunction:
    pattern = r"([a-zA-Z]+)\((.*)\)$"

    @staticmethod
    def is_function_string(function_string):
        match = re.match(ExcelFunction.pattern, function_string)
        if not match:
            return False
        # find all "(" in the string and make sure the previous character is a letter
        balance = 0
        for index, character in enumerate(function_string):
            previous_character = function_string[index-1] if index else ''
            if character == "(":
                balance += 1
            elif character == ")":
                balance -= 1
            
            if character == "(" and not previous_character.isalpha() and balance == 1:
                return False
        if function_string.count("(") != function_string.count(")"):
            return False
        if not function_string.endswith(")"):
            return False
        return True
    
    def __init__(self, function_string):
        match = re.match(ExcelFunction.pattern, str(function_string))
        self.match = match
        if not bool(self.match):
            raise ValueError("Invalid function format")
        self.name = match.group(1)
        self.arguments = self.parse_arguments(match.group(2))

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
        if current_arg:  # Append the last argument if present
            args.append(''.join(current_arg).strip())

        if brackets != 0:  # Ensure parentheses are balanced
            raise ValueError("Unbalanced parentheses in arguments")

        # Return ExcelFunction objects for nested functions
        return [ExcelFunction(arg) if ExcelFunction.is_function_string(arg) else arg for arg in args]

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