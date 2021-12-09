from collections import namedtuple
import Tokens

AddNode = namedtuple("AddNode", ["a", "b"])
SubNode = namedtuple("SubNode", ["a", "b"])
MultNode = namedtuple("MultNode", ["a", "b"])
DivNode = namedtuple("DivNode", ["a", "b"])
ModulusNode = namedtuple("ModulusNode", ["a", "b"])
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
        if self.current_token.type == Tokens.IDENTIFIER:
            return self.gen_assign_node()
        else:
            return self.expression()

    def gen_assign_node(self):
        identifier = self.current_token.value
        self.next_token()
        if self.current_token is None:
            return VariableNode(identifier)
        elif self.current_token.type == Tokens.PLUS_SIGN:
            self.next_token()
            return AddNode(VariableNode(identifier), self.expression())
        elif self.current_token.type == Tokens.MINUS_SIGN:
            self.next_token()
            return SubNode(VariableNode(identifier), self.expression())
        elif self.current_token.type == Tokens.MULT_SIGN:
            self.next_token()
            return MultNode(VariableNode(identifier), self.expression())
        elif self.current_token.type == Tokens.DIV_SIGN:
            self.next_token()
            return DivNode(VariableNode(identifier), self.expression())
        elif self.current_token.type == Tokens.MODULUS_SIGN:
            self.next_token()
            return ModulusNode(VariableNode(identifier), self.expression())
        elif self.current_token.type == Tokens.EQUALS:
            self.next_token()
            return AssignNode(identifier, self.expression())
        else:
            raise Exception("Syntax Error")

    def expression(self):
        result = self.term()
        while self.current_token is not None and self.current_token.type in (Tokens.PLUS_SIGN, Tokens.MINUS_SIGN):
            if self.current_token.type == Tokens.PLUS_SIGN:
                self.next_token()
                result = AddNode(result, self.term())
            else:
                self.next_token()
                result = SubNode(result, self.term())
        return result

    def term(self):
        result = self.factor()
        while self.current_token is not None and self.current_token.type in (Tokens.MULT_SIGN, Tokens.DIV_SIGN, Tokens.MODULUS_SIGN):
            if self.current_token.type == Tokens.MULT_SIGN:
                self.next_token()
                result = MultNode(result, self.factor())
            elif self.current_token.type == Tokens.DIV_SIGN:
                self.next_token()
                result = DivNode(result, self.factor())
            else:
                self.next_token()
                result = ModulusNode(result, self.factor())
        return result

    def factor(self):
        token = self.current_token
        if token.type == Tokens.NUMBER:
            self.next_token()
            return token.value
        elif token.type == Tokens.PLUS_SIGN:
            self.next_token()
            return self.factor()
        elif token.type == Tokens.MINUS_SIGN:
            self.next_token()
            return MultNode(-1, self.factor())
        elif token.type == Tokens.LPAREN:
            self.next_token()
            result = self.expression()
            if self.current_token.type != Tokens.RPAREN:
                raise Exception("SyntaxError")
            else:
                self.next_token()
                return result
        elif token.type == Tokens.IDENTIFIER:
            self.next_token()
            return VariableNode(token.value)
        else:
            raise Exception("Syntax error")
