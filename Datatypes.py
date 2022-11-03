from collections import namedtuple, Counter
from itertools import combinations, permutations, combinations_with_replacement

ALPHABET_MAP = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", range(1, 27)))


def convert_to_ints(arglist):
    return [elem.get_num() if isinstance(elem, Number) else elem for elem in arglist]


def convert_to_builtin(arg):
    if isinstance(arg, Array):
        return arg.contents
    elif isinstance(arg, String):
        return arg.str
    elif isinstance(arg, Bool):
        return arg.boolean_value
    elif isinstance(arg, Number):
        return arg.get_num()
    else:
        return arg


class Number:
    def __init__(self, value):
        if isinstance(value, int) or isinstance(value, float) or isinstance(value, str):
            self.num = float(value)
        elif isinstance(value, Bool):
            if Bool:
                self.num = 1
            else:
                self.num = 0
        elif isinstance(value, String):
            self.num = float(value.str)
        else:
            raise ValueError(f"Couldn't convert type {type(value).__name__} to number.")

    def __add__(self, other):
        return Number(self.num + float(other))

    def __radd__(self, other):
        return Number(self.num + float(other))

    def __sub__(self, other):
        return Number(self.num - float(other))

    def __rsub__(self, other):
        return Number(float(other) - self.num)

    def __mul__(self, other):
        return Number(self.num * float(other))

    def __rmul__(self, other):
        return Number(self.num * float(other))

    def __truediv__(self, other):
        return Number(self.num / float(other))

    def __rtruediv__(self, other):
        return Number(float(other) / self.num)

    def __mod__(self, other):
        return Number(int(self) % int(other))

    def __rmod__(self, other):
        return Number(int(other) % int(self))

    def pow(self, other):
        return Number(self.num ** float(other))

    def __lt__(self, other):
        return self.num < float(other)

    def __le__(self, other):
        return self.num <= float(other)

    def __gt__(self, other):
        return self.num > float(other)

    def __ge__(self, other):
        return self.num >= float(other)

    def __bool__(self):
        return Bool(self)

    def __len__(self):
        return len(str(self.num))

    def __str__(self):
        return str(self.get_num())

    def __repr__(self):
        return str(self)

    def __int__(self):
        return int(self.num)

    def get_num(self):
        if self.num % 1 == 0:
            return int(self.num)
        else:
            return self.num

    def __float__(self):
        return float(self.num)

    def __eq__(self, other):
        return self.num == float(other)


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
        self.max = len(self.str)

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
        num = num.get_num()
        if num < 1:
            raise TypeError("Cannot divide arrays.")
        self.str *= num
        return self

    def __eq__(self, other):
        return str(self) == str(other)

    def __getitem__(self, index):
        return String(self.str[index.get_num()])

    def __setitem__(self, index, val):
        lst = list(self.str)
        try:
            lst[index.get_num()] = str(String(val))
        except IndexError:
            pass
        self.str_arr[-1][index.get_num()] = str(String(val))
        self.str = "".join(lst)

    def slice(self, *args):
        args = convert_to_ints(args)
        if len(args) == 1:
            stop = args[0]
            start = 0
            step = 1
        elif len(args) == 2:
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
                new += Number(ALPHABET_MAP[char.capitalize()])
            else:
                new += char
        return new

    def delete(self):
        del self.str_arr[-1][self.n[-1] - 1]
        self.n[-1] -= 1
        self.max -= 1
        return self

    def deleteAt(self, *args):
        for arg in convert_to_ints(args):
            del self.str[arg]

    def remove(self, *args):
        arr = Array(list(self.str))
        for arg in args:
            for arg in args:
                arr.remove(arg)
                self.n = [n - 1 for n in self.n]
                self.max -= 1
        self.str = "".join(arr)
        return self

    def removeall(self, *args):
        for arg in args:
            while arg in self:
                self.remove(arg)
        return self

    def pop(self, *args):
        return self.contents.pop(*convert_to_ints(args))

    def posof(self, value):
        return Number(self.str.index(str(value)))

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
        return Number(ct)

    def mostcommon(self, *args):
        c = Counter(list([str(s) for s in self.str]))
        results = []
        args = convert_to_ints(args)
        if len(args) == 0:
            ranking_length = 3
        else:
            ranking_length = args[0]
        for tup in c.most_common(ranking_length):
            results.append(Array([String(tup[0]), Number(tup[1])]))
        return Array(results)

    def combinations(self, *args):
        temp = []
        for comb in combinations(self.str, *convert_to_ints(args)):
            temp.append(Array([String(elem) for elem in comb]))
        return Array(temp)

    def allcombinations(self):
        temp = []
        for length in range(len(self.str) + 1):
            for subset in combinations(self.str, length):
                temp.append(Array([String(elem) for elem in subset]))
        return Array(temp)

    def multicombinations(self, *args):
        temp = []
        if len(args) == 0:
            args = [len(self)]
        for comb in combinations_with_replacement(self.str, *convert_to_ints(args)):
            temp.append(Array([String(elem) for elem in comb]))
        return Array(temp)

    def permutations(self):
        temp = []
        for comb in permutations(self.str):
            temp.append(Array([String(elem) for elem in comb]))
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
        elif isinstance(value, Number):
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
        self.max = len(self.contents)

    def __str__(self):
        if len(self) == 0:
            return "[]"
        res = "["
        for c in self.contents:
            res += repr(c) + ", "
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
        return Array(self.contents.copy() + [elem])

    def copy(self):
        return Array(self.contents.copy())

    def __mul__(self, num):
        num = int(num)
        if num < 1:
            raise TypeError("Cannot divide arrays.")
        self.contents *= num
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
                if v != other[Number(i)]:
                    eq = False
            return Bool(eq)
        except TypeError:
            raise TypeError(f"{type(other).__name__} object is not iterable.")

    def __getitem__(self, index):
        return self.contents[index.get_num()]

    def __contains__(self, elem):
        return elem in self.contents

    def __setitem__(self, index, val):
        self.contents[index.get_num()] = val

    def append(self, *args):
        for arg in args:
            self += arg
        return self

    def convert_to_builtins(self):
        new = []
        for element in self.contents:
            new.append(convert_to_builtin(element))
        return new

    def slice(self, *args):
        args = convert_to_ints(args)
        if len(args) == 1:
            stop = args[0]
            start = 0
            step = 1
        elif len(args) == 2:
            start, stop = args
            step = 1
        else:
            start, stop, step = args
        return Array(self.contents[start:stop:step])

    def flatten(self):
        new = Array([])
        for elem in self.contents:
            if isinstance(elem, Array):
                for item in elem.flatten():
                    new += item
            else:
                new += elem
        return new

    def combinations(self, *args):
        temp = []
        for comb in combinations(self.contents, *convert_to_ints(args)):
            temp.append(Array(list(comb)))
        return Array(temp)

    def allcombinations(self):
        temp = []
        for length in range(len(self.contents) + 1):
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
            results.append(Array([String(tup[0]), Number(tup[1])]))
        return Array(results)

    def count(self, *args):
        ct = 0
        for arg in args:
            ct += self.contents.count(arg)
        return Number(ct)

    def delete(self):
        del self.contents[self.n[-1] - 1]
        self.n = [n - 1 for n in self.n]
        self.max -= 1
        return self

    def deleteAt(self, *args):
        for arg in convert_to_ints(args):
            del self.contents[arg]

    def removeall(self, *args):
        for arg in args:
            while arg in self.contents:
                self.remove(arg)
        return self

    def pop(self, *args):
        return self.contents.pop(*convert_to_ints(args))

    def posof(self, value):
        return Number(self.contents.index(value))

    def remove(self, *args):
        for arg in args:
            self.contents.remove(arg)
            self.n = [n - 1 for n in self.n]
            self.max -= 1
        return self

    # def flatten(self):
    #    
    #    for elem in self:

    def replace(self, *args):
        old = args[0]
        new = args[1]
        return Array([new if elem == old else elem for elem in self.contents])

    def join(self, *args):
        delimiter = "" if len(args) == 0 else args[0]
        return String(str(delimiter).join([str(s) for s in self.contents]))

    def sum(self):
        s = 0
        for el in self.contents:
            if isinstance(el, Number):
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


