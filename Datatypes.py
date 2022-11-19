from collections import namedtuple, Counter
from itertools import combinations, permutations, combinations_with_replacement

ALPHABET_MAP = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", range(1, 27)))


def convert_to_ints(argument_list):
    return [elem.get_num() if isinstance(elem, Number) else elem for elem in argument_list]


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

#TODO: Let Dataclasses inherit from Python Types


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
        elif isinstance(value, Number):
            self.num = value.num
        else:
            raise ValueError(f"Couldn't convert type {type(value).__name__} to number.")
    
    def __hash__(self):
        return hash(self.num)

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

    def __floordiv__(self, other):
        return Number(self.num // float(other))
    
    def __rfloordiv__(self, other):
        return Number(float(other) // self.num)

    def __mod__(self, other):
        return Number(int(self) % int(other))

    def __rmod__(self, other):
        return Number(int(other) % int(self))

    def pow(self, other):
        return Number(self.num ** float(other))

    def __lt__(self, other):
        return Bool(self.num < float(other))

    def __le__(self, other):
        return Bool(self.num <= float(other))

    def __gt__(self, other):
        return Bool(self.num > float(other))

    def __ge__(self, other):
        return Bool(self.num >= float(other))

    def __bool__(self):
        return False if self.num == 0 else True

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
        self.str = self.str.replace("\#", "#")
        self.str_arr = []
        self.n = []
        self.max = len(self.str)

    def __len__(self):
        return len(self.str)
    
    def __hash__(self):
        return hash(self.str)

    def __str__(self):
        return self.str

    def __repr__(self):
        return "\"" + self.str + "\""

    def clone(self):
        return String(self.str)

    def __bool__(self):
        return False if len(self) == 0 else True

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

    def __add__(self, other):
        return String(str(self) + str(String(other)))

    def __radd__(self, other):
        return String(str(self) + str(String(other)))

    def __lt__(self, other):
        return Bool(self.str < other.str)

    def __le__(self, other):
        return Bool(self.str <= other.str)

    def __gt__(self, other):
        return Bool(self.str > other.str)

    def __ge__(self, other):
        return Bool(self.str >= other.str)

    def __mul__(self, num):
        num = num.get_num()
        if not isinstance(num,int):
            raise TypeError("Cannot multiply strings with floats.")
        self.str *= num
        return self

    def __eq__(self, other):
        return Bool(str(self) == str(other))

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
    
    def enumerate(self):
        return self.n[-1], next(self)

    def numMap(self):
        new = Array([])
        for char in self.str:
            if char.capitalize() in ALPHABET_MAP:
                new += Number(ALPHABET_MAP[char.capitalize()])
            else:
                new += char
        return new
    
    def first(self):
        return self[Number(0)]
    
    def last(self):
        return self[Number(-1)]
    
    def middle(self):
        return self[Number(len(self)//2)]
    
    def at(self, *args):
        return self[Number(args[0])]

    def insert(self, *args):
        arr = Array(list(self.str))
        self.str = str(arr.insert(*args).join())
        return self

    def delete(self):
        del self.str_arr[-1][self.n[-1] - 1]
        self.n = [n - 1 for n in self.n]
        self.max -= 1
        return self

    def deleteAt(self, *args):
        for arg in convert_to_ints(args):
            self.n = [n - 1 for n in self.n]
            self.max -= 1
            if arg<0:
                arg = len(self) + arg
            self.str = self.str[:arg] + self.str[arg + 1:]

    def hasValue(self, value):
        return Bool(value in self)

    def remove(self, *args):
        arr = Array(list(self.str))
        for arg in args:
            arr.remove(arg)
            self.n = [n - 1 for n in self.n]
            self.max -= 1
        self.str = "".join(arr)
        return self

    def removeAll(self, *args):
        arr = Array(list(self.str))
        for arg in args:
            while arg in arr:
                arr.remove(arg)
                self.n = [n-1 for n in self.n]
                self.max -= 1
        self.str = "".join(arr)
        return self

    def pop(self, *args):
        self.n = [n - 1 for n in self.n]
        self.max -= 1
        if len(args) == 0:
            args = [-1]
        elem = self[Number(args[0])]
        self.deleteAt(Number(args[0]))
        return elem

    def find(self, value):
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

    def isUpper(self):
        return Bool(self.str.isupper())

    def isLower(self):
        return Bool(self.str.islower())

    def isCapitalized(self):
        return Bool(self.str.istitle())

    def count(self, *args):
        ct = 0
        for arg in args:
            if not isinstance(arg, String):
                raise TypeError("Expected type String for function count")
            ct += self.str.count(str(arg))
        return Number(ct)

    def mostCommon(self, *args):
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

    def allCombinations(self):
        temp = []
        for length in range(len(self.str) + 1):
            for subset in combinations(self.str, length):
                temp.append(Array([String(elem) for elem in subset]))
        return Array(temp)

    def multiCombinations(self, *args):
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

    def removeDuplicates(self):
        self.contents = [*set(self.contents)]
        return self

    def reverse(self):
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
    
    def startswith(self, arg):
        return Bool(self.str.startswith(str(arg)))
    
    def endswith(self, arg):
        return Bool(self.str.endswith(str(arg)))


class Bool:
    def __init__(self, value=None):
        self.boolean_value = bool(value)

    def __hash__(self):
        return hash(self.boolean_value)

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
        return self


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

    def clone(self):
        return Array(self.contents.copy())

    def __mul__(self, num):
        num = int(num)
        if not isinstance(num,int):
            raise TypeError("Cannot multiply strings with floats.")
        arrcopy = self.contents.copy()
        for _ in range(num-1):
            for elem in arrcopy:
                if isinstance(elem,Array):
                    self.contents.append(elem.clone())
                else:
                    self.contents.append(elem)
        return self

    def __sub__(self, elem):
        elem = [elem] if not isinstance(elem, Array) else elem
        while len(elem) > 0:
            for i in reversed(range(len(self))):
                if self[Number(i)] in elem:
                    elem.remove(self.contents[i])
                    del self.contents[i]
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
        return Bool(elem in self.contents)

    def __setitem__(self, index, val):
        self.contents[index.get_num()] = val
    
    def __bool__(self):
        return False if len(self) == 0 else True

    def enumerate(self):
        return self.n[-1], next(self)
        
    def append(self, *args):
        for arg in args:
            self.contents.append(arg)
        return self

    def first(self):
        return self[Number(0)]
    
    def last(self):
        return self[Number(-1)]
    
    def middle(self):
        return self[Number(len(self)//2)]
    
    def at(self, *args):
        return self[Number(args[0])]
    
    def insert(self, *args):
        self.contents.insert(*args)
        return self
    
    def extend(self, *args):
        for arg in args:
            if not hasattr(arg, '__iter__'):
                raise TypeError(f"{type(arg).__name__} object is not iterable.")
            for elem in arg:
                self += elem
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

    def allCombinations(self):
        temp = []
        for length in range(len(self.contents) + 1):
            for subset in combinations(self.contents, length):
                temp.append(Array(list(subset)))
        return Array(list(temp))

    def multiCombinations(self, *args):
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

    def removeDuplicates(self):
        self.contents = [*set(self.contents)]
        return self

    def intersection(self, *args):
        for arg in args:
            for elem in self:
                if elem not in arg:
                    self.remove(elem)              
        return self

    def union(self, *args):
        for arg in args:
            for elem in arg:
                if elem not in self:
                    self.contents.append(elem)
        return self

    def difference(self, *args):
        for arg in args:
            for elem in arg:
                if elem in self:
                    self.contents.remove(elem)
        return self

    def mostCommon(self, *args):
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
            self.n = [n - 1 for n in self.n]
            self.max -= 1
            del self.contents[arg]
    
    def hasValue(self, value):
        return Bool(value in self)

    def removeAll(self, *args):
        for arg in args:
            while arg in self.contents:
                self.n = [n-1 for n in self.n]
                self.max -= 1
                self.remove(arg)
        return self

    def pop(self, *args):
        self.n = [n - 1 for n in self.n]
        self.max -= 1
        return self.contents.pop(*convert_to_ints(args))

    def find(self, value):
        return Number(self.contents.index(value))

    def remove(self, *args):
        for arg in args:
            self.contents.remove(arg)
            self.n = [n - 1 for n in self.n]
            self.max -= 1
        return self

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
    
    def sorted(self):
        return Array(sorted(self.contents))

    def min(self):
        return Number(min(self.contents))

    def max(self):
        return Number(max(self.contents))

    def reverse(self):
        self.contents.reverse()
        return self

    def all(self):
        return Bool(all([bool(x) for x in self]))
    
    def some(self):
        return Bool(any([bool(x) for x in self]))
    
    def none(self):
        return Bool(not any([bool(x) for x in self]))


class Dictionary:
    def __init__(self, contents):
        self.contents = contents
        self.n = []
        self.max = len(self.contents)

    def __str__(self):
        str = "{"
        for k,v in self.contents.items():
            str += repr(k) + " > " + repr(v) + ", "
        str = str[:-2]
        str+= "}"         
        return str

    def __len__(self):
        return len(self.contents)

    def __iter__(self):
        return iter(Array([Array(list(item)) for item in self.contents.items()]))

    def clone(self):
        return Dictionary(self.contents.copy())

    def __sub__(self, key):
        del self.contents[key]
        return self

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if not isinstance(other, Dictionary):
            raise TypeError(f"Comparison between type Dictionary and type {type(other).__name__} not supported.")
        return Bool(self.contents == other.contents)

    def __getitem__(self, key):
        return self.contents[key]

    def __contains__(self, elem):
        return elem in self.contents

    def __setitem__(self, key, val):
        self.contents[key] = val

    def __bool__(self):
        return False if len(self.contents) == 0 else True

    def delete(self, *keys):
        for key in keys:
            del self.contents[key]

    def pop(self, key):
        self.n = [n-1 for n in self.n]
        self.max -= 1
        return self.contents.pop(key)

    def hasKey(self, key):
        return Bool(key in self.contents.keys())
    
    def hasValue(self, val):
        return Bool(val in self.contents.values())
        
    def get(self, key):
        return self.contents.get(key)

    def keys(self):
        return Array(list(self.contents.keys()))

    def values(self):
        return Array(list(self.contents.values()))

class Class:
    def __init__(self, identifier, constructor=None):
        self.identifier = identifier
        self.constructor = constructor
    
    def __repr__(self):
        return str(self.__dict__)
    
class Instance:
    def __init__(self, instanceof: Class):
        self.instanceof = instanceof


class Function:
    def __init__(self, arglist, body, identifier="Anonymous", is_static=False):
        self.arguments = arglist
        self.body = body
        self.identifier = identifier
        self.is_static = is_static

    def __repr__(self):
        return f"Function {self.identifier} {self.body}"
    
    def __str__(self):
        return repr(self)

class Token:
    def __init__(self, type=None, value=None):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"TOKEN({type_dict.get(self.type)}" + (f", VALUE = {self.value})" if self.value is not None else ")")
    
    def __eq__(self, other):
        return self.type == other.type and self.value == other.value


class IfNode:
    def __init__(self):
        self.blocks = []

    def add_block(self, keyword, body, condition=None):
        self.blocks.append({"keyword": keyword, "condition": condition, "body": body})

    def __repr__(self):
        out = "IfNode("
        for block in self.blocks:
            kw = type_dict.get(block["keyword"])
            condition = block["condition"]
            body = block["body"]
            out += f"[keyword = {kw}, condition = {condition}, body = {body}]"
        out += ")"
        return out


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
BIND = GREATER_THAN
FLOORDIV_SIGN = 59
UNLESS = 60
ITERATE_ARROW = 61
DOUBLE_PERIOD = 62
ANONYMOUS_FUNCTION_KEYWORD = 63
CLASS_KEYWORD = 64
STATIC_FUNCTION_KEYWORD = 65


AddNode = namedtuple("AddNode", ["a", "b"])
SubNode = namedtuple("SubNode", ["a", "b"])
MultNode = namedtuple("MultNode", ["a", "b"])
DivNode = namedtuple("DivNode", ["a", "b"])
FloorDivNode = namedtuple("FloorDivNode", ["a", "b"])
ModulusNode = namedtuple("ModulusNode", ["a", "b"])
ExpNode = namedtuple("ExpNode", ["a", "b"])
AssignNode = namedtuple("AssignNode", ["variable", "value"])
VariableNode = namedtuple("VariableNode", ["identifier"])
FuncCallNode = namedtuple("FuncCallNode", ["variable", "arguments"])
ComparisonNode = namedtuple("ComparisonNode", ["a", "b", "operator"])
BooleanNegationNode = namedtuple("BooleanNegationNode", ["value"])
LogicalOperationNode = namedtuple("LogicalOperationNode", ["a", "b", "operation"])
ForNode = namedtuple("ForNode", ["assignment", "condition", "increment", "statements"])
ReturnNode = namedtuple("ReturnNode", ["statement"])
PrintNode = namedtuple("PrintNode", ["statement"])
SolveNode = namedtuple("SolveNode", ["left_side", "right_side"])
SolveAssignNode = namedtuple("SolveAssignNode", ["left_side", "right_side"])
BracketCallNode = namedtuple("BracketCallNode", ["identifier", "index"])
ArrayApplyNode = namedtuple("ArrayApplyNode", ["identifier", "function"])
IterateNode = namedtuple("IterateNode", ["iterable", "items", "statements"])
RangeNode = namedtuple("RangeNode", ["start", "stop", "step"])
ArrayDeclareNode = namedtuple("ArrayDeclareNode", ["items"])
DictDeclareNode = namedtuple("DictDeclareNode", ["items"])
PostIncrementNode = namedtuple("PostIncrementNode", ["factor", "value"])
StringBuilderNode = namedtuple("StringBuilderNode", ["string", "tokens"])
ClassDeclareNode = namedtuple("ClassDeclareNode", ["identifier", "body"])


DATATYPES = [Array, Number, String, Dictionary, Bool]

OPERATOR_NODE_DICT = {PLUS_SIGN: AddNode, MINUS_SIGN: SubNode, MULT_SIGN: MultNode, DIV_SIGN: DivNode,
                      MODULUS_SIGN: ModulusNode, EQUALS: AssignNode, PLUS_ASSIGN: AddNode, MINUS_ASSIGN: SubNode,
                      MULT_ASSIGN: MultNode, DIV_ASSIGN: DivNode, MODULUS_ASSIGN: ModulusNode,
                      ARRAYAPPLY_ASSIGN: ArrayApplyNode, FLOORDIV_SIGN: FloorDivNode}

STATEMENT_TOKENS = (IF, SOLVE_ASSIGN, SOLVE, ITERATE_ARROW, COMP_EQUALS, COMP_NOT_EQUALS, GREATER_THAN,
                    LESS_THAN, GREATER_OR_EQUALS, LESS_OR_EQUALS, IN)

EXPRESSION_TOKENS = (PLUS_SIGN, MINUS_SIGN)

TERM_TOKENS = (MULT_SIGN, DIV_SIGN, MODULUS_SIGN, EQUALS,
                PLUS_ASSIGN, MINUS_ASSIGN, MULT_ASSIGN,
                DIV_ASSIGN, MODULUS_ASSIGN, ARRAYAPPLY_ASSIGN,
                ARRAYAPPLY, DOUBLE_PERIOD, FLOORDIV_SIGN)
                
EXPONENTIAL_TOKENS = (EXP, DOUBLE_MINUS, DOUBLE_PLUS, LBRACKET, IDENTIFIER, COLON)

OP_ASSIGN_TOKENS = (PLUS_ASSIGN, MINUS_ASSIGN, MULT_ASSIGN, DIV_ASSIGN, MODULUS_ASSIGN, ARRAYAPPLY_ASSIGN)

OPERATOR_DICT = {"+": PLUS_SIGN, "-": MINUS_SIGN, "*": MULT_SIGN, "/": DIV_SIGN,
                 "%": MODULUS_SIGN, "+=": PLUS_ASSIGN, "-=": MINUS_ASSIGN,
                 "*=": MULT_ASSIGN, "/=": DIV_ASSIGN, "%=": MODULUS_ASSIGN,
                 "(": LPAREN, ")": RPAREN, "**": EXP, ",": COMMA,
                 "==": COMP_EQUALS, "!=": COMP_NOT_EQUALS,
                 "<": LESS_THAN, ">": GREATER_THAN, "<=": LESS_OR_EQUALS,
                 ">=": GREATER_OR_EQUALS, "=>": ARROW, "=": EQUALS, "!": NOT,
                 "--": DOUBLE_MINUS, "++": DOUBLE_PLUS, "<<": BLOCK_END,
                 "{": LCURLY, "}": RCURLY, "?=": SOLVE_ASSIGN, "?": SOLVE,
                 "[": LBRACKET, "]": RBRACKET, ">>": ARRAYAPPLY,
                 ">>>": ARRAYAPPLY_ASSIGN, ":": COLON, "//": FLOORDIV_SIGN,
                 "<-": RETURN, "->": ITERATE_ARROW, "..": DOUBLE_PERIOD}
KEYWORD_DICT = {"if": IF, "else": ELSE, "fn": FUNCTION_KEYWORD, "True": TRUE,
                "False": FALSE, "not": NOT, "or": OR, "and": AND,
                "repeat": REP, "as": AS, "for": FOR, "return": RETURN,
                "break": BREAK, "continue": CONTINUE, "in": IN, "iterate": ITERATE,
                "delete": DEL, "let": LET, "equals": COMP_EQUALS,
                "greater": GREATER_THAN, "smaller": LESS_THAN, "while": WHILE,
                "unless": UNLESS, "afn": ANONYMOUS_FUNCTION_KEYWORD, "class": CLASS_KEYWORD,
                "sfn": STATIC_FUNCTION_KEYWORD
                }
            
OXYGEN_DICT = OPERATOR_DICT | KEYWORD_DICT

MACROS = [[[Token(UNLESS)], [Token(IF), Token(NOT)]]]

type_dict = {NUMBER: "NUMBER", PLUS_SIGN: "PLUS_SIGN", MINUS_SIGN: "MINUS_SIGN", MULT_SIGN: "MULT_SIGN",
             DIV_SIGN: "DIV_SIGN", MODULUS_SIGN: "MODULUS_SIGN", PLUS_ASSIGN: "PLUS_ASSIGN",
             MINUS_ASSIGN: "MINUS_ASSIGN", MULT_ASSIGN: "MULT_ASSIGN", DIV_ASSIGN: "DIV_ASSIGN",
             MODULUS_ASSIGN: "MODULUS_ASSIGN", LPAREN: "LPAREN", RPAREN: "RPAREN", IDENTIFIER: "IDENTIFIER",
             EQUALS: "EQUALS", EXP: "EXPONENTIAL_SIGN", ARROW: "ARROW", FUNCTION_KEYWORD: "FUNCTION_KEYWORD",
             COMMA: "COMMA", COMP_EQUALS: "COMP_EQUALS",
             COMP_NOT_EQUALS: "COMP_NOT_EQUALS", GREATER_THAN: "GREATER_THAN", LESS_THAN: "LESS_THAN",
             GREATER_OR_EQUALS: "GREATER_OR_EQUALS", LESS_OR_EQUALS: "LESS_OR_EQUALS", TRUE: "TRUE", FALSE: "FALSE",
             NOT: "NOT", AND: "AND", OR: "OR", IF: "IF", ELSE: "ELSE", REP: "REP", FOR: "FOR", STRING: "STRING", AS: "AS",
             DOUBLE_MINUS: "DOUBLE_MINUS", DOUBLE_PLUS: "DOUBLE_PLUS", BLOCK_END: "BLOCK_END", RETURN: "RETURN",
             LCURLY: "LCURLY", RCURLY: "RCURLY", SOLVE_ASSIGN: "SOLVE_ASSIGN", SOLVE: "SOLVE", LINEBREAK: "LINEBREAK",
             BREAK: "BREAK", CONTINUE: "CONTINUE", LBRACKET: "LBRACKET", RBRACKET: "RBRACKET", ARRAYAPPLY: "ARRAYAPPLY",
             IN: "IN", ITERATE: "ITERATE", DEL: "DEL", ARRAYAPPLY_ASSIGN: "ARRAYAPPLY_ASSIGN", LET: "LET",
             COLON: "COLON", WHILE: "WHILE", FLOORDIV_SIGN: "FLOORDIV_SIGN", UNLESS: "UNLESS", ITERATE_ARROW: "ITERATE_ARROW",
             DOUBLE_PERIOD: "DOUBLE_PERIOD", ANONYMOUS_FUNCTION_KEYWORD: "ANONYMOUS_FUNCTION_KEYWORD", STATIC_FUNCTION_KEYWORD: "STATIC_FUNCTION_KEYWORD"}