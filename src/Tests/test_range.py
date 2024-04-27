import pytest
import pandas as pd
from Models.range import CellRange

class TestCellRange:

    def test_valid_range_initialization(self):
        """ Test initialization with valid range strings. """
        # Initialization using a single range string
        range = CellRange('A1:C3')
        assert str(range.start_cell) == 'A1'
        assert str(range.end_cell) == 'C3'
        
        # Testing with separate start and end references
        range = CellRange('A1', 'C3')
        assert str(range.start_cell) == 'A1'
        assert str(range.end_cell) == 'C3'

    def test_invalid_range_format(self):
        """ Test initialization with invalid range formats should raise ValueError. """
        with pytest.raises(ValueError):
            CellRange('A1C3')  # No colon separator
        with pytest.raises(ValueError):
            CellRange('A1:')  # Missing end reference
        with pytest.raises(ValueError):
            CellRange(':A1')  # Missing start reference
        with pytest.raises(ValueError):
            CellRange('1A:C3')  # Invalid start reference
        with pytest.raises(ValueError):
            CellRange('A1:3C')  # Invalid end reference

    def test_range_string_representation(self):
        """ Test the string representation of a cell range. """
        range = CellRange('A1', 'B2')
        assert str(range) == 'A1:B2'

    def test_to_dict(self):
        """ Test the dictionary representation of a cell range. """
        range = CellRange('A1', 'C3')
        expected_dict = {
            "range": "A1:C3",
            "components": {
                "start": "A1",
                "end": "C3"
            }
        }
        assert range.to_dict() == expected_dict

    def test_rows_and_columns_in_range(self):
        """ Test getting rows and columns from the range. """
        range = CellRange('A1', 'C3')
        assert range.get_rows_in_range() == [1, 2, 3]
        assert range.get_columns_in_range(as_numbers=True) == [1, 2, 3]
        assert range.get_columns_in_range() == ['A', 'B', 'C']

    def test_cells_in_range(self):
        """ Test getting all cells in the range. """
        range = CellRange('A1', 'B2')
        expected_cells = [['A1', 'B1'], ['A2', 'B2']]
        assert range.get_cells_in_range() == expected_cells

        df = range.get_cells_in_range(as_dataframe=True)
        assert df.equals(pd.DataFrame(expected_cells, index=['Row 1', 'Row 2'], columns=['A', 'B']))
