from importlib import import_module


class Types:

    def __init__(self, type_str='') -> None:
        self.type_str = type_str
        self.module_name = 'Models'  # Assuming all model classes are in the 'Models' package

    def get_type(self):
        
        if not self.type_str:
            raise ValueError("Type string not provided")

        try:
            # Dynamically import the module and access the class
            module = import_module(f".{self.type_str.lower()}", package=self.module_name)
            type_class = getattr(module, self.type_str.capitalize())
            return type_class
        except (ImportError, AttributeError) as e:
            raise ImportError(f"Could not load type {self.type_str}: {str(e)}")


if __name__ == "__main__":
    # Example usage
    type_str = 'Reference'
    type_class = Types(type_str).get_type()
    type_instance = type_class('A1')
    print(type_instance)
    print(type_class.is_valid_reference('A1'))