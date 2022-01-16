from collections import namedtuple
# Includes token types

token = namedtuple("token", "type value", defaults=(None, None))
NUMBER = 0
PLUS_SIGN = 1
MINUS_SIGN = 2
MULT_SIGN = 3
DIV_SIGN = 4
MODULUS_SIGN = 5
LPAREN = 6
RPAREN = 7
IDENTIFIER = 8
EQUALS = 9
KEYWORD = 10
EXP = 11
FUNCTION_OPERATOR = 12
FUNCTION_KEYWORD = 13
PERIOD_FUNC_CALL = 14
COMMA = 15

# Debug
type_dict = {
    0: "NUMBER",
    1: "PLUS_SIGN",
    2: "MINUS_SIGN",
    3: "MULT_SIGN",
    4: "DIV_SIGN",
    5: "MODULUS_SIGN",
    6: "LPAREN",
    7: "RPAREN",
    8: "IDENTIFIER",
    9: "EQUALS",
    10: "KEYWORD",
    11: "EXPONENTIAL_SIGN",
    12: "FUNCTION_OPERATOR",
    13: "FUNCTION_KEYWORD",
    14: "PERIOD_FUNC_CALL",
    15: "COMMA"
}
