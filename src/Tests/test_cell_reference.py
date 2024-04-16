import pytest
from Objects.cell_reference import CellReference

class TestCellReference:
    def test_valid_cell_references(self):
        # Valid references with and without sheet names
        valid_refs = [
            "A1", "Z999", "'Sheet1'!A1", "'Sheet1'!Z999"
        ]
        for ref in valid_refs:
            cell = CellReference(ref)
            assert str(cell) == ref, f"Expected {ref}, got {str(cell)}"

    def test_invalid_cell_references(self):
        # Invalid references
        invalid_refs = ["1A", "AA", "A0", "ZZZ", "'SheetOne'!A-1", ""]
        for ref in invalid_refs:
            with pytest.raises(ValueError):
                CellReference(ref)

    def test_column_number(self):
        # Test column number calculation
        test_data = {
            "A1": 1,
            "B1": 2,
            "AA1": 27,
            "'Sheet1'!AB1": 28
        }
        for ref, expected_col_num in test_data.items():
            cell = CellReference(ref)
            assert cell.column_number == expected_col_num, f"For {ref}, expected {expected_col_num}, got {cell.column_number}"

    def test_row_number(self):
        # Test row number extraction from cell references
        test_data = {
            "A1": 1,
            "B10": 10,
            "Z999": 999,
            "'Sheet1'!A100": 100
        }
        for ref, expected_row_num in test_data.items():
            cell = CellReference(ref)
            assert cell.row_number == expected_row_num, f"For {ref}, expected row number {expected_row_num}, got {cell.row_number}"


    def test_update_column_and_row(self):
        # Test updating column letter and row number
        cell = CellReference("C3")
        cell.update_column_letter("D")
        cell.update_row_number(4)
        assert str(cell) == "D4", f"Expected 'D4', got {str(cell)}"

    def test_string_representation_with_sheet_name(self):
        # Test string representation with a sheet name
        cell = CellReference("'Sheet2'!E5")
        assert str(cell) == "'Sheet2'!E5", "String representation should include the sheet name"