class Dictionary():
    def __init__(self, contents):
        self.contents = contents
        self.n = []
        self.max = len(self.contents)

    def __str__(self):
        return str(self.contents)

    def __len__(self):
        return len(self.contents)

    def __iter__(self):
        return iter(Array([Array(list(item)) for item in self.contents.items()]))

    def copy(self):
        return Dictionary(self.contents.copy())

    def __sub__(self, key):
        del self.contents[key]
        return self

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, Dictionary):
            raise TypeError(f"Comparison between type Dictionary and type {type(other).__name__} not supported.")
        return Bool(self.contents == other.contents)

    def __getitem__(self, key):
        return self.contents[convert_to_builtin(key)]

    def __contains__(self, elem):
        return convert_to_builtin(elem) in self.contents

    def __setitem__(self, key, val):
        self.contents[convert_to_builtin(key)] = val

    def delete(self, *keys):
        for key in keys:
            del self.contents[convert_to_builtin(key)]

    def pop(self, key):
        return self.contents.pop(convert_to_builtin(key))

    def keys(self):
        return Array(list(self.contents.keys()))

    def values(self):
        return Array(list(self.contents.values()))


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
BIND = 58

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
BracketCallNode = namedtuple("BracketCallNode", ["identifier", "index"])
ArrayApplyNode = namedtuple("ArrayApplyNode", ["identifier", "function"])
PeriodCallNode = namedtuple("PeriodCallNode", ["left_side", "right_side"])
WhileNode = namedtuple("WhileNode", ["condition", "statements"])
ContainsNode = namedtuple("ContainsNode", ["iterable", "item"])
IterateNode = namedtuple("IterateNode", ["iterable", "items", "statements"])
RangeNode = namedtuple("RangeNode", ["start", "stop", "step"])
DictCreateNode = namedtuple("DictCreateNode", ["items"])

