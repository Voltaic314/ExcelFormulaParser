import pytest
from Objects import ExcelFunction

class TestExcelFunction:
    
    def test_valid_function_parsing(self):
        """Test initialization with valid function strings and nested functions."""
        function = ExcelFunction("SUM(1, 2, 3)")
        assert function.name == "SUM"
        assert function.arguments == ["1", "2", "3"], "Should handle simple numeric arguments"

        function = ExcelFunction("AVERAGE(1, 2, SUM(4, 5))")
        assert function.name == "AVERAGE"
        assert len(function.arguments) == 3, "Should correctly parse all arguments"
        assert function.arguments[0] == "1" and function.arguments[1] == "2", "Should parse simple arguments correctly"
        assert isinstance(function.arguments[2], ExcelFunction), "The third argument should be an ExcelFunction instance"
        nested_function = function.arguments[2]
        assert nested_function.name == "SUM", "Nested function should be identified correctly"
        assert nested_function.arguments == ["4", "5"], "Nested function should have the correct arguments"

    def test_invalid_function_parsing(self):
        """Test handling of invalid function strings."""
        with pytest.raises(ValueError):
            ExcelFunction("INVALID(1, 2, 3")

        with pytest.raises(ValueError):
            ExcelFunction("(1, 2, 3)") # because this is an expression, not a function.

        with pytest.raises(ValueError):
            ExcelFunction("MISSINGPARENTHESIS")

        with pytest.raises(ValueError):
            ExcelFunction("SUM((1, 2))")  # Improper nesting

    def test_function_string_representation(self):
        """Test the string representation of the function."""
        function = ExcelFunction("SUM(1, 2, 3)")
        assert str(function) == "SUM(1, 2, 3)", "String representation should match the input format"

        nested_function = ExcelFunction("AVERAGE(1, 2, SUM(4, 5))")
        assert str(nested_function) == "AVERAGE(1, 2, SUM(4, 5))", "Should properly format nested functions in string representation"
