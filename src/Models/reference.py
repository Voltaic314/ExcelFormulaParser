import re
from openpyxl.utils import column_index_from_string, get_column_letter

class Reference:
    pattern = r"(?:'([^']+)'!)?([A-Z]+)(\d+)$"
    
    @staticmethod
    def from_dict(ref_dict):
        """Reconstruct the reference string from its dictionary representation."""
        column_letter = ref_dict['components']['column_letter']
        row_number = ref_dict['components']['row_number']
        sheet_name = ref_dict['components'].get('sheet_name', None)
        # return an instance of the Reference class using the parsed components
        if sheet_name:
            return Reference(f"'{sheet_name}'!{column_letter}{row_number}")
        return Reference(f"{column_letter}{row_number}")
    
    @staticmethod
    def is_valid_reference(cell_ref):
        """Check if the provided cell reference is valid."""
        if not cell_ref:
            return False
        
        row_number = None
        column_letter = None
        column_number = None

        ref_is_dict = isinstance(cell_ref, dict)
        ref_is_str = isinstance(cell_ref, str)
        if ref_is_str:
            match = re.match(Reference.pattern, cell_ref)
            if not match:
                return False
            _, column_letter, row_number = match.groups()
            row_number = int(row_number)
            if not row_number:
                return False
            # if there isn't at least a column letter or column number, then return false
            if not (column_letter or column_number):
                return False

        elif ref_is_dict:
            if not 'components' in cell_ref:
                return False
            
            components = cell_ref['components']
            if not 'row_number' in components or (not 'column_letter' in components or not 'column_number' in components):
                return False

            column_letter = components.get('column_letter', None)
            column_number = components.get('column_number', None)
            row_number = components['row_number']

        if not column_number:
            column_number = column_index_from_string(column_letter)

        # breaking conditions - types
        if not isinstance(row_number, int) or not isinstance(column_number, int) or not isinstance(column_letter, str):
            return False

        # breaking conditions - values
        if column_number < 0 or row_number < 0 or not column_letter.isalpha():
            return False
        
        return True

    def __init__(self, cell_ref):
        """Initialize the CellReference instance by parsing the provided reference."""
        valid = Reference.is_valid_reference(cell_ref)
        if not valid:
            raise ValueError(f"Invalid cell reference: {cell_ref}")
        self.parse_cell_ref(cell_ref)

    def parse_cell_ref(self, cell_ref):
        """Parse the cell reference string and set the object attributes."""
        match = re.match(Reference.pattern, cell_ref)
        
        self.sheet_name, self.column_letter, row_number = match.groups()
        self.row_number = int(row_number)

    def to_dict(self):
        """Create a dictionary representation of the cell reference."""
        return {
            "reference": str(self), 
            "components": {
                "sheet_name": self.sheet_name,
                "column_letter": self.column_letter,
                "row_number": self.row_number,
                "column_number": self.column_number
            }
        }

    @property
    def column_number(self):
        return self._column_number

    @column_number.setter
    def column_number(self, value):
        if not isinstance(value, int) or value < 1:
            raise ValueError("Invalid column number")
        self._column_number = value
        self._column_letter = get_column_letter(value)

    @property
    def column_letter(self):
        return self._column_letter

    @column_letter.setter
    def column_letter(self, value):
        if not isinstance(value, str) or not value.isalpha():
            raise ValueError("Invalid column letter")
        self._column_letter = value
        self._column_number = column_index_from_string(value)

    def update_column_letter(self, new_letter):
        self.column_letter = new_letter

    def update_column_number(self, new_number):
        self.column_number = new_number

    def update_row_number(self, new_number):
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
            cell = Reference(ref)
            print(f"Successfully created cell reference: {cell}")
        except ValueError as e:
            print(f"Error creating cell reference {ref}: {e}")
            failures += 1

    if failures == len(invalid_refs):
        print("All invalid references failed, as expected.")
