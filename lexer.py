import Datatypes
from Datatypes import Token, OXYGEN_DICT, OXYGEN_SET
from collections import deque


class Lexer:
    def __init__(self, text):
        self.text = deque(text)
        self.current_char = None
        self.ignore = False
        self.next_char()

    def next_char(self):
        try:
            self.current_char = self.text.popleft()
        except IndexError:
            self.current_char = None

    def gen_tokens(self):
        tokens = deque()
        while self.current_char is not None:
            current_char = self.current_char
            if current_char in ";\n":
                self.ignore = False
                tokens.append(Token(Datatypes.LINEBREAK))
                self.next_char()
            elif current_char in [" ", "\t"] or self.ignore:
                self.next_char()
            elif current_char == "~":
                tokens.append(Token(Datatypes.LINEBREAK))
                self.next_char()
                self.ignore = True
            elif current_char in OXYGEN_SET:
                operator = ""
                while self.current_char is not None and operator+self.current_char in OXYGEN_SET:
                    operator += self.current_char
                    self.next_char()
                tokens.append(Token(OXYGEN_DICT.get(operator)))
            elif current_char in Datatypes.NUM_CHARS:
                num_tokens = self.gen_number()
                for token in num_tokens:
                    tokens.append(token)
            elif current_char in Datatypes.LETTERS:
                tokens.append(self.gen_identifier())
            elif current_char in ("\"", "\'"):
                tokens.append(self.gen_string())
            else:
                raise SyntaxError(f"Unexpected character {current_char}")
        return tokens

    def gen_number(self):
        number = ""
        period_count = 0
        while self.current_char is not None and self.current_char in (Datatypes.NUM_CHARS.union(".")):
            if self.current_char == ".":
                period_count += 1
            else:
                period_count = 0
            if period_count == 2:
                self.next_char()
                return [Token(Datatypes.NUMBER, Datatypes.Number(number[:-1])), Token(Datatypes.DOUBLE_PERIOD)]
            number += self.current_char
            self.next_char()
        if self.current_char is not None and self.current_char in Datatypes.LETTERS:
            return [Token(Datatypes.NUMBER, Datatypes.Number(number)), Token(Datatypes.MULT_SIGN), self.gen_identifier()]
        return [Token(Datatypes.NUMBER, Datatypes.Number(number))]

    def gen_identifier(self):
        identifier = ""
        while self.current_char is not None and self.current_char in Datatypes.LETTERS.union(Datatypes.NUM_CHARS):
            identifier += self.current_char
            self.next_char()
        kw_id = OXYGEN_DICT.get(identifier)
        return Token(kw_id) if kw_id is not None else Token(Datatypes.IDENTIFIER, identifier)

    def gen_string(self):
        quotation_mark = self.current_char
        self.next_char()
        string = ""
        tokens = deque()
        escaped = False
        while self.current_char not in (None, quotation_mark):
            if self.current_char == "#" and not escaped:
                string += self.current_char
                self.next_char()
                token_string = ""
                while self.current_char not in (None, "#", quotation_mark):
                    token_string += self.current_char
                    self.next_char()
                if self.current_char in (None, quotation_mark):
                    raise SyntaxError("Expected '#'")
                tokens.append(Lexer(token_string).gen_tokens())
            else:
                escaped = False
                string += self.current_char
            if self.current_char == "\\":
                escaped = True
            self.next_char()
        if self.current_char != quotation_mark:
            raise SyntaxError(f"Expected {quotation_mark}")
        self.next_char()
        return Token(Datatypes.STRING, Datatypes.StringBuilderNode(string=Datatypes.String(string), tokens=tokens))
