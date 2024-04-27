import pytest
from Models.function import Function

class TestFunction:

    def test_valid_function_parsing(self):
        """Test initialization with valid function strings and nested functions."""
        function = Function("SUM(1, 2, 3)")
        assert function.name == "SUM"
        function.parse_arguments()
        assert function.args == ["1", "2", "3"], "Should handle simple numeric arguments"
        assert function.to_dict()['components']['arguments'] == ["1", "2", "3"], "Dictionary structure should match parsed arguments"

        function = Function("AVERAGE(1, 2, SUM(4, 5))")
        function.parse_arguments()
        assert function.name == "AVERAGE"
        assert len(function.args) == 3, "Should correctly parse all arguments"
        assert function.args[0] == "1" and function.args[1] == "2", "Should parse simple arguments correctly"
        assert 'function' in function.args[2], "The third argument should be a nested function dictionary"

        nested_function = function.args[2]
        assert nested_function['components']['name'] == "SUM", "Nested function should be identified correctly"
        assert nested_function['components']['arguments'] == ["4", "5"], "Nested function should have the correct arguments"

    def test_invalid_function_parsing(self):
        """Test handling of invalid function strings."""
        with pytest.raises(ValueError):
            Function("INVALID(1, 2, 3")

        with pytest.raises(ValueError):
            Function("(1, 2, 3)")  # Because this is an expression, not a function.

        with pytest.raises(ValueError):
            Function("MISSINGPARENTHESIS")


    def test_function_string_representation(self):
        """Test the string representation of the function."""
        function = Function("SUM(1, 2, 3)")
        function.parse_arguments()  # Ensure arguments are parsed before testing representation
        assert str(function) == "SUM(1, 2, 3)", "String representation should match the input format"

        nested_function = Function("AVERAGE(1, 2, SUM(4, 5))")
        nested_function.parse_arguments()  # Parse to ensure correct representation
        assert str(nested_function) == "AVERAGE(1, 2, SUM(4, 5))", "Should properly format nested functions in string representation"
