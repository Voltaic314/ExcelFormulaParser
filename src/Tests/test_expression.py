import pytest
from Models.expression import Expression


class TestExpression:

    def test_valid_expressions(self):
        """ Test initialization with valid expressions """
        valid_exprs = [
            "A1 + B1",
            "A1 - B2 * C3 / (A4 + B5)",
            "10 > 5",
            "(A1 + A2) * (B1 + B2)"
        ]
        for expr in valid_exprs:
            expression = Expression(expr)
            assert expression.original_expression == expr.strip()
            assert isinstance(expression.expression, list)  # Ensure parsed expression is a list of components
            assert Expression.is_valid_expression(expr)  # Ensure the validity check passes

    def test_invalid_expressions(self):
        """ Test initialization with invalid expressions """
        invalid_exprs = [
            "",  # Empty string
            "+",  # Single operator
            "A1 + (B1 -",  # Unbalanced parentheses
            "A1 + B1 *"
        ]
        for expr in invalid_exprs:
            with pytest.raises(ValueError):
                Expression(expr)

    def test_balanced_parentheses(self):
        """ Test the balanced parentheses check """
        assert Expression.has_balanced_parentheses("(A1 + B1) * (C1 + D1)") == True
        assert Expression.has_balanced_parentheses("(A1 + (B1 + (C1)))") == True
        assert Expression.has_balanced_parentheses("(A1 + B1") == False
        assert Expression.has_balanced_parentheses("A1 + B1)") == False

    def test_expression_parsing(self):
        """ Test parsing detailed structures within expressions """
        expr = "A1 + B1 - C1 * (D1 / E1)"
        expression = Expression(expr)
        expected_components = ['A1', '+', 'B1', '-', 'C1', '*', {'expression': ['D1', '/', 'E1']}]
        assert expression.expression == expected_components

    def test_expression_to_dict(self):
        """ Test the dictionary output of the expression """
        expr = "A1 + B1"
        expression = Expression(expr)
        expected_dict = {
            "expression": "A1 + B1",
            "components": ['A1', '+', 'B1']
        }
        assert expression.to_dict() == expected_dict

    def test_string_representation(self):
        """ Test the string representation of the expression object """
        expr = "A1 + B1"
        expression = Expression(expr)
        assert str(expression) == "A1 + B1"
