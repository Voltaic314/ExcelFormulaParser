import pytest
from Models.formula_parser import FormulaParser

class TestFormulaParser:
    
    def test_basic_formula_parsing(self):
        """ Test parsing of simple formulas with no nested functions. """
        formula = "=A1 + B1"
        parser = FormulaParser(formula)
        expected_dict = {
            'expression': 'A1 + B1',
            'components': [
                {'reference': 'A1', 
                'components': {'column_letter': 'A', 
                                'row_number': 1,
                                'sheet_name': None,
                                'column_number': 1}},
                {'operator': '+'},
                {'reference': 'B1', 
                'components': {'column_letter': 'B', 
                                'row_number': 1, 
                                'sheet_name': None,
                                'column_number': 2}}
            ]
        }
        assert parser.to_dict() == expected_dict, "Parsed dictionary should match expected output"
    
    def test_nested_function_parsing(self):
        """ Test parsing of formulas with nested functions. """
        formula = "=SUM(A1, MAX(B1, C1))"
        parser = FormulaParser(formula)
        expected_output = {
            "function": "SUM(A1, MAX(B1, C1))",
            "components": {
                "name": "SUM",
                "arguments": [
                    {
                        'reference': 'A1', 
                        'components': {
                            'column_letter': 'A', 
                            'row_number': 1,
                            'sheet_name': None,  # Assuming the default value when not specified
                            'column_number': 1
                        }
                    },
                    {
                        "function": "MAX(B1, C1)",
                        "components": {
                            "name": "MAX",
                            "arguments": [
                                {
                                    'reference': 'B1', 
                                    'components': {
                                        'column_letter': 'B', 
                                        'row_number': 1,
                                        'sheet_name': None,  # Assuming the default value when not specified
                                        'column_number': 2  # Assuming column B is 2
                                    }
                                },
                                {
                                    'reference': 'C1', 
                                    'components': {
                                        'column_letter': 'C', 
                                        'row_number': 1,
                                        'sheet_name': None,  # Assuming the default value when not specified
                                        'column_number': 3  # Assuming column C is 3
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        }
        assert parser.to_dict() == expected_output, "Nested function parsing should be correct"


    def test_invalid_formula(self):
        """ Test handling of invalid formulas. """
        invalid_formulas = ["A1 + B1", "=(1 + 2", "=SUM((A1, A2)"]
        for formula in invalid_formulas:
            with pytest.raises(ValueError):
                FormulaParser(formula)

    def test_reconstructed_formula(self):
        """ Test the reconstructed formula from parsed output. """
        formula = "=A1 + B1"
        parser = FormulaParser(formula)
        output_formula = parser.reconstructed_formula.replace("(", "").replace(")", "")
        assert formula == output_formula, "Reconstructed formula should match the original"

    def test_get_all_keys_with_counts(self):
        """ Test key counting in parsed formulas. """
        formula = "=SUM(A1, MAX(B1, C1))"
        parser = FormulaParser(formula)
        parsed = parser.to_dict()
        key_counts = FormulaParser.get_all_keys_with_counts(parsed)
        expected_counts = {
            'function': 2, 'arguments': 2, 'reference': 3
        }
        assert key_counts == expected_counts, "Counts of keys should match expected values"
