

class Constant:

    @staticmethod
    def is_valid_constant(arg):
        # Check if the arg is a digit, possibly a float or an integer
        if not str(arg).isdigit() or not str(arg).isnumeric():
            raise ValueError("Invalid constant format")
        return True

    def __init__(self, value):
        self.value = value

    def parse_constant(self, constant_str):
        if not isinstance(constant_str, str):
            try:
                constant_str = str(constant_str)
            except ValueError:
                raise ValueError("Invalid constant format")
            
        constant_str = constant_str.replace("'", "").replace('"', "")

        # If it's a valid number, return it as float or int
        try:
            if '.' in constant_str:
                return float(constant_str)  # Return as float
            else:
                return int(constant_str)  # Return as int

        except ValueError:
            raise ValueError("Invalid constant format") # uno reversal lol
    
    def __str__(self):
        return str(self.value)
    
    def to_dict(self):
        return {"constant": self.value}