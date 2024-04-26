import re 



class Expression:
    operators = ['+', '-', '*', '/', '>', '<', '>=', '<=', '=', '<>']
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
        # Basic check for the presence of an operator
        if not any(op in expr for op in Expression.operators):
            return False
        
        if len(expr) == 1:
            return False # this is a single operator, not an expression
        
        # Check for balanced parentheses
        if not Expression.has_balanced_parentheses(expr):
            return False
        
        # if none of our checks failed, return True
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
        return str(self.original_expression)

    def to_dict(self):
        return {"expression": self.expression}


# Example testing
if __name__ == "__main__":
    # expression_string = "A1 + (B1 + C1) / D1"
    expression_string = "A1 > 0"
    expr = Expression(expression_string)
    print(expr.to_dict())
    print(expr)