from collections import namedtuple

# Matches token types to an easily-compared number

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
EXP = 10
FUNCTION_OPERATOR = 11
FUNCTION_KEYWORD = 12
PERIOD_FUNC_CALL = 13
COMMA = 14

# Debug
# Can make lexer output readable
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
    10: "EXPONENTIAL_SIGN",
    11: "FUNCTION_OPERATOR",
    12: "FUNCTION_KEYWORD",
    13: "PERIOD_FUNC_CALL",
    14: "COMMA"
}
