import pytest
from Objects import CellRange

class TestCellRange:
    def test_valid_range_initialization(self):
        """ Test initialization with valid range strings. """
        range = CellRange('A1:C3')
        assert range.start_cell.__str__() == 'A1'
        assert range.end_cell.__str__() == 'C3'
        
        # Testing with separate start and end references
        range = CellRange('A1', 'C3')
        assert range.start_cell.__str__() == 'A1'
        assert range.end_cell.__str__() == 'C3'

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