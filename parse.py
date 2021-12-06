from collections import namedtuple

NumNode = int()
AddNode = namedtuple("AddNode", ["n1", "n2"])
SubNode = namedtuple("AddNode", ["n1", "n2"])
MultNode = namedtuple("MultNode", ["n1", "n2"])
DivNode = namedtuple("DivNode", ["n1", "n2"])


class Parser:
    def __init__(self, tokens):
        self.tokens = iter(tokens)
        self.current_token = None
        self.next_token()

    def next_token(self):
        try:
            self.current_token = next(self.tokens)
        except StopIteration:
            self.current_token = None

    def parse(self):
        return self.expression()

    def expression(self):
        result = self.term()
        while self.current_token is not None and self.current_token.type in (1, 2):
            self.next_token()
            result = ExprNode(result, self.term())
        return result

    def term(self):
        result = self.factor()
        while self.current_token is not None and self.current_token.type in (3, 4):
            self.next_token()
            result = TermNode(result, self.factor())
        return result

    def factor(self):
        token = self.current_token
        if token.type == 0:
            self.next_token()
            return token.value
        else:
            raise Exception("Syntax error")
