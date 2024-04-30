# ExcelFormulaParser

## Description

ExcelFormulaParser extends openpyxl to enhance formula parsing capabilities in Excel spreadsheets. While openpyxl handles spreadsheet management well, its formula parsing features are limited. This project aims to build a robust structure for mapping and manipulating Excel formulas through a comprehensive, user-friendly data structure.
Features

     - Formula Parsing: Decompose formulas into a structured format, making them easy to manipulate and analyze.

     - Formula Manipulation: Implement methods like formula.translate() to adjust formulas based on cell repositioning.

     - Analytics: Analyze formulas to extract components count, such as the number of functions used.

## Okay... but why? 
Strings are inherently chaotic. They give us all the info we need 
about a formula at the surface level but not much beyond that. If you 
need to systematically modify a formula in a way that's not easy to 
program in rules for, this will help a ton. I presume for most people 
this library will be overkill for their spreadsheet modification needs.
But I still think it's better to have a robust overkill solution to a 
problem than having to spend 3 hours writing complex regex string 
matching, grouping, and substitution algorithms to do this instead of 
just treating the formula like a dictionary and iterating through a dictionary. 

This also allows for easier transmission, encoding and decoding, of 
these formulas via APIs (god forbid you'd need to do that), and not to
mention allows you to store these structures to files as json files. 
As well as adding any other metadata fields you need to the structure 
before it gets saved. So I'm imagining a lot of benefits here. 

## Progress and Contributions

The project is in active development, aiming for significant functionality completion by end of May 2024. Contributions are welcome! If you'd like to help:

    Fork the repository and create a pull request with your additions.
    Ensure your code is accompanied by updated or new tests that validate your changes.

### Current Work

    - Developing features to provide analytical insights into formula components.
    - Need to work on implementing absolute cell reference support into our structure. Shouldn't be too hard but will take time as everything relies on this class. 


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
f_str = str(f)  # reconstructs back into an excel friendly string

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

### Translating formulas
```python
import ExcelFormulaParser as efp

# Initialize with a formula
f = efp.Formula("=SUM(A1, A2)")
f.translate(input_cell="A1", output_cell="C3")
str(f) # would now return: "=SUM(C3, C4)"

# so essentially translating is just taking every cell reference in 
# the formula and calculating the offset in rows and columns from the 
# input and output cell shift amounts, then applying that to every cell reference.

# I plan to add more functionality to this, but for now this is just a blanket translation to all cel refs.
```

### Iterating through cell ranges
```python
# you can already iterate through a function's arguments since function_instance.args is a list
# and same goes for expression components. 
# but to iterate through a range of cells or check if a cell ref string would be inside a bigger range, you can do this syntax: 
import ExcelFormulaParser as efp

# Instantiate a Range object
cell_range = efp.Range("A1:B2")

# Check if a cell reference is within the range
print("B1" in cell_range)  # Outputs: True
print("B3" in cell_range)  # Outputs: False

# Iterate through all cells in the range
for cell in cell_range:
    print(cell)  # Outputs: 'A1', 'B1', 'A2', 'B2'

# You can also iterate row-wise if needed:
for row in cell_range.get_cells_in_range():
    for cell in row:
        print(cell)  # Each cell within each row of the range is printed
```

## Project Structure

Explore the src/Models directory for class details and src/Tests for unit tests corresponding to each class. The primary interface is through the Formula class, which serves as a facade for the underlying Parser class handling the detailed parsing logic.
