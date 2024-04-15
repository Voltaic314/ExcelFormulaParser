import pytest
from Objects import ExcelFormula

class TestExcelFormula:
    def test_valid_formula_parsing(self):
        """ Test parsing of valid formulas. """
        formula = ExcelFormula("=SUM(A1, B1)")
        assert formula.parsed_formula['function'] == "SUM"
        assert "A1" in str(formula.parsed_formula['arguments'][0])
        assert "B1" in str(formula.parsed_formula['arguments'][1])

        formula = ExcelFormula("=A1 + B1")
        assert 'expression' in formula.parsed_formula
        assert "A1" in str(formula.parsed_formula['expression'][0])
        assert '+' in formula.parsed_formula['expression'][1]['operator']
        assert "B1" in str(formula.parsed_formula['expression'][2])

    def test_error_handling(self):
        """ Ensure formulas without '=' raise ValueError. """
        with pytest.raises(ValueError):
            ExcelFormula("SUM(A1, B1)")

    def test_complex_nested_formulas(self):
        """ Test formulas with nested functions and mixed operations. """
        formula = ExcelFormula("=SUM(A1, MAX(B1, C1 + D1))")
        assert formula.parsed_formula['function'] == "SUM"
        assert isinstance(formula.parsed_formula['arguments'][1], ExcelFormula)  # MAX function
        max_func = formula.parsed_formula['arguments'][1]
        assert max_func['function'] == "MAX"
        assert "C1" in str(max_func['arguments'][1]['expression'][0])

    def test_formula_reconstruction(self):
        """ Test reconstructing the formula string from the parsed object. """
        formula = ExcelFormula("=SUM(A1, B1)")
        assert formula.reconstruct_formula() == "=SUM(A1, B1)"
        formula = ExcelFormula("=A1 + B1 - C1 * D1 / E1")
        assert formula.reconstruct_formula() == "=A1 + B1 - C1 * D1 / E1"
        formula = ExcelFormula("=SUM(A1, MAX(B1, C1 + D1))")
        assert formula.reconstruct_formula() == "=SUM(A1, MAX(B1, C1 + D1))"

    def test_json_structure(self):
        """ Test the JSON output against expected dictionary structures. """
        formula = ExcelFormula("=SUM(A1, MAX(B1 + C1, 'Sheet2'!B2), 3 * (A2 + 4))")
        expected_json = {
            "function": "SUM",
            "arguments": [
                {"cell_reference": "A1"},
                {
                    "function": "MAX",
                    "arguments": [
                        {
                            "expression": [
                                {"cell_reference": "B1"},
                                {"operator": "+"},
                                {"cell_reference": "C1"}
                            ]
                        },
                        {"constant": "'Sheet2'!B2"}
                    ]
                },
                {
                    "expression": [
                        {"cell_reference": "A2"},
                        {"operator": "+"},
                        {"constant": "4"}
                    ]
                }
            ]
        }
        # Ensure the parsed JSON matches the expected structure
        assert formula.to_dict() == expected_json

        # Test the reconstruction of the formula from the JSON
        reconstructed_formula = formula.reconstruct_formula()
        assert reconstructed_formula == "=SUM(A1, MAX(B1 + C1, 'Sheet2'!B2), 3 * A2 + 4)"
        assert ExcelFormula(reconstructed_formula).to_dict() == expected_json