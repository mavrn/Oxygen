from collections import namedtuple, Counter
from itertools import combinations, permutations, combinations_with_replacement

ALPHABET_MAP = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H":8 , "I":9, "J":10, "K":11, "L":12, "M":13,
                "N":14, "O":15, "P":16, "Q":17, "R":18, "S":19, "T":20, "U":21, "V":22, "W":23, "X":24, "Y":25, "Z":26}

def convert_to_ints(arglist):
    return [int(elem) if (isinstance(elem, float) and elem%1==0) else elem for elem in arglist]

class String:
    def __init__(self, value=None):
        if isinstance(value, float) and value % 1 == 0:
            self.str = str(int(value))
        elif value is None:
            self.str = None
        elif isinstance(value, String):
            self.str = value.str
        else:
            self.str = str(value)
        self.str_arr = []
        self.n = []


    def __len__(self):
        return len(self.str)

    def __str__(self):
        return self.str

    def __repr__(self):
        return "\"" + self.str + "\""

    def copy(self):
        return String(self.str)

    def __iter__(self):
        self.n.append(0)
        self.max = len(self)
        self.str_arr.append(list(self.str))
        return self

    def __next__(self):
        if self.n[-1] < self.max:
            res = self.str_arr[-1][self.n[-1]]
            self.n[-1] += 1
            return String(res)
        else:
            self.str = str(Array(self.str_arr.pop()).join(""))
            self.n.pop()
            raise StopIteration  
    
    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False
    
    def __add__(self, other):
        return String(str(self) + str(String(other)))
    
    def __radd__(self, other):
        return String(str(self) + str(String(other)))

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
        self.str_arr[-1][index] = str(String(val))
        self.str = "".join(lst)
    
    def slice(self, *args):
        args = convert_to_ints(args)
        if len(args) == 1:
            stop = args[0]
            start = 0
            step = 1
        elif len(args)==2:
            start, stop = args
            step = 1
        else:
            start, stop, step = args
        return String(self.str[start:stop:step])
    
    def append(self, *args):
        for arg in args:
            self += arg
        return self
            
    def nummap(self):
        new = Array([])
        for char in self.str:
            if char.capitalize() in ALPHABET_MAP:
                new += str(ALPHABET_MAP[char.capitalize()])
            else:
                new += char
        return new  
    
    def delete(self):
        del self.str_arr[-1][self.n[-1]-1]
        self.n[-1] -= 1
        self.max -= 1
        return self

    def deleteAt(self, *args):
        for arg in convert_to_ints(args):
            del self.str[arg]
    
    def pop(self, *args):
        return self.contents.pop(*convert_to_ints(args))

    def posof(self, value):
        return self.str.index(str(value))

    def lower(self):
        return String(self.str.lower())
    
    def upper(self):
        return String(self.str.upper())
    
    def capitalize(self):
        return String(self.str.capitalize())
    
    def strip(self, *args):
        if len(args) == 0:
            delimiters = " "
        else:
            delimiters = ""
            for arg in args:
                delimiters += str(arg)
        return String(self.str.strip(delimiters))
    
    def replace(self, *args):
        return String(self.str.replace(*[str(arg) for arg in args]))
    
    def isupper(self):
        return Bool(self.str.isupper())
    
    def islower(self):
        return Bool(self.str.islower())
    
    def iscapitalized(self):
        return Bool(self.str.istitle())
        
    def count(self, *args):
        ct = 0
        for arg in args:
            if not isinstance(arg, String):
                raise TypeError("Expected type String for function count")
            ct += self.str.count(str(arg))
        return float(ct)
    
    def mostcommon(self, *args):
        c = Counter(list([str(s) for s in self.str]))
        results = []
        args = convert_to_ints(args)
        if len(args) == 0:
            ranking_length = 3
        else:
            ranking_length = args[0]
        for tup in c.most_common(ranking_length):
            results.append(Array(list(tup)))
        return Array(results)

    def combinations(self, *args):
        temp = []
        for comb in combinations(self.str, *convert_to_ints(args)):
            temp.append(Array(list(comb)))
        return Array(temp)

    def allcombinations(self):
        temp = []
        for length in range(len(self.str) +1):
            for subset in combinations(self.str, length):
                temp.append(Array(list(subset)))
        return Array(temp)
    
    def multicombinations(self, *args):
        temp = []
        if len(args) == 0:
            args = [len(self)]
        for comb in combinations_with_replacement(self.str, *convert_to_ints(args)):
            temp.append(Array(list(comb)))
        return Array(temp)

    def permutations(self):
        temp = []
        for comb in permutations(self.str):
            temp.append(Array(list(comb)))
        return Array(temp)
    
    def removeduplicates(self):
        return Array(list(dict.fromkeys(list(self.str))))

    def rev(self):
        self.str = self.str[::-1]
        return self

    def split(self, *args):
        if len(args) == 0:
            return Array([String(s) for s in self.str.split()])
        new = self.str.replace(r" ", " ")
        master = str(args[0])
        for i in range(1, len(args)):
            new = new.replace(str(args[i]), master)
        return Array([String(s) for s in new.split(str(master))])

class Bool:
    def __init__(self, value=None):
        if isinstance(value, bool):
            self.boolean_value = value
        elif isinstance(value, Bool):
            self.boolean_value = value.boolean_value
        elif isinstance(value, float) or isinstance(value, int):
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

    def rev(self):
        self.boolean_value = not self.boolean_value


class Array:
    def __init__(self, contents):
        self.contents = contents
        self.n = []
    
    def process_element(self, elem):
        if isinstance(elem, float) and elem%1==0:
            return int(elem)
        if isinstance(elem, str):
            return String(elem)
        return elem

    def __str__(self):
        if len(self) ==0:
            return "[]"
        res = "["
        for c in self.contents:
            res += repr(self.process_element(c)) + ", "
        res = res[:-2]
        res += "]"
        return res
    
    def __len__(self):
        return len(self.contents)

    def __iter__(self):
        self.n.append(0)
        self.max = len(self)
        return self

    def __add__(self, elem):
        return Array(self.contents.copy() +[elem])
    
    def copy(self):
        return Array(self.contents.copy())

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
    
    def append(self, *args):
        for arg in args:
            self += arg
        return self

    def convert_to_builtins(self):
        new = []
        for element in self.contents:
            if isinstance(element, Array):
                new.append(element.contents)
            elif isinstance(element, String):
                new.append(element.str)
            elif isinstance(element, Bool):
                new.append(element.boolean_value)
            elif isinstance(element, float) and element%1==0:
                new.append(int(element))
            else:
                new.append(element)
        return new

    def slice(self, *args):
        args = convert_to_ints(args)
        if len(args) == 1:
            stop = args[0]
            start = 0
            step = 1
        elif len(args)==2:
            start, stop = args
            step = 1
        else:
            start, stop, step = args
        return Array(self.contents[start:stop:step])

    def combinations(self, *args):
        temp = []
        for comb in combinations(self.contents, *convert_to_ints(args)):
            temp.append(Array(list(comb)))
        return Array(temp)
        
    def allcombinations(self):
        temp = []
        for length in range(len(self.contents) +1):
            for subset in combinations(self.contents, length):
                temp.append(Array(list(subset)))
        return Array(list(temp))

    def multicombinations(self, *args):
        temp = []
        if len(args) == 0:
            args = [len(self)]
        for comb in combinations_with_replacement(self.contents, *convert_to_ints(args)):
            temp.append(Array(list(comb)))
        return Array(temp)
    
    def permutations(self):
        temp = []
        for comb in permutations(self.contents):
            temp.append(Array(list(comb)))
        return Array(temp)

    def removeduplicates(self):
        return Array(list(dict.fromkeys(self.convert_to_builtins())))

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

    def difference(self, other):
        for elem in other:
            if elem in self:
                    self.contents.remove(elem)
        return self

    def mostcommon(self, *args):
        c = Counter(self.convert_to_builtins())
        results = []
        args = convert_to_ints(args)
        if len(args) == 0:
            ranking_length = 3
        else:
            ranking_length = args[0]
        for tup in c.most_common(ranking_length):
            results.append(Array(list(tup)))
        return Array(results)

    def count(self, *args):
        ct = 0
        for arg in args:
            ct += self.contents.count(arg)
        return float(ct)
    
    def delete(self):
        del self.contents[self.n[-1]-1]
        self.n = [n-1 for n in self.n]
        self.max -= 1
        return self

    def deleteAt(self, *args):
        for arg in convert_to_ints(args):
            del self.contents[arg]
    
    def pop(self, *args):
        return self.contents.pop(*convert_to_ints(args))
    
    def posof(self, value):
        return self.contents.index(value)

    def remove(self, element):
        self.n[-1] -= 1
        self.max -= 1
        self.contents.remove(element)
        return self

    def replace(self, *args):
        old = args[0]
        new = args[1]
        return Array([new if elem==old else elem for elem in self.contents])

    def join(self, *args):
        delimiter = "" if len(args) == 0 else args[0]
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
    
    def sort(self):
        self.contents.sort()
        return self
    
    def min(self):
        return min(self.contents)

    def max(self):
        return max(self.contents)

    def rev(self):
        self.contents.reverse()
        return self
            

# Defines a function consisting of the arguments and the body
class Function:
    def __init__(self, arguments, body, identifier):
        self.arguments = arguments
        self.body = body
        self.identifier = identifier

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
ARRAYAPPLY_ASSIGN = 51
IN = 52
ITERATE = 53
DEL = 54
LET = 55
COLON = 56
WHILE = 57

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
WhileNode = namedtuple("WhileNode", ["condition", "statements"])
ContainsNode = namedtuple("ContainsNode", ["iterable", "item"])
IterateNode = namedtuple("IterateNode", ["iterable", "items", "statements"])
RangeNode = namedtuple("RangeNode", ["start", "stop", "step"])

# Returns the correct node for operations
OPERATOR_NODE_DICT = {PLUS_SIGN: AddNode, MINUS_SIGN: SubNode, MULT_SIGN: MultNode, DIV_SIGN: DivNode,
                      MODULUS_SIGN: ModulusNode, EQUALS: AssignNode, PLUS_ASSIGN: AddNode, MINUS_ASSIGN: SubNode,
                      MULT_ASSIGN: MultNode, DIV_ASSIGN: DivNode, MODULUS_ASSIGN: ModulusNode, ARRAYAPPLY_ASSIGN: ArrayApplyNode}

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
    DEL: "DEL",
    ARRAYAPPLY_ASSIGN: "ARRAYAPPLY_ASSIGN",
    LET: "LET",
    COLON: "COLON",
    WHILE: "WHILE"
}
