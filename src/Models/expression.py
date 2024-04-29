import re 
from Models.model_types import Types


class Expression:
    operators = ['+', '-', '*', '/', '>', '<', '>=', '<=', '=', '<>']
    operator_pattern = '|'.join(re.escape(op) for op in operators)  # Create a regex pattern for splitting

    @staticmethod
    def from_dict(expr_dict):
        """Constructs an Expression object from its dictionary representation."""
        def reconstruct_expression(components):
            parts = []
            for component in components:
                if isinstance(component, dict):
                    # Recursively handle nested expressions
                    if 'expression' in component:
                        nested_expr = reconstruct_expression(component['expression'])
                        parts.append(f"({nested_expr})")
                    elif 'operator' in component:
                        parts.append(component['operator'])
                    elif 'constant' in component:
                        parts.append(str(component['constant']))
                    else:
                        type_str = [item for item in component.keys() if item not in ['components']][0]
                        obj_type = Types(type_str).get_type()
                        instance = obj_type.from_dict(component)
                        parts.append(str(instance))
                else:
                    parts.append(str(component))
            return ' '.join(parts)

        if 'components' in expr_dict:
            expression_string = reconstruct_expression(expr_dict['components'])
        else:
            raise ValueError("Invalid dictionary format for constructing an Expression.")

        return Expression(expression_string)

    def __init__(self, expression):
        self.original_expression = expression.strip()
        if not self.is_valid_expression(self.original_expression):
            raise ValueError("Invalid expression format")
        self.expression = self.parse_expression(self.original_expression)

    @staticmethod
    def has_balanced_parentheses(expr):
        balance = 0
        for char in expr:
            if char == '(':
                balance += 1
            elif char == ')':
                balance -= 1
        return balance == 0

    @staticmethod
    def is_valid_expression(expr):
        if not expr:
            return False  # Empty string is not a valid expression

        # Basic check for the presence of an operator
        if not any(op in expr for op in Expression.operators):
            return False

        # Check for balanced parentheses
        if not Expression.has_balanced_parentheses(expr):
            return False

        # Split expression by operators and check the parts
        parts = re.split(Expression.operator_pattern, expr)
        if any(not part.strip() for part in parts):  # Check if any part is empty or just whitespace
            return False

        return True

    def parse_expression(self, expr):
        # Function to handle recursive parsing
        def parse_recursive(chars):
            components = []
            current = []
            depth = 0

            i = 0
            while i < len(chars):
                char = chars[i]

                if char == '(':
                    if depth == 0 and current:
                        # Add current content before '(' as a new component if it's not just space
                        component = ''.join(current).strip()
                        if component:
                            components.append(component)
                        current = []
                    depth += 1
                elif char == ')':
                    if depth == 1:
                        # Closing the current nested expression
                        if current:
                            component = ''.join(current).strip()
                            if component:
                                components.append({'expression': parse_recursive(current)[0]})
                        current = []
                        depth -= 1
                    else:
                        current.append(char)
                        depth -= 1
                elif depth == 0 and char in Expression.operators:
                    # Add operator and the current content as separate components
                    if current:
                        component = ''.join(current).strip()
                        if component:
                            components.append(component)
                        current = []
                    components.append(char)
                elif char != ' ':
                    # Add non-space characters to the current buffer
                    current.append(char)

                i += 1

            # Add remaining characters after the last operator or parenthesis
            if current:
                component = ''.join(current).strip()
                if component:
                    components.append(component)

            return components, i

        parsed_expr, _ = parse_recursive(list(expr))
        return parsed_expr

    def __str__(self):
        def build_expression_string(components):
            expr_str = []
            for component in components:
                if isinstance(component, dict):
                    if 'expression' in component:
                        expr_str.append('(' + build_expression_string(component['expression']) + ')')
                elif isinstance(component, str):
                    expr_str.append(component)
            return ' '.join(expr_str)

        return build_expression_string(self.expression)

    def to_dict(self):
        return {"expression": str(self), 
                "components": self.expression}


# Example testing
if __name__ == "__main__":
    # expression_string = "A1 + (B1 + C1) / D1"
    expression_string = "A1 > 0"
    expr = Expression(expression_string)
    print(expr.to_dict())
    print(expr)