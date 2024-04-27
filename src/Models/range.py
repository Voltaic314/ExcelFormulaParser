import re
import pandas as pd
from openpyxl.utils import column_index_from_string, get_column_letter
from Models.reference import Reference

class CellRange:
    pattern = r"([A-Z]+\d+):([A-Z]+\d+)"  # Class attribute for the regex pattern

    @staticmethod
    def is_valid_range(range_str):
        """Check if the string represents a valid cell range."""
        return bool(re.match(CellRange.pattern, range_str)) or isinstance(range_str, CellRange)

    def __init__(self, start_ref, end_ref=None):
        """Initialize CellRange either from a single range string or from two CellReference objects."""
        if end_ref is None:
            self.start_cell, self.end_cell = self.parse_range(start_ref)
        else:
            self.start_cell = Reference(start_ref)
            self.end_cell = Reference(end_ref)

    def parse_range(self, range_str):
        """Parse a range string into start and end CellReferences."""
        match = re.match(CellRange.pattern, range_str)
        if not match:
            raise ValueError(f"Invalid range format: {range_str}")
        start_ref, end_ref = match.groups()
        return Reference(start_ref), Reference(end_ref)
    
    def get_rows_in_range(self):
        """Return a list of rows covered by the range."""
        return list(range(self.start_cell.row_number, self.end_cell.row_number + 1))

    def get_columns_in_range(self, as_numbers=False):
        """Return a list of columns covered by the range, as numbers or letters."""
        start_col = column_index_from_string(self.start_cell.column_letter)
        end_col = column_index_from_string(self.end_cell.column_letter)
        if as_numbers:
            return list(range(start_col, end_col + 1))
        else:
            return [get_column_letter(col) for col in range(start_col, end_col + 1)]
        
    def get_cells_in_range(self, as_dataframe=False):
        """Return all cells in the range, optionally as a pandas DataFrame."""
        rows = range(self.start_cell.row_number, self.end_cell.row_number + 1)
        cols = range(column_index_from_string(self.start_cell.column_letter), column_index_from_string(self.end_cell.column_letter) + 1)
        cells = [[f"{get_column_letter(col)}{row}" for col in cols] for row in rows]

        if as_dataframe:
            return pd.DataFrame(cells, index=[f"Row {row}" for row in rows], columns=[get_column_letter(col) for col in cols])
        return cells

    def to_dict(self):
        """Create a dictionary representation of the cell range."""
        return {
            "range": str(self),
            "components": {
                "start": str(self.start_cell),
                "end": str(self.end_cell)
            }
        }

    def __str__(self):
        """String representation of the cell range."""
        return f"{self.start_cell}:{self.end_cell}"

if __name__ == "__main__":
    valid_ranges = ['A1:B2', 'C3:D4', 'E5:F6', 'G7:H8']
    invalid_ranges = ['A1B2', 'A1:', ':B2', '1A:B2', 'A1:2B']

    for valid_range in valid_ranges:
        try:
            cell_range = CellRange(valid_range)
            print(f"Successfully created cell range: {cell_range}")
        except ValueError as e:
            print(f"Error creating cell range: {e}")

    for invalid_range in invalid_ranges:
        try:
            cell_range = CellRange(invalid_range)
            print(f"Successfully created cell range: {cell_range}")
        except ValueError as e:
            print(f"Error creating cell range: {e}")
