class Bool:
    def __init__(self, var: bool = None):
        if var is None:
            self.var = None
        elif var is False:
            self.var = False
        elif var is True:
            self.var = True
        else:
            raise Exception("An unknown exception occured")

    def __repr__(self):
        if self.var is False:
            return "False"
        if self.var is True:
            return "True"
