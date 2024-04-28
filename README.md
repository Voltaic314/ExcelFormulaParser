# ExcelFormulaParser

## Description

ExcelFormulaParser extends openpyxl to enhance formula parsing capabilities in Excel spreadsheets. While openpyxl handles spreadsheet management well, its formula parsing features are limited. This project aims to build a robust structure for mapping and manipulating Excel formulas through a comprehensive, user-friendly data structure.
Features

     - Formula Parsing: Decompose formulas into a structured format, making them easy to manipulate and analyze.

     - Formula Manipulation: Implement methods like formula.translate() to adjust formulas based on cell repositioning.

     - Analytics: Analyze formulas to extract components count, such as the number of functions used.

## Progress and Contributions

The project is in active development, aiming for significant functionality completion by May 2024. Contributions are welcome! If you'd like to help:

    Fork the repository and create a pull request with your additions.
    Ensure your code is accompanied by updated or new tests that validate your changes.

### Current Work

    Enhancing the formula.translate() method to shift references based on specified start and end cells.
    Developing features to provide analytical insights into formula components.


## installation 
```python
pip install ExcelFormulaParser
```

## Usage

To use ExcelFormulaParser, start by importing the module and initializing a Formula object with an Excel formula string. Here’s how you can parse a formula and manipulate it:

```python

import ExcelFormulaParser as efp

# Initialize with a formula
f = efp.Formula("=SUM(A1, A2)")

# Access the parsed formula
parsed_formula = f.parsed_formula

# To reflect changes back to a formula string after modifications:
f_str = str(f)  # Outputs the original or modified formula string

# dictionary structure of this formula: 
# {
#     "function': '=SUM(A1, A2)
#     "components": {
#         "name": "SUM"
#         "arguments": [
#             {"reference": "A1"
#              "components": {
#                  "sheet_name": None,
#                  "column_letter": "A",
#                  "column_number": 1,
#                  "row_number": 1}},
#
#             {"reference": "A2"
#              "components": {
#                  "sheet_name": None,
#                  "column_letter": "A",
#                  "column_number": 1,
#                  "row_number": 2}},
#          ]
#     }
# }
```

## Structure

Explore the src/Models directory for class details and src/Tests for unit tests corresponding to each class. The primary interface is through the Formula class, which serves as a facade for the underlying Parser class handling the detailed parsing logic.
