from collections import namedtuple


# CUSTOM BOOLEAN DATACLASS
# Exists to make the Interpreter Bools customizable


class Bool:
    def __init__(self, value=None):
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


class String:
    def __init__(self, value=None):
        if isinstance(value, float) and value % 1 == 0:
            self.str = str(int(value))
        else:
            self.str = str(value)

    def __str__(self):
        return self.str

    def __repr__(self):
        return self.str


# Defines a function consisting of the arguments and the body
class Function:
    def __init__(self, arguments, body):
        self.arguments = arguments
        self.body = body

    def __repr__(self):
        return f"FUNCTION: \n ARGS = {self.arguments} \n BODY = {self.body}"


# Defines a token consisting of a type ID and some value
class Token:
    def __init__(self, type=None, value=None):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"TOKEN({type_dict.get(self.type)}" + (f", VALUE = {self.value})" if self.value is not None else ")")


class IfNode:
    def __init__(self):
        self.blocks = []

    def add_block(self, keyword, statements, condition=None):
        self.blocks.append({"keyword": keyword, "condition": condition, "statements": statements})

    def __repr__(self):
        repr = ""
        for block in self.blocks:
            kw = block["keyword"]
            condition = block["condition"]
            statements = block["statements"]
            repr += f"{type_dict.get(kw)} {condition} {statements}; "
        return repr


# TOKEN TYPE IDs
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
ARROW = 16
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
IF = 31
ELSE = 32
REP = 33
FOR = 34
STRING = 35
AS = 36
DOUBLE_MINUS = 37
DOUBLE_PLUS = 38
BLOCK_END = 39
RETURN = 40
PRINT = 41
LCURLY = 42
RCURLY = 43

# NODE TYPES
AddNode = namedtuple("AddNode", ["a", "b"])
SubNode = namedtuple("SubNode", ["a", "b"])
MultNode = namedtuple("MultNode", ["a", "b"])
DivNode = namedtuple("DivNode", ["a", "b"])
ModulusNode = namedtuple("ModulusNode", ["a", "b"])
ExpNode = namedtuple("ExpNode", ["a", "b"])
AssignNode = namedtuple("AssignNode", ["identifier", "value"])
VariableNode = namedtuple("VariableNode", ["identifier"])
FuncDeclareNode = namedtuple("FuncDeclareNode", ["identifier", "arguments", "body"])
FuncCallNode = namedtuple("FuncCallNode", ["identifier", "arguments"])
ComparisonNode = namedtuple("ComparisonNode", ["a", "b", "operator"])
BooleanNegationNode = namedtuple("BooleanNegationNode", ["value"])
BooleanConversionNode = namedtuple("BooleanConversionNode", ["value"])
LogicalOperationNode = namedtuple("LogicalOperationNode", ["a", "b", "operation"])
RepNode = namedtuple("RepNode", ["repetitions", "count_identifier", "statements"])
ForNode = namedtuple("ForNode", ["assignment", "condition", "increment", "statements"])
ReturnNode = namedtuple("ReturnNode", ["statement"])
PrintNode = namedtuple("PrintNode", ["statement"])

# Returns the correct node for operations
OPERATOR_NODE_DICT = {PLUS_SIGN: AddNode, MINUS_SIGN: SubNode, MULT_SIGN: MultNode, DIV_SIGN: DivNode,
                      MODULUS_SIGN: ModulusNode, EQUALS: AssignNode, PLUS_ASSIGN: AddNode, MINUS_ASSIGN: SubNode,
                      MULT_ASSIGN: MultNode, DIV_ASSIGN: DivNode, MODULUS_ASSIGN: ModulusNode}

# Debug
# Helps to make tokens more readable
type_dict = {
    NUMBER: "NUMBER",
    PLUS_SIGN: "PLUS_SIGN",
    MINUS_SIGN: "MINUS_SIGN",
    MULT_SIGN: "MULT_SIGN",
    DIV_SIGN: "DIV_SIGN",
    MODULUS_SIGN: "MODULUS_SIGN",
    PLUS_ASSIGN: "PLUS_ASSIGN",
    MINUS_ASSIGN: "MINUS_ASSIGN",
    MULT_ASSIGN: "MULT_ASSIGN",
    DIV_ASSIGN: "DIV_ASSIGN",
    MODULUS_ASSIGN: "MODULUS_ASSIGN",
    LPAREN: "LPAREN",
    RPAREN: "RPAREN",
    IDENTIFIER: "IDENTIFIER",
    EQUALS: "EQUALS",
    EXP: "EXPONENTIAL_SIGN",
    ARROW: "ARROW",
    FUNCTION_KEYWORD: "FUNCTION_KEYWORD",
    PERIOD_FUNC_CALL: "PERIOD_FUNC_CALL",
    COMMA: "COMMA",
    COMP_EQUALS: "COMP_EQUALS",
    COMP_NOT_EQUALS: "COMP_NOT_EQUALS",
    GREATER_THAN: "GREATER_THAN",
    LESS_THAN: "LESS_THAN",
    GREATER_OR_EQUALS: "GREATER_OR_EQUALS",
    LESS_OR_EQUALS: "LESS_OR_EQUALS",
    TRUE: "TRUE",
    FALSE: "FALSE",
    NOT: "NOT",
    AND: "AND",
    OR: "OR",
    IF: "IF",
    ELSE: "ELSE",
    REP: "REP",
    FOR: "FOR",
    STRING: "STRING",
    AS: "AS",
    DOUBLE_MINUS: "DOUBLE_MINUS",
    DOUBLE_PLUS: "DOUBLE_PLUS",
    BLOCK_END: "BLOCK_END",
    RETURN: "RETURN",
    PRINT: "PRINT",
    LCURLY: "LCURLY",
    RCURLY: "RCURLY",
}
