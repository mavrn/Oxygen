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
                 }
KEYWORD_DICT = {"if": Datatypes.IF, "else": Datatypes.ELSE, "fn": Datatypes.FUNCTION_KEYWORD,
                "True": Datatypes.TRUE, "False": Datatypes.FALSE, "not": Datatypes.NOT, "or": Datatypes.OR,
                "and": Datatypes.AND, "rep": Datatypes.REP}


# TODO: replace this with a regex lexer


# LEXER/TOKENIZER
# Is responsible for generating a list of tokens based on a string input using the pre-defined Tokens
# from the Datatypes.py file.
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
        tokens_list = []
        while self.current_char is not None:
            # Skips whitespace entirely
            if self.current_char == " ":
                self.next_char()
            # Ignores any input after "~"
            elif self.current_char == "~":
                break
            # Concludes current token list and starts a new one after the statement seperator ";"
            elif self.current_char == ";":
                tokens_list.append(tokens)
                tokens = []
                self.next_char()
            # For some characters, there needs to be a check for other characters after them
            elif self.current_char in OPERATOR_DICT:
                char = self.current_char
                self.next_char()
                operator = char + str(self.current_char)
                if operator in OPERATOR_DICT:
                    tokens.append(Token(OPERATOR_DICT[operator]))
                    self.next_char()
                else:
                    tokens.append(Token(OPERATOR_DICT[char]))
            elif self.current_char in (NUM_CHARS + "."):
                tokens.append(self.gen_number())
            elif self.current_char in LETTERS:
                identifier = self.gen_string()
                # If the entered identifier is a keyword, it will be matched to its ID
                if identifier in KEYWORD_DICT:
                    tokens.append(Token(KEYWORD_DICT[identifier]))
                else:
                    tokens.append(Token(Datatypes.IDENTIFIER, identifier))
                # Will recognize when a function is called with a period after the identifier
                if self.current_char == ".":
                    tokens.append(Token(Datatypes.PERIOD_FUNC_CALL))
                    self.next_char()
            elif self.current_char in ("\"", "\'"):
                quotation_mark = self.current_char
                self.next_char()
                string = Datatypes.String(self.gen_string())
                if self.current_char != quotation_mark:
                    raise SyntaxError(f"Expected {quotation_mark}")
                tokens.append(Token(Datatypes.STRING, string))
                self.next_char()
            else:
                raise Exception(f"Illegal Character {self.current_char}")
        if len(tokens) > 0:
            tokens_list.append(tokens)
        return tokens_list

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
            raise ValueError(f"Illegal number {number}")
        return Token(Datatypes.NUMBER, float(number))

    # Will generate and return an identifier with multiple or one letter(s)
    def gen_string(self):
        string = ""
        while self.current_char is not None and self.current_char in (LETTERS + NUM_CHARS):
            string += self.current_char
            self.next_char()
        return string
