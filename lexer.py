import Tokens
from Tokens import token

NUM_CHARS = "0123456789"
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_"
OPERATORS = "+-*/%()^,"
CHAR_TYPES = {"+": Tokens.PLUS_SIGN, "-": Tokens.MINUS_SIGN, "*": Tokens.MULT_SIGN, "/": Tokens.DIV_SIGN,
              "%": Tokens.MODULUS_SIGN, "=": Tokens.EQUALS, "(": Tokens.LPAREN, ")": Tokens.RPAREN, "^": Tokens.EXP,
              "=>": Tokens.FUNCTION_OPERATOR, ",": Tokens.COMMA, ".": Tokens.PERIOD_FUNC_CALL}
KEYWORDS = ["sqrt", "sin", "cos", "tan", "factorial"]
FN_KEYWORD = "fn"


# TODO: consider replacing confusing ifs with regex


class Lexer:
    def __init__(self, text):
        self.text = iter(text)
        self.current_char = None
        self.next_char()

    def next_char(self):
        try:
            self.current_char = next(self.text)
        except StopIteration:
            self.current_char = None

    def gen_tokens(self):
        tokens = []

        while self.current_char is not None:
            if self.current_char == " ":
                self.next_char()
            elif self.current_char in NUM_CHARS:
                tokens.append(self.gen_number())
            elif self.current_char in OPERATORS:
                tokens.append(token(CHAR_TYPES.get(self.current_char)))
                self.next_char()
            elif self.current_char == "=":
                self.next_char()
                if self.current_char == ">":
                    tokens.append(token(CHAR_TYPES.get("=>")))
                    self.next_char()
                else:
                    tokens.append(token(CHAR_TYPES.get("=")))
            elif self.current_char in LETTERS:
                tokens.append(self.gen_identifier())
                if self.current_char == ".":
                    tokens.append(token(CHAR_TYPES.get(".")))
                    self.next_char()
            else:
                raise Exception(f"Illegal Character {self.current_char}")
        self.token_validation(tokens)
        return tokens


    def gen_number(self):
        number = ""
        while self.current_char is not None and self.current_char in (NUM_CHARS + "."):
            number += self.current_char
            self.next_char()
        if number.startswith("."):
            number = "0" + number
        if number.count(".") > 1:
            raise Exception("Illegal number", number)
        return token(Tokens.NUMBER, float(number))

    def gen_identifier(self):
        name = ""
        while self.current_char is not None and self.current_char in (LETTERS + NUM_CHARS):
            name += self.current_char
            self.next_char()
        if name in KEYWORDS:
            if self.current_char == ".":
                self.next_char()
                return token(Tokens.KEYWORD, name)
            elif self.current_char == "(":
                return token(Tokens.KEYWORD, name)
            else:
                raise SyntaxError(f"Wrong use of keyword {name}.")
        elif name == FN_KEYWORD:
            return token(Tokens.FUNCTION_KEYWORD)
        else:
            return token(Tokens.IDENTIFIER, name)

    # placeholder to resolve syntax like 'x = 2a' cutting off after number
    def token_validation(self, tokens):
        for i, token in enumerate(tokens):
            if token.type == Tokens.NUMBER and i < len(tokens) - 1 and tokens[i + 1].type == Tokens.IDENTIFIER:
                raise SyntaxError(
                    f"Invalid syntax. Perhaps there is an operator missing between {token.value} and {tokens[i + 1].value}?")
