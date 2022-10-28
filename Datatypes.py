from collections import namedtuple
from sqlite3 import DatabaseError

class String:
    def __init__(self, value=None):
        if isinstance(value, float) and value % 1 == 0:
            self.str = str(int(value))
        else:
            self.str = str(value)

    def __len__(self):
        return len(self.str)

    def __str__(self):
        return self.str

    def __repr__(self):
        return "\"" + self.str + "\""

    def __iter__(self):
        self.n = 0
        self.max = len(self)
        self.str_arr = list(self.str)
        return self

    def __next__(self):
        if self.n < self.max:
            res = self.str_arr[self.n]
            self.n += 1
            return String(res)
        else:
            self.str = str(Array(self.str_arr).join(""))
            raise StopIteration  
    
    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False
    
    def __add__(self, other):
        return String(str(self) + str(other))

    def __mul__(self, num):
        if isinstance(num, float) and num%1==0:
            num = int(num)
        if num<1:
            raise TypeError("Cannot divide arrays.")
        if not isinstance (num, int):
            raise TypeError(f"Cannot multiply Array with {type(num).__name__}")
        self.str*=num
        return self       

    def __eq__(self, other):
        return str(self) == str(other)

    def __getitem__(self, index):
        if isinstance(index, float) and index%1 == 0:
            index = int(index)
        return String(self.str[index])

    def __setitem__(self, index, val):
        lst = list(self.str)
        if isinstance(index, float) and index%1 == 0:
            index = int(index)
        try:
            lst[index] = str(String(val))
        except IndexError:
            pass
        self.str_arr[index] = str(String(val))
        self.str = "".join(lst)
    
    def reverse(self):
        self.str = self.str[::-1]
        return self

    def split(self, delimiter):
        return Array([String(s) for s in self.str.split(delimiter)])

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
    
    def __str__(self):
        return self.__repr__()

    def __bool__(self):
        return self.boolean_value

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

    def reverse(self):
        self.boolean_value = not self.boolean_value


class Array:
    def __init__(self, contents):
        self.contents = contents
        self.n = []
    
    def __str__(self):
        if len(self) ==0:
            return "[]"
        repr = "["
        for c in self.contents:
            repr += String(c).str + ", "
        repr = repr[:-2]
        repr += "]"
        return repr
    
    def __len__(self):
        return len(self.contents)

    def __iter__(self):
        self.n.append(0)
        self.max = len(self)
        return self

    def __add__(self, elem):
        return Array(self.contents.copy() +[elem])
    
    def __mul__(self, num):
        if isinstance(num, float) and num%1==0:
            num = int(num)
        if num<1:
            raise TypeError("Cannot divide arrays.")
        if not isinstance (num, int):
            raise TypeError(f"Cannot multiply Array with {type(num).__name__}")
        self.contents*=num
        return self        
    
    def __sub__(self, elem):
        for i in reversed(range(len(self))):
            if self[i] == elem:
                del self[i]
        return self        

    def __next__(self):
        if self.n[-1] < self.max:
            res = self.contents[self.n[-1]]
            self.n[-1] += 1
            return res
        else:
            self.n.pop()
            raise StopIteration        
        
    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        try:
            if len(self) != len(other):
                return Bool(False)
            _ = iter(other)
            eq = True
            for i, v in enumerate(self):
                if v != other[i]:
                    eq = False
            return Bool(eq)
        except TypeError:
            raise TypeError(f"{type(other).__name__} object is not iterable.")         

    def __getitem__(self, index):
        if isinstance(index, float) and index%1 == 0:
            index = int(index)
        return self.contents[index]

    def __contains__(self, elem):
        return elem in self.contents

    def __setitem__(self, index, val):
        if isinstance(index, float) and index%1 == 0:
            index = int(index)
        self.contents[index] = val

    def intersection(self, other):
        new = []
        for elem in self:
            if elem in other:
                new.append(elem)
        self.contents = new
        return self
    
    def union(self, other):
        for elem in other:
            if elem not in self:
                self.contents.append(elem)
        return self
    
    def delete(self):
        del self.contents[self.n[-1]-1]
        self.n[-1] -= 1
        self.max -= 1
        return self
    
    def remove(self, element):
        self.n[-1] -= 1
        self.max -= 1
        self.contents.remove(element)
        return self
    
    def join(self, delimiter):
        return String(str(delimiter).join([str(s) for s in self.contents]))
    
    def sum(self):
        s = 0
        for el in self.contents:
            if isinstance(el, float):
                s += el
            elif isinstance(el, Array):
                s += el.sum()
            else:
                raise TypeError(f"Cannot add item of type {type(el).__name__} to sum")
        return s
    
    def min(self):
        return min(self.contents)

    def max(self):
        return max(self.contents)

    def reverse(self):
        self.contents.reverse()
        return self
            

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

    def add_block(self, keyword, body, condition=None):
        self.blocks.append({"keyword": keyword, "condition": condition, "body": body})

    def __repr__(self):
        repr = "IfNode("
        for block in self.blocks:
            kw = type_dict.get(block["keyword"])
            condition = block["condition"]
            body = block["body"]
            repr += f"[keyword = {kw}, condition = {condition}, body = {body}]"
        repr += ")"
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
PERIOD_CALL = 18
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
LCURLY = 41
RCURLY = 42
SOLVE_ASSIGN = 43
SOLVE = 44
LINEBREAK = 45
BREAK = 46
CONTINUE = 47
LBRACKET = 48
RBRACKET = 49
ARRAYAPPLY = 50
IN = 51
ITERATE = 52
DEL = 53

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
SolveNode = namedtuple("SolveNode", ["left_side", "right_side"])
SolveAssignNode = namedtuple("SolveAssignNode", ["left_side", "right_side"])
BreakNode = namedtuple("BreakNode", [])
ContinueNode = namedtuple("ContinueNode", [])
ArrayCallNode = namedtuple("ArrayCallNode", ["identifier", "index"])
ArrayApplyNode = namedtuple("ArrayApplyNode", ["identifier", "function"])
PeriodCallNode = namedtuple("PeriodCallNode", ["left_side", "right_side"])
ForEachNode = namedtuple("ForEachNode", ["item", "iterable", "statements"])
ContainsNode = namedtuple("ContainsNode", ["iterable", "item"])
IterateNode = namedtuple("IterateNode", ["iterable", "items", "statements"])

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
    PERIOD_CALL: "PERIOD_FUNC_CALL",
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
    LCURLY: "LCURLY",
    RCURLY: "RCURLY",
    SOLVE_ASSIGN: "SOLVE_ASSIGN",
    SOLVE: "SOLVE",
    LINEBREAK: "LINEBREAK",
    BREAK: "BREAK",
    CONTINUE: "CONTINUE",
    LBRACKET: "LBRACKET",
    RBRACKET: "RBRACKET",
    ARRAYAPPLY: "ARRAYAPPLY",
    IN: "IN",
    ITERATE: "ITERATE",
    DEL: "DEL"
}
