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
                 "[": Datatypes.LBRACKET, "]": Datatypes.RBRACKET, ">>": Datatypes.ARRAYAPPLY, ">>>": Datatypes.ARRAYAPPLY_ASSIGN,
                ":": Datatypes.COLON
                 }
KEYWORD_DICT = {"if": Datatypes.IF, "else": Datatypes.ELSE, "fn": Datatypes.FUNCTION_KEYWORD,
                "True": Datatypes.TRUE, "False": Datatypes.FALSE, "not": Datatypes.NOT, "or": Datatypes.OR,
                "and": Datatypes.AND, "rep": Datatypes.REP, "as": Datatypes.AS, "for": Datatypes.FOR,
                "return": Datatypes.RETURN, "break": Datatypes.BREAK, "continue": Datatypes.CONTINUE, "in": Datatypes.IN,
                "iter": Datatypes.ITERATE, "del": Datatypes.DEL, "let": Datatypes.LET, "equals": Datatypes.EQUALS, 
                "greater": Datatypes.GREATER_THAN, "smaller": Datatypes.LESS_THAN, "while": Datatypes.WHILE}


# TODO: replace this with a regex lexer


# LEXER/TOKENIZER
# Is responsible for generating a list of tokens based on a string input using the pre-defined Tokens
# from the Datatypes.py file.
class Lexer:
    # Defines an iterator based on the string input
    def __init__(self, text):
        self.text = iter(text)
        self.current_char = None
        self.ignore = False
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
            # Concludes current token list and starts a new one after the statement separator ";"
            if self.current_char in ";\n":
                self.ignore = False
                tokens.append(Token(Datatypes.LINEBREAK))
                self.next_char()
            # Skips whitespace entirely
            elif self.current_char in [" ", "\t"] or self.ignore:
                self.next_char()
            # Ignores any input after "~"
            elif self.current_char == "~":
                self.next_char()
                self.ignore = True
            # For some characters, there needs to be a check for other characters after them
            elif self.current_char in OPERATOR_DICT:
                char = self.current_char
                self.next_char()
                operator = char + str(self.current_char)
                if operator in OPERATOR_DICT:
                    self.next_char()
                    if operator + str(self.current_char) in OPERATOR_DICT:
                        tokens.append(Token(OPERATOR_DICT[operator + str(self.current_char)]))
                        self.next_char()
                    else:
                        tokens.append(Token(OPERATOR_DICT[operator]))
                else:
                    tokens.append(Token(OPERATOR_DICT[char]))
                if self.current_char == ".":
                    tokens.append(Token(Datatypes.PERIOD_CALL))
                    self.next_char()
            elif self.current_char in (NUM_CHARS + "."):
                num, add_period_call = self.gen_number()
                tokens.append(num)
                if add_period_call:
                    tokens.append(Token(Datatypes.PERIOD_CALL))
            elif self.current_char in LETTERS:
                tokens.append(self.gen_identifier())
                # Will recognize when a function is called with a period after the identifier
                if self.current_char == ".":
                    tokens.append(Token(Datatypes.PERIOD_CALL))
                    self.next_char()
            elif self.current_char in ("\"", "\'"):
                tokens.append(self.gen_string())
                if self.current_char == ".":
                    tokens.append(Token(Datatypes.PERIOD_CALL))
                    self.next_char()
            else:
                raise Exception(f"Illegal Character {self.current_char}")
        return tokens

    # Will generate and return a number with multiple or one digit(s)
    def gen_number(self):
        add_period_call = False
        number = ""
        while self.current_char is not None and self.current_char in (NUM_CHARS + "."):
            number += self.current_char
            self.next_char()
        # Will change ie. ".5" to "0.5"
        if number.startswith("."):
            number = "0" + number
        if number.endswith("."):
            add_period_call = True
        # A number with multiple periods will raise an exception
        if number.count(".") > 1:
            raise ValueError(f"Illegal number {number}")
        return Token(Datatypes.NUMBER, Datatypes.Number(number)), add_period_call

    # Will generate and return an identifier with multiple or one letter(s)
    def gen_identifier(self):
        identifier = ""
        while self.current_char is not None and self.current_char in (LETTERS + NUM_CHARS):
            identifier += self.current_char
            self.next_char()
        # If the entered identifier is a keyword, it will be matched to its ID
        kw_id = KEYWORD_DICT.get(identifier)
        return Token(kw_id) if kw_id is not None else Token(Datatypes.IDENTIFIER, identifier)

    def gen_string(self):
        quotation_mark = self.current_char
        self.next_char()
        string = ""
        while self.current_char is not None and self.current_char != quotation_mark:
            string += self.current_char
            self.next_char()
        if self.current_char != quotation_mark:
            raise SyntaxError(f"Expected {quotation_mark}")
        self.next_char()
        return Token(Datatypes.STRING, Datatypes.String(string))
