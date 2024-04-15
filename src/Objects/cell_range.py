from .cell_reference import CellReference
import re


class CellRange:
    pattern = r"([A-Z]+\d+):([A-Z]+\d+)"  # Class attribute for the regex pattern

    def is_valid_range(range_str):
        return bool(re.match(CellRange.pattern, range_str)) or isinstance(range_str, CellRange)

    def __init__(self, start_ref, end_ref=None):
        if end_ref is None:
            self.start_cell, self.end_cell = self.parse_range(start_ref)
        else:
            self.start_cell = CellReference(start_ref)
            self.end_cell = CellReference(end_ref)

    def parse_range(self, range_str):
        match = re.match(CellRange.pattern, range_str)
        if not match:
            raise ValueError(f"Invalid range format: {range_str}")
        start_ref, end_ref = match.groups()
        return CellReference(start_ref), CellReference(end_ref)

    def __str__(self):
        return f"{self.start_cell}:{self.end_cell}"