class Bool:
    def __init__(self, value: bool = None):
        if isinstance(value, bool):
            self.boolean_value = value
        elif isinstance(value, Bool):
            self.boolean_value = value.boolean_value
        elif value is None:
            self.boolean_value = False
        elif value == 0:
            self.boolean_value = False
        elif value > 0 or value < 0:
            self.boolean_value = True
        else:
            raise TypeError(f"Type {type(value).__name__} could not be converted to bool.")

    def __repr__(self):
        if self.boolean_value is False:
            return "False"
        if self.boolean_value is True:
            return "True"

    def reverse(self):
        self.boolean_value = not self.boolean_value
