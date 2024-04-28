import pytest
from Models.reference import Reference

class TestReference:

    def test_valid_cell_references(self):
        # Valid references with and without sheet names
        valid_refs = [
            "A1", "Z999", "'Sheet1'!A1", "'Sheet1'!Z999"
        ]
        expected_results = [
            {"reference": "A1", "components": {"sheet_name": None, "column_letter": "A", "row_number": 1, "column_number": 1}},
            {"reference": "Z999", "components": {"sheet_name": None, "column_letter": "Z", "row_number": 999, "column_number": 26}},
            {"reference": "'Sheet1'!A1", "components": {"sheet_name": "Sheet1", "column_letter": "A", "row_number": 1, "column_number": 1}},
            {"reference": "'Sheet1'!Z999", "components": {"sheet_name": "Sheet1", "column_letter": "Z", "row_number": 999, "column_number": 26}}
        ]
        for ref, expected in zip(valid_refs, expected_results):
            cell = Reference(ref)
            assert cell.to_dict() == expected, f"Expected {expected}, got {cell.to_dict()}"

    def test_invalid_cell_references(self):
        # Invalid references
        invalid_refs = ["1A", "AA", "A0", "ZZZ", "'SheetOne'!A-1", ""]
        for ref in invalid_refs:
            with pytest.raises(ValueError):
                Reference(ref)

    def test_column_number(self):
        # Test column number calculation
        test_data = {
            "A1": 1,
            "B1": 2,
            "AA1": 27,
            "'Sheet1'!AB1": 28
        }
        for ref, expected_col_num in test_data.items():
            cell = Reference(ref)
            assert cell.column_number == expected_col_num, f"For {ref}, expected {expected_col_num}, got {cell.column_number}"

    def test_update_column_and_row(self):
        # Test updating column letter and row number
        cell = Reference("C3")
        cell.update_column_letter("D")
        cell.update_row_number(4)
        assert str(cell) == "D4", f"Expected 'D4', got {str(cell)}"

        cell = Reference("C3")
        cell.update_column_number(4)
        cell.update_row_number(4)
        assert str(cell) == "D4", f"Expected 'D4', got {str(cell)}"

    def test_string_representation_with_sheet_name(self):
        # Test string representation with a sheet name
        cell = Reference("'Sheet2'!E5")
        assert str(cell) == "'Sheet2'!E5", "String representation should include the sheet name"
