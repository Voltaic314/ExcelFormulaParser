import re
from openpyxl.utils import column_index_from_string

class CellReference:
    pattern = r"(?:'([^']+)'!)?([A-Z]+)(\d+)$"

    @staticmethod
    def is_valid_reference(cell_ref):
        """Check if the provided cell reference is valid."""
        if not cell_ref:
            return False
        match = re.match(CellReference.pattern, cell_ref)
        return bool(match) or isinstance(cell_ref, CellReference)

    def __init__(self, cell_ref):
        """Initialize the CellReference instance by parsing the provided reference."""
        self.parse_cell_ref(cell_ref)

    def parse_cell_ref(self, cell_ref):
        """Parse the cell reference string and set the object attributes."""
        valid = CellReference.is_valid_reference(cell_ref)
        if not valid:
            raise ValueError(f"Invalid cell reference: {cell_ref}")
        match = re.match(CellReference.pattern, cell_ref)
        
        self.sheet_name, self.column_letter, row_number = match.groups()
        self.row_number = int(row_number)
        if self.row_number < 1:
            raise ValueError("Row number must be greater than 0.")

    @property
    def column_number(self):
        """Convert the column letter to a number using openpyxl's utility."""
        return column_index_from_string(self.column_letter)

    def to_dict(self):
        """Create a dictionary representation of the cell reference."""
        return {
            "cell_reference": {
                "sheet_name": self.sheet_name,
                "column_letter": self.column_letter,
                "row_number": self.row_number,
                "column_number": self.column_number
            }
        }

    def update_column_letter(self, new_letter):
        """Update the column letter of the cell reference."""
        if not new_letter.isalpha():
            raise ValueError("Invalid column letter")
        self.column_letter = new_letter

    def update_row_number(self, new_number):
        """Update the row number of the cell reference."""
        if not isinstance(new_number, int) or new_number <= 0:
            raise ValueError("Invalid row number")
        self.row_number = new_number

    def __str__(self):
        """String representation of the cell reference."""
        return f"'{self.sheet_name}'!{self.column_letter}{self.row_number}" if self.sheet_name else f"{self.column_letter}{self.row_number}"

if __name__ == "__main__":
    test_str = "'Sheet1'!A1"
    invalid_refs = ["1A", "AA", "A0", "ZZZ", "'SheetOne'!A-1"]

    failures = 0
    for ref in invalid_refs:
        try:
            cell = CellReference(ref)
            print(f"Successfully created cell reference: {cell}")
        except ValueError as e:
            print(f"Error creating cell reference {ref}: {e}")
            failures += 1

    if failures == len(invalid_refs):
        print("All invalid references failed, as expected.")