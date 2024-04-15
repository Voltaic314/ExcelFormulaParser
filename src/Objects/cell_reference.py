import re
import openpyxl

class CellReference:
    # Updated the regex pattern to ensure it captures expected patterns correctly
    pattern = r"(?:'([^']+)'!)?([A-Z]+)(\d+)$"

    @staticmethod
    def is_valid_reference(cell_ref):
        # Checks if the cell reference is valid
        match = re.match(CellReference.pattern, cell_ref)
        return bool(match) or isinstance(cell_ref, CellReference)

    def __init__(self, cell_ref):
        self.parse_cell_ref(cell_ref)  # Call parsing directly in constructor

    def parse_cell_ref(self, cell_ref):
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
        # Converts the column letter to a number (e.g., "A" -> 1)
        return openpyxl.utils.column_index_from_string(self.column_letter)

    def update_column_letter(self, new_letter):
        # Updates the column letter of the cell reference
        if not new_letter.isalpha():
            raise ValueError("Invalid column letter")
        self.column_letter = new_letter

    def update_row_number(self, new_number):
        # Updates the row number of the cell reference
        if not isinstance(new_number, int) or new_number <= 0:
            raise ValueError("Invalid row number")
        self.row_number = new_number

    def __str__(self):
        # String representation of the cell reference, considering optional sheet name
        if self.sheet_name:
            return f"'{self.sheet_name}'!{self.column_letter}{self.row_number}"
        return f"{self.column_letter}{self.row_number}"

if __name__ == "__main__":
    test_str = "'Sheet1'!A1"
    invalid_refs = ["1A", "AA", "A0", "ZZZ", "'SheetOne'!A-1"]

    for ref in invalid_refs:
        try:
            cell = CellReference(ref)
            print(f"Successfully created cell reference: {cell}")
        except ValueError as e:
            print(f"Error creating cell reference {ref}: {e}")