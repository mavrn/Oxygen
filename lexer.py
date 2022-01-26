import Tokens
from Tokens import token

NUM_CHARS = "0123456789"
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_"
OPERATORS = "+-*/%()^,"
OPERATOR_DICT = {"+": Tokens.PLUS_SIGN, "-": Tokens.MINUS_SIGN, "*": Tokens.MULT_SIGN, "/": Tokens.DIV_SIGN,
                 "%": Tokens.MODULUS_SIGN, "+=": Tokens.PLUS_ASSIGN, "-=": Tokens.MINUS_ASSIGN,
                 "*=": Tokens.MULT_ASSIGN, "/=": Tokens.DIV_ASSIGN, "%=": Tokens.MODULUS_ASSIGN,
                 "(": Tokens.LPAREN, ")": Tokens.RPAREN, "^": Tokens.EXP, ",": Tokens.COMMA}
FN_KEYWORD = "fn"


# TODO: replace this with a regex lexer


# Is responsible for generating a list of tokens based on a string input using the pre-defined Tokens
# from the Tokens.py file.
class Lexer:
    # Defines an iterator based on the string input
    def __init__(self, text):
        self.text = iter(text)
        self.current_char = None
        self.next_char()

    # Advances the iterator to the next character, returns None at the end of the text
    def next_char(self):
        try:
            self.current_char = next(self.text)
        except StopIteration:
            self.current_char = None

    # Generates a list of tokens
    def gen_tokens(self):
        tokens = []
        while self.current_char is not None:
            if self.current_char == " ":
                self.next_char()
            elif self.current_char in OPERATORS:
                operator = self.current_char
                self.next_char()
                # Checks for an equals after an operator to determine if the token should be of assign type
                if operator in "+-*/%" and self.current_char == "=":
                    tokens.append(token(OPERATOR_DICT.get(operator + "=")))
                    self.next_char()
                else:
                    tokens.append(token(OPERATOR_DICT.get(operator)))
            elif self.current_char == "=":
                self.next_char()
                # We have to differentiate between a simple equals and the function operator "=>", so we check for a ">"
                if self.current_char == ">":
                    tokens.append(token(Tokens.FUNCTION_OPERATOR))
                    self.next_char()
                else:
                    tokens.append(token(Tokens.EQUALS))
            elif self.current_char in (NUM_CHARS + "."):
                tokens.append(self.gen_number())
            elif self.current_char in LETTERS:
                tokens.append(self.gen_identifier())
                # Will recognize when a function is called with a period after the identifier
                if self.current_char == ".":
                    tokens.append(token(Tokens.PERIOD_FUNC_CALL))
                    self.next_char()
            else:
                raise Exception(f"Illegal Character {self.current_char}")
        return tokens

    # Will generate and return a number with multiple or one digit(s)
    def gen_number(self):
        number = ""
        while self.current_char is not None and self.current_char in (NUM_CHARS + "."):
            number += self.current_char
            self.next_char()
        # Will change ie. ".5" to "0.5"
        if number.startswith("."):
            number = "0" + number
        # A number with multiple periods will raise an exception
        if number.count(".") > 1:
            raise Exception("Illegal number", number)
        return token(Tokens.NUMBER, float(number))

    # Will generate and return an identifier with multiple or one letter(s)
    def gen_identifier(self):
        name = ""
        while self.current_char is not None and self.current_char in (LETTERS + NUM_CHARS):
            name += self.current_char
            self.next_char()
        if name == FN_KEYWORD:
            return token(Tokens.FUNCTION_KEYWORD)
        else:
            return token(Tokens.IDENTIFIER, name)
