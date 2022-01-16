import Tokens
import Nodes


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
        elif self.current_token.type == Tokens.FUNCTION_KEYWORD:
            self.next_token()
            return self.declare_function()
        else:
            return self.expression()

    def expression(self):
        result = self.term()
        while self.current_token is not None and self.current_token.type in (Tokens.PLUS_SIGN, Tokens.MINUS_SIGN):
            if self.current_token.type == Tokens.PLUS_SIGN:
                self.next_token()
                result = Nodes.AddNode(result, self.term())
            else:
                self.next_token()
                result = Nodes.SubNode(result, self.term())
        return result

    def term(self):
        result = self.exponential()
        while self.current_token is not None and self.current_token.type in (Tokens.MULT_SIGN, Tokens.DIV_SIGN, Tokens.MODULUS_SIGN, Tokens.EQUALS):
            if self.current_token.type == Tokens.MULT_SIGN:
                self.next_token()
                result = Nodes.MultNode(result, self.exponential())
            elif self.current_token.type == Tokens.DIV_SIGN:
                self.next_token()
                result = Nodes.DivNode(result, self.exponential())
            elif self.current_token.type == Tokens.EQUALS:
                self.next_token()
                try:
                    result = Nodes.AssignNode(result.identifier, self.expression())
                except AttributeError:
                    raise SyntaxError(f"Couldn't assign to type {type(result).__name__}")
            else:
                self.next_token()
                result = Nodes.ModulusNode(result, self.exponential())
        return result

    # TODO: consider replacing with keyword
    def exponential(self):
        token = self.factor()
        if self.current_token is not None and self.current_token.type == Tokens.EXP:
            self.next_token()
            return Nodes.ExpNode(token, self.factor())
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
            return Nodes.MultNode(-1, self.exponential())
        elif token.type == Tokens.LPAREN:
            self.next_token()
            result = self.expression()
            if self.current_token is None or self.current_token.type != Tokens.RPAREN:
                raise SyntaxError("Expected a closing parenthesis")
            else:
                self.next_token()
                return result
        elif token.type == Tokens.IDENTIFIER:
            identifier = token.value
            self.next_token()
            if self.current_token is None or self.current_token.type not in (Tokens.LPAREN, Tokens.PERIOD_FUNC_CALL):
                return Nodes.VariableNode(token.value)
            else:
                return self.call_function(identifier)

        elif token.type == Tokens.KEYWORD:
            keyword = self.current_token.value
            self.next_token()
            return Nodes.KeywordNode(keyword, self.exponential())
        else:
            raise SyntaxError("Invalid syntax")

    # TODO: do some more testing with functions
    def declare_function(self):
        arguments = []
        if self.current_token.type != Tokens.IDENTIFIER:
            raise SyntaxError("Expected an identifier")
        else:
            identifier = self.current_token.value
            self.next_token()
        while self.current_token.type == Tokens.IDENTIFIER:
            arguments.append(self.current_token.value)
            self.next_token()
        if self.current_token.type != Tokens.FUNCTION_OPERATOR:
            raise SyntaxError("Expected \"=>\"")
        else:
            self.next_token()
            return Nodes.FuncDeclareNode(identifier, arguments, self.expression())

    def call_function(self, identifier):
        arguments = []
        if self.current_token.type == Tokens.LPAREN:
            self.next_token()
            while self.current_token is not None and self.current_token.type in (
            Tokens.IDENTIFIER, Tokens.COMMA, Tokens.NUMBER):
                arguments.append(self.expression())
                if self.current_token.type not in (Tokens.COMMA, Tokens.RPAREN):
                    raise SyntaxError("Expected comma or closing parenthesis")
                elif self.current_token.type != Tokens.RPAREN:
                    self.next_token()
            if self.current_token.type != Tokens.RPAREN:
                raise SyntaxError("Expected closing parenthesis")
            self.next_token()
            return Nodes.FuncCallNode(identifier, arguments)
        elif self.current_token.type == Tokens.PERIOD_FUNC_CALL:
            self.next_token()
            arguments.append(self.expression())
            return Nodes.FuncCallNode(identifier, arguments)
        else:
            raise SyntaxError("An unknown error occurred")
