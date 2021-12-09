from collections import namedtuple
from lexer import OPERATORS

AddNode = namedtuple("AddNode", ["a", "b"])
SubNode = namedtuple("SubNode", ["a", "b"])
MultNode = namedtuple("MultNode", ["a", "b"])
DivNode = namedtuple("DivNode", ["a", "b"])
AssignNode = namedtuple("AssignNode", ["identifier", "value"])
VariableNode = namedtuple("VariableNode", ["identifier"])


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
        if self.current_token.type == 7:
            return self.gen_assign_node()
        else:
            return self.expression()

    def gen_assign_node(self):
        identifier = self.current_token.value
        self.next_token()
        if self.current_token is None:
            return VariableNode(identifier)
        elif self.current_token.type == 1:
            self.next_token()
            return AddNode(VariableNode(identifier), self.expression())
        elif self.current_token.type == 2:
            self.next_token()
            return SubNode(VariableNode(identifier), self.expression())
        elif self.current_token.type == 3:
            self.next_token()
            return MultNode(VariableNode(identifier), self.expression())
        elif self.current_token.type == 4:
            self.next_token()
            return DivNode(VariableNode(identifier), self.expression())
        elif self.current_token.type == 8:
            self.next_token()
            return AssignNode(identifier, self.expression())
        else:
            raise Exception("Syntax Error")

    def expression(self):
        result = self.term()
        while self.current_token is not None and self.current_token.type in (1, 2):
            if self.current_token.type == 1:
                self.next_token()
                result = AddNode(result, self.term())
            else:
                self.next_token()
                result = SubNode(result, self.term())
        return result

    def term(self):
        result = self.factor()
        while self.current_token is not None and self.current_token.type in (3, 4):
            if self.current_token.type == 3:
                self.next_token()
                result = MultNode(result, self.factor())
            else:
                self.next_token()
                result = DivNode(result, self.factor())
        return result

    def factor(self):
        token = self.current_token
        if token.type == 0:
            self.next_token()
            return token.value
        elif token.type == 2:
            self.next_token()
            return MultNode(-1, self.factor())
        elif token.type == 5:
            self.next_token()
            result = self.expression()
            if self.current_token.type != 6:
                raise Exception("SyntaxError")
            else:
                self.next_token()
                return result
        elif token.type == 7:
            self.next_token()
            return VariableNode(token.value)
        else:
            raise Exception("Syntax error")
