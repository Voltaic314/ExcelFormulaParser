import re
import openpyxl

class CellReference:
    def __init__(self, cell_ref):
        self.cell_ref = cell_ref
        self.sheet_name = None  # Add sheet_name attribute
        self.parse_cell_ref(self.cell_ref)

    def parse_cell_ref(self, cell_ref):
        # Updated pattern to include optional sheet name
        pattern = r"(?:'([^']+)'!)?([A-Z]+)(\d+)"
        match = re.match(pattern, cell_ref)
        if not match:
            raise ValueError(f"Invalid cell reference: {cell_ref}")

        self.sheet_name, self.column_letter, row_number = match.groups()
        self.row_number = int(row_number)

    @property
    def column_number(self):
        return openpyxl.utils.column_index_from_string(self.column_letter)

    def update_column_letter(self, new_letter):
        self.column_letter = new_letter

    def update_row_number(self, new_number):
        self.row_number = int(new_number)

    def __str__(self):
        if self.sheet_name:
            return f"'{self.sheet_name}'!{self.column_letter}{self.row_number}"
        return f"{self.column_letter}{self.row_number}"