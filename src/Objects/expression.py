import re

class Expression:
    pattern = r"^\d+$|^[a-zA-Z_]+\([^\)]*\)$"  # General expression pattern
    operator_pattern = r"[\+\-\*/]"

    @staticmethod
    def has_balanced_parentheses(s):
        balance = 0
        for char in s:
            if char == '(':
                balance += 1
            elif char == ')':
                balance -= 1
            if balance < 0:
                return False
        return balance == 0
    
    @staticmethod
    def is_valid_expression(expr):
        # Ensure the parentheses are balanced
        if not Expression.has_balanced_parentheses(expr):
            return False
        
        # Check for the presence of at least one arithmetic operator
        if not any(op in expr for op in ['+', '-', '*', '/']):
            return False

        # Split the expression by operators and check if there are valid elements around each operator
        parts = re.split(r'[\+\-\*/]', expr)
        parts = [part for part in parts if part]
        if len(parts) < 2:
            return False  # Need at least two operands around an operator

        # Further validation can be added here to ensure each part is a valid number, reference, or sub-expression
        return True

    @staticmethod
    def extract_expression(input_string):
        # Remove any surrounding parentheses
        if input_string.startswith("(") and input_string.endswith(")"):
            return input_string[1:-1]
        return input_string

    def __init__(self, expression):
        
        if "(" in expression and ")" in expression:
            if not self.has_balanced_parentheses(expression):
                raise ValueError("Unbalanced parentheses in expression")
            self.expression = self.extract_expression(expression)
        else:
            self.expression = expression

        self.components = self.split_expression(self.expression)

    def split_expression(self, expr):
        # Split the expression by operators, retaining the operators for analysis
        parts = re.split(r"(\+|\-|\*|\/)", expr)  # Split but keep the operators
        stripped_parts = [part.strip() for part in parts if part.strip()]

        # Remove the leading '=' sign if present in the first component only
        if stripped_parts and stripped_parts[0].startswith("="):
            stripped_parts[0] = stripped_parts[0].lstrip("=")

        return stripped_parts

    def __str__(self):
        return f"Expression: {self.components}"
