from collections import namedtuple


# CUSTOM BOOLEAN DATACLASS
class Bool:
    def __init__(self, value: bool = None):
        if isinstance(value, bool):
            self.boolean_value = value
        elif isinstance(value, Bool):
            self.boolean_value = value.boolean_value
        elif isinstance(value, float):
            if value == 0:
                self.boolean_value = False
            else:
                self.boolean_value = True
        elif value is None:
            self.boolean_value = False
        else:
            raise TypeError(f"Type {type(value).__name__} could not be converted to bool.")

    def __repr__(self):
        if self.boolean_value is False:
            return "False"
        if self.boolean_value is True:
            return "True"

    def __bool__(self):
        return self.boolean_value

    def reverse(self):
        self.boolean_value = not self.boolean_value


# TOKEN
token = namedtuple("token", "type value", defaults=(None, None))
# TOKEN TYPES
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
NOT = 28
AND = 29
OR = 30

# NODE TYPES
AddNode = namedtuple("AddNode", ["a", "b"])
SubNode = namedtuple("SubNode", ["a", "b"])
MultNode = namedtuple("MultNode", ["a", "b"])
DivNode = namedtuple("DivNode", ["a", "b"])
ModulusNode = namedtuple("ModulusNode", ["a", "b"])
ExpNode = namedtuple("ExpNode", ["a", "b"])
AssignNode = namedtuple("AssignNode", ["identifier", "value"])
VariableNode = namedtuple("VariableNode", ["identifier"])
KeywordNode = namedtuple("KeywordNode", ["keyword", "value"])
FuncDeclareNode = namedtuple("FuncDeclareNode", ["identifier", "arguments", "body"])
FuncCallNode = namedtuple("FuncCallNode", ["identifier", "arguments"])
ComparisonNode = namedtuple("ComparisonNode", ["a", "b", "operator"])
BooleanNegationNode = namedtuple("BooleanNegationNode", ["value"])
BooleanConversionNode = namedtuple("BooleanConversionNode", ["value"])
LogicalOperationNode = namedtuple("LogicalOperationNode", ["a", "b", "operation"])

# Defines a function consisting of the arguments and the body
function = namedtuple("function", ["arguments", "body"])


# Returns the correct node for operation assignments
def match_operator_to_node(operator_id):
    id = operator_id
    if id == PLUS_ASSIGN:
        return AddNode
    elif id == MINUS_ASSIGN:
        return SubNode
    elif id == MULT_ASSIGN:
        return MultNode
    elif id == DIV_ASSIGN:
        return DivNode
    else:
        return ModulusNode


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
    27: "FALSE",
    28: "NOT",
    29: "AND",
    30: "OR"
}