# Returns the correct node for operations
OPERATOR_NODE_DICT = {PLUS_SIGN: AddNode, MINUS_SIGN: SubNode, MULT_SIGN: MultNode, DIV_SIGN: DivNode,
                      MODULUS_SIGN: ModulusNode, EQUALS: AssignNode, PLUS_ASSIGN: AddNode, MINUS_ASSIGN: SubNode,
                      MULT_ASSIGN: MultNode, DIV_ASSIGN: DivNode, MODULUS_ASSIGN: ModulusNode,
                      ARRAYAPPLY_ASSIGN: ArrayApplyNode}

# Debug
# Helps to make tokens more readable
type_dict = {NUMBER: "NUMBER", PLUS_SIGN: "PLUS_SIGN", MINUS_SIGN: "MINUS_SIGN", MULT_SIGN: "MULT_SIGN",
    DIV_SIGN: "DIV_SIGN", MODULUS_SIGN: "MODULUS_SIGN", PLUS_ASSIGN: "PLUS_ASSIGN", MINUS_ASSIGN: "MINUS_ASSIGN",
    MULT_ASSIGN: "MULT_ASSIGN", DIV_ASSIGN: "DIV_ASSIGN", MODULUS_ASSIGN: "MODULUS_ASSIGN", LPAREN: "LPAREN",
    RPAREN: "RPAREN", IDENTIFIER: "IDENTIFIER", EQUALS: "EQUALS", EXP: "EXPONENTIAL_SIGN", ARROW: "ARROW",
    FUNCTION_KEYWORD: "FUNCTION_KEYWORD", PERIOD_CALL: "PERIOD_FUNC_CALL", COMMA: "COMMA", COMP_EQUALS: "COMP_EQUALS",
    COMP_NOT_EQUALS: "COMP_NOT_EQUALS", GREATER_THAN: "GREATER_THAN", LESS_THAN: "LESS_THAN",
    GREATER_OR_EQUALS: "GREATER_OR_EQUALS", LESS_OR_EQUALS: "LESS_OR_EQUALS", TRUE: "TRUE", FALSE: "FALSE", NOT: "NOT",
    AND: "AND", OR: "OR", IF: "IF", ELSE: "ELSE", REP: "REP", FOR: "FOR", STRING: "STRING", AS: "AS",
    DOUBLE_MINUS: "DOUBLE_MINUS", DOUBLE_PLUS: "DOUBLE_PLUS", BLOCK_END: "BLOCK_END", RETURN: "RETURN",
    LCURLY: "LCURLY", RCURLY: "RCURLY", SOLVE_ASSIGN: "SOLVE_ASSIGN", SOLVE: "SOLVE", LINEBREAK: "LINEBREAK",
    BREAK: "BREAK", CONTINUE: "CONTINUE", LBRACKET: "LBRACKET", RBRACKET: "RBRACKET", ARRAYAPPLY: "ARRAYAPPLY",
    IN: "IN", ITERATE: "ITERATE", DEL: "DEL", ARRAYAPPLY_ASSIGN: "ARRAYAPPLY_ASSIGN", LET: "LET", COLON: "COLON",
    WHILE: "WHILE", BIND: "BIND"}
