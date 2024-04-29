import Models


class Types:

    type_map = {
        "constant": Models.Constant,
        "reference": Models.Reference,
        "range": Models.Range,
        "function": Models.Function,
        "expression": Models.Expression,
        "formula": Models.Formula
    }
    composite_types = [item for item in type_map.keys() if item not in ['constant', 'reference']]
    def __init__(self, type_str='') -> None:
        if type_str:
            self.type_str = type_str
    
    def get_type(self):
        if not self.type_str:
            raise ValueError("Type string not provided")
        
        type_value = Types.type_map.get(self.type_str, None)
        if not type_value:
            raise ValueError(f"Invalid type: {self.type_str}")
        
        return type_value
