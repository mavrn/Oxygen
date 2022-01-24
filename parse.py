import Tokens
import Nodes


# Is responsible for recursively generating a tree of operations based on the lexer output using the pre-defined Nodes
# from the Nodes.py file.
class Parser:
    # defines an iterator based on the list of Tokens
    def __init__(self, tokens):
        self.tokens = iter(tokens)
        self.current_token = None
        self.next_token()

    # advances the iterator to the next token, returns None at the end of the list
    def next_token(self):
        try:
            self.current_token = next(self.tokens)
        except StopIteration:
            self.current_token = None

    # will start and end the parsing process
    def parse(self):
        # if there are no tokens, None will be returned
        if self.current_token is None:
            tree = None
        # if the first token is the FUNCTION_KEYWORD, the parsing process will begin at the declare_function function
        elif self.current_token.type == Tokens.FUNCTION_KEYWORD:
            self.next_token()
            tree = self.declare_function()
        else:
            tree = self.expression()
        # if the parsing process is finished and there are still tokens left, the syntax is invalid:
        # an example would be x = 2a
        if self.current_token is not None:
            raise SyntaxError("Invalid Syntax.")
        else:
            return tree

    # following, there are the valid elements of an expression, following the common order top-down.
    # an expression will have a plus or minus sign
    # a term will have a multiplication, division, assignment(equals) or a modulus sign
    # an "exponential" will have the exponentiation operator. the reason this has its own layer is that exponential
    # operations will have to be evaluated before a term, but after a factor.
    # finally, the factor can be a number, identifier or an expression between brackets.
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
        while self.current_token is not None and self.current_token.type in (
                Tokens.MULT_SIGN, Tokens.DIV_SIGN, Tokens.MODULUS_SIGN, Tokens.EQUALS):
            if self.current_token.type == Tokens.MULT_SIGN:
                self.next_token()
                result = Nodes.MultNode(result, self.exponential())
            elif self.current_token.type == Tokens.DIV_SIGN:
                self.next_token()
                result = Nodes.DivNode(result, self.exponential())
            elif self.current_token.type == Tokens.EQUALS:
                # will throw an exception if an equals comes after anything other than a variable
                if type(result).__name__ == "VariableNode":
                    self.next_token()
                    result = Nodes.AssignNode(result.identifier, self.expression())
                else:
                    raise SyntaxError(f"Couldn't assign to type {type(result).__name__}")
            else:
                self.next_token()
                result = Nodes.ModulusNode(result, self.exponential())
        return result

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
            raise SyntaxError("Expected number or identifier")
        # will return the float value for a number token
        if token.type == Tokens.NUMBER:
            self.next_token()
            return token.value
        # will handle unary plus und minus signs
        elif token.type == Tokens.PLUS_SIGN:
            self.next_token()
            return self.exponential()
        elif token.type == Tokens.MINUS_SIGN:
            self.next_token()
            return Nodes.MultNode(-1, self.exponential())
        # will handle parentheses and throw an exception in case of a missing parenthesis
        elif token.type == Tokens.LPAREN:
            self.next_token()
            result = self.expression()
            if self.current_token is None or self.current_token.type != Tokens.RPAREN:
                raise SyntaxError("Expected a closing parenthesis")
            else:
                self.next_token()
                return result
        # will return either a variable node or a function call node if brackets or a period come after the identifier
        elif token.type == Tokens.IDENTIFIER:
            identifier = token.value
            self.next_token()
            if self.current_token is None or self.current_token.type not in (Tokens.LPAREN, Tokens.PERIOD_FUNC_CALL):
                return Nodes.VariableNode(token.value)
            else:
                return self.call_function(identifier)
        else:
            raise SyntaxError("Invalid syntax")

    # TODO: do some more testing with functions
    # will follow the pre-defined syntax of a function declaration linearly
    # and will throw exceptions if the syntax is incorrect
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
            return Nodes.FuncDeclareNode(identifier=identifier, arguments=arguments, body=self.expression())

    # will follow the pre-defined syntax of a function call linearly
    # and will throw exceptions if the syntax is incorrect
    def call_function(self, identifier):
        arguments = []
        # will handle a function call by brackets
        if self.current_token.type == Tokens.LPAREN:
            self.next_token()
            while self.current_token is not None and self.current_token.type in (
                    Tokens.IDENTIFIER, Tokens.COMMA, Tokens.NUMBER
            ):
                arguments.append(self.expression())
                if self.current_token.type == Tokens.COMMA:
                    self.next_token()
                elif self.current_token.type != Tokens.RPAREN:
                    raise SyntaxError("Expected comma or closing parenthesis")
            if self.current_token.type != Tokens.RPAREN:
                raise SyntaxError("Expected closing parenthesis")
            self.next_token()
            return Nodes.FuncCallNode(identifier=identifier, arguments=arguments)
        # will handle a function call by period
        elif self.current_token.type == Tokens.PERIOD_FUNC_CALL:
            self.next_token()
            arguments.append(self.expression())
            return Nodes.FuncCallNode(identifier=identifier, arguments=arguments)
        # the program should never reach this point
        else:
            raise SyntaxError("An unknown error occurred")
