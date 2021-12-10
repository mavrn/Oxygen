from collections import namedtuple
import Tokens

AddNode = namedtuple("AddNode", ["a", "b"])
SubNode = namedtuple("SubNode", ["a", "b"])
MultNode = namedtuple("MultNode", ["a", "b"])
DivNode = namedtuple("DivNode", ["a", "b"])
ModulusNode = namedtuple("ModulusNode", ["a", "b"])
ExpNode = namedtuple("ExpNode", ["a", "b"])
AssignNode = namedtuple("AssignNode", ["identifier", "value"])
VariableNode = namedtuple("VariableNode", ["identifier"])
KeywordNode = namedtuple("KeywordNode", ["keyword", "value"])


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
        if self.current_token is None:
            return None
        else:
            return self.expression()

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
        result = self.exponential()
        while self.current_token is not None and self.current_token.type in (Tokens.MULT_SIGN, Tokens.DIV_SIGN, Tokens.MODULUS_SIGN, Tokens.EQUALS):
            if self.current_token.type == Tokens.MULT_SIGN:
                self.next_token()
                result = MultNode(result, self.exponential())
            elif self.current_token.type == Tokens.DIV_SIGN:
                self.next_token()
                result = DivNode(result, self.exponential())
            elif self.current_token.type == Tokens.EQUALS:
                self.next_token()
                try:
                    result = AssignNode(result.identifier, self.expression())
                except AttributeError:
                    raise SyntaxError(f"Couldn't assign to type {type(result).__name__}")
            else:
                self.next_token()
                result = ModulusNode(result, self.exponential())
        return result

    def exponential(self):
        token = self.factor()
        if self.current_token is not None and self.current_token.type == Tokens.EXP:
            self.next_token()
            return ExpNode(token, self.factor())
        else:
            return token

    def factor(self):
        token = self.current_token
        if token is None:
            raise SyntaxError("Invalid syntax")
        if token.type == Tokens.NUMBER:
            self.next_token()
            return token.value
        elif token.type == Tokens.PLUS_SIGN:
            self.next_token()
            return self.exponential()
        elif token.type == Tokens.MINUS_SIGN:
            self.next_token()
            return MultNode(-1, self.exponential())
        elif token.type == Tokens.LPAREN:
            self.next_token()
            result = self.expression()
            if self.current_token is None or self.current_token.type != Tokens.RPAREN:
                raise SyntaxError("Expected a closing parenthesis")
            else:
                self.next_token()
                return result
        elif token.type == Tokens.IDENTIFIER:
            self.next_token()
            return VariableNode(token.value)
        elif token.type == Tokens.KEYWORD:
            keyword = self.current_token.value
            self.next_token()
            return KeywordNode(keyword, self.exponential())
        else:
            raise SyntaxError("Invalid syntax")
