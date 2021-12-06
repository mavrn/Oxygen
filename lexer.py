from collections import namedtuple

token = namedtuple("token", "type value", defaults=(None, None))
NUM_CHARS = ".0123456789"
OPERATORS = "+-*/()"
CHAR_TYPES = {"NUM": 0, "+": 1, "-": 2, "*": 3, "/": 4, "(": 5, ")": 6}


class Lexer:
    current_char = ""

    def __init__(self, text):
        self.text = iter(text)

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
            else:
                raise Exception(f"Illegal Character {self.current_char}")
        return tokens

    def gen_number(self):
        number = ""
        while self.current_char is not None and self.current_char in NUM_CHARS:
            number += self.current_char
            self.next_char()

        if number.startswith("."):
            number = "0" + number
        if number.count(".") > 1:
            raise Exception("Illegal number", number)
        return token(CHAR_TYPES.get("NUM"), float(number))
