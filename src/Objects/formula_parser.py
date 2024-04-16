import re
from Objects.expression import Expression
from Objects.excel_function import ExcelFunction
from Objects.constant import Constant
from Objects.cell_reference import CellReference

class FormulaParser:
    def __init__(self, formula: str):
        self.formula = formula
        self.function_pattern = re.compile(ExcelFunction.pattern)

    def classify_component(self, component):
        if Expression.is_valid_expression(component):
            return {"type": "expression", "value": component}
        elif ExcelFunction.is_function_string(component):
            return {"type": "function", "value": component}
        elif Constant.is_valid_constant(component):
            return {"type": "constant", "value": component}
        elif CellReference.is_valid_reference(component):
            return {"type": "reference", "value": component}
        else:
            return {"type": "unknown", "value": component}

    def parse_formula(self):
        expression = Expression(self.formula)
        components = expression.components
        classified_components = {i: self.classify_component(comp) for i, comp in enumerate(components)}
        return classified_components

# Example usage of the FormulaParser class
if __name__ == "__main__":
    formula = "=A1 + 5"
    formula_parser = FormulaParser(formula)
    parsed_output = formula_parser.parse_expression(formula)
    print(parsed_output)  # Should show components like ['A1', '+', '5']
