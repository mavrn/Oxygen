import Datatypes
from Datatypes import Token

NUM_CHARS = "0123456789"
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_"
OPERATOR_DICT = {"+": Datatypes.PLUS_SIGN, "-": Datatypes.MINUS_SIGN, "*": Datatypes.MULT_SIGN, "/": Datatypes.DIV_SIGN,
                 "%": Datatypes.MODULUS_SIGN, "+=": Datatypes.PLUS_ASSIGN, "-=": Datatypes.MINUS_ASSIGN,
                 "*=": Datatypes.MULT_ASSIGN, "/=": Datatypes.DIV_ASSIGN, "%=": Datatypes.MODULUS_ASSIGN,
                 "(": Datatypes.LPAREN, ")": Datatypes.RPAREN, "^": Datatypes.EXP, ",": Datatypes.COMMA,
                 "&": Datatypes.AND, "|": Datatypes.OR, "==": Datatypes.COMP_EQUALS, "!=": Datatypes.COMP_NOT_EQUALS,
                 "<": Datatypes.LESS_THAN, ">": Datatypes.GREATER_THAN, "<=": Datatypes.LESS_OR_EQUALS,
                 ">=": Datatypes.GREATER_OR_EQUALS, "=>": Datatypes.ARROW, "=": Datatypes.EQUALS, "!": Datatypes.NOT,
                 "--": Datatypes.DOUBLE_MINUS, "++": Datatypes.DOUBLE_PLUS, "<<": Datatypes.BLOCK_END,
                 "{": Datatypes.LCURLY, "}": Datatypes.RCURLY, "?=": Datatypes.SOLVE_ASSIGN, "?": Datatypes.SOLVE,
                 "[": Datatypes.LBRACKET, "]": Datatypes.RBRACKET, ">>": Datatypes.ARRAYAPPLY,
                 ">>>": Datatypes.ARRAYAPPLY_ASSIGN, ":": Datatypes.COLON, "//": Datatypes.FLOORDIV_SIGN}
KEYWORD_DICT = {"if": Datatypes.IF, "else": Datatypes.ELSE, "fn": Datatypes.FUNCTION_KEYWORD, "True": Datatypes.TRUE,
                "False": Datatypes.FALSE, "not": Datatypes.NOT, "or": Datatypes.OR, "and": Datatypes.AND,
                "rep": Datatypes.REP, "as": Datatypes.AS, "for": Datatypes.FOR, "return": Datatypes.RETURN,
                "break": Datatypes.BREAK, "continue": Datatypes.CONTINUE, "in": Datatypes.IN, "iter": Datatypes.ITERATE,
                "del": Datatypes.DEL, "let": Datatypes.LET, "equals": Datatypes.EQUALS,
                "greater": Datatypes.GREATER_THAN, "smaller": Datatypes.LESS_THAN, "while": Datatypes.WHILE,
                }


class Lexer:
    def __init__(self, text):
        self.text = iter(text)
        self.current_char = None
        self.ignore = False
        self.next_char()

    def next_char(self):
        try:
            self.current_char = next(self.text)
        except StopIteration:
            self.current_char = None

    def gen_tokens(self):
        tokens = []
        while self.current_char is not None:
            current_char = self.current_char
            if current_char in ";\n":
                self.ignore = False
                tokens.append(Token(Datatypes.LINEBREAK))
                self.next_char()
            elif current_char in [" ", "\t"] or self.ignore:
                self.next_char()
            elif current_char == "~":
                self.next_char()
                self.ignore = True
            elif current_char in OPERATOR_DICT:
                self.next_char()
                operator = current_char + str(self.current_char)
                if operator in OPERATOR_DICT:
                    self.next_char()
                    if operator + str(self.current_char) in OPERATOR_DICT:
                        tokens.append(Token(OPERATOR_DICT[operator + str(self.current_char)]))
                        self.next_char()
                    else:
                        tokens.append(Token(OPERATOR_DICT[operator]))
                else:
                    tokens.append(Token(OPERATOR_DICT[current_char]))
            elif current_char in NUM_CHARS:
                num_tokens = self.gen_number()
                for token in num_tokens:
                    tokens.append(token)
            elif current_char in LETTERS:
                tokens.append(self.gen_identifier())
            elif current_char == ".":
                self.next_char()
                tokens.append(Token(Datatypes.PERIOD_CALL))
            elif current_char in ("\"", "\'"):
                tokens.append(self.gen_string())
            else:
                raise SyntaxError(f"Unexpected character {current_char}")
        return tokens

    def gen_number(self):
        number = ""
        while self.current_char is not None and self.current_char in (NUM_CHARS + "."):
            number += self.current_char
            self.next_char()
        if number.endswith("."):
            number = number[:-1]
            return [Token(Datatypes.NUMBER, Datatypes.Number(number)), Token(Datatypes.PERIOD_CALL)]
        return [Token(Datatypes.NUMBER, Datatypes.Number(number))]

    def gen_identifier(self):
        identifier = ""
        while self.current_char is not None and self.current_char in (LETTERS + NUM_CHARS):
            identifier += self.current_char
            self.next_char()
        kw_id = KEYWORD_DICT.get(identifier)
        return Token(kw_id) if kw_id is not None else Token(Datatypes.IDENTIFIER, identifier)

    def gen_string(self):
        quotation_mark = self.current_char
        self.next_char()
        string = ""
        tokens = []
        escaped = False
        while self.current_char not in (None, quotation_mark):
            if self.current_char == "#" and not escaped:
                string += self.current_char
                self.next_char()
                token_string = ""
                while self.current_char not in (None, "#", quotation_mark):
                    token_string += self.current_char
                    self.next_char()
                    print(self.current_char)
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
