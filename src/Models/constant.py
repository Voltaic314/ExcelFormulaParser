

class Constant:

    @staticmethod
    def is_valid_constant(arg):
        # Check if the arg is a digit, possibly a float or an integer
        if not str(arg).isdigit() or not str(arg).isnumeric():
            return False
        return True

    def __init__(self, value):
        self.value = value

    def __init__(self, value):
        # Automatically parse and set value during initialization
        self.value = self.parse_constant(value)

    @staticmethod
    def parse_constant(constant_str):
        constant_str = str(constant_str).replace("'", "").replace('"', "").strip()
        
        # Try to convert to float or int
        try:
            if '.' in constant_str:
                return float(constant_str) 
            return int(constant_str)  
        
        except ValueError:
            raise ValueError("Invalid constant format")

    def __str__(self):
        return str(self.value)
    
    def to_dict(self):
        return {"constant": self.value}