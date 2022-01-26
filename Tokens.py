from collections import namedtuple

# Matches token types to easily-compared numbers

token = namedtuple("token", "type value", defaults=(None, None))
NUMBER = 0
PLUS_SIGN = 1
MINUS_SIGN = 2
MULT_SIGN = 3
DIV_SIGN = 4
MODULUS_SIGN = 5
PLUS_ASSIGN = 6
MINUS_ASSIGN = 7
MULT_ASSIGN = 8
DIV_ASSIGN = 9
MODULUS_ASSIGN = 10
LPAREN = 11
RPAREN = 12
IDENTIFIER = 13
EQUALS = 14
EXP = 15
FUNCTION_OPERATOR = 16
FUNCTION_KEYWORD = 17
PERIOD_FUNC_CALL = 18
COMMA = 19
COMP_EQUALS = 20
COMP_NOT_EQUALS = 21
GREATER_THAN = 22
LESS_THAN = 23
GREATER_OR_EQUALS = 24
LESS_OR_EQUALS = 25
TRUE = 26
FALSE = 27
# Debug
# Can make lexer output readable
type_dict = {
    0: "NUMBER",
    1: "PLUS_SIGN",
    2: "MINUS_SIGN",
    3: "MULT_SIGN",
    4: "DIV_SIGN",
    5: "MODULUS_SIGN",
    6: "PLUS_ASSIGN",
    7: "MINUS_ASSIGN",
    8: "MULT_ASSIGN",
    9: "DIV_ASSIGN",
    10: "MODULUS_ASSIGN",
    11: "LPAREN",
    12: "RPAREN",
    13: "IDENTIFIER",
    14: "EQUALS",
    15: "EXPONENTIAL_SIGN",
    16: "FUNCTION_OPERATOR",
    17: "FUNCTION_KEYWORD",
    18: "PERIOD_FUNC_CALL",
    19: "COMMA",
    20: "COMP_EQUALS",
    21: "COMP_NOT_EQUALS",
    22: "GREATER_THAN",
    23: "LESS_THAN",
    24: "GREATER_OR_EQUALS",
    25: "LESS_OR_EQUALS",
    26: "TRUE",
    27: "FALSE"
}
