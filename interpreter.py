import builtins
import math
import numpy as np
from matplotlib import pyplot as plt
import Datatypes
import builtinfunctions
import equation_solver

BUILTIN_EXPECTED_ARGS = {"sin": [1], "cos": [1], "tan": [1], "asin": [1], "acos": [1], "atan": [1], "abs": [1],
                         "sqrt": [1], "factorial": [1], "bool": [1], "plot": [3, 4], "out": range(1, 100),
                         "midnight": [3], "rick": [0], "leet": [1], "type": [1], "asArr": [1], "apply": [2],
                         "append": range(2,100), "union": range(2,100), "intersection": range(2,100), "size": [1], "join": [0, 1], 
                         "sum": [1], "slice": [2, 3, 4], "openURL": [1], "min": [1], "max": [1],
                         "asString": [1], "split": [1, 2], "asNum": [1], "difference": range(2, 100),
                         "count": range(2, 100), "numMap": [1], "lower": [1], "upper": [1], "capitalize": [1],
                         "strip": [1, 2], "replace": [3], "isUpper": [1], "isLower": [1], "isCapitalized": [1],
                         "input": [0], "sort": [1], "find": [2], "combinations": [2], "allCombinations": [1],
                         "permutations": [1], "mostCommon": [1, 2], "multiCombinations": [1, 2],
                         "removeDuplicates": [1], "range": [1, 2, 3], "deleteAt": range(2, 100), "pop": [1, 2],
                         "getFields": [0, 1], "quit": [0], "removeAll": range(2, 100), "remove": range(2, 100),
                         "keys": [1], "values": [1], "flatten": [1], "getScope": [0], "clone": [1], "select": [2],
                         "divMod": [2], "change": [2], "macro": [2], "first": [1], "last": [1], "middle": [1],
                         "at": [2], "insert": [3], "get": [2], "sorted": [1], "all": [1], "some": [1], "none": [1],
                         "startswith": [2], "endswith": [2], "format": range(2, 100), "extend": [2], "repr": [1],
                         "findseq": [2], "detect": [2], "foreach": [2], "arrOf" : range(0,100), "fill": [2], 
                         "every": [2], "reverse": [1], "hasKey": [2], "hasValue": [2]
                         }

MATH_KEYWORDS = ["sin", "cos", "tan", "asin", "acos", "atan", "sqrt", "factorial"]
INTERNAL_KEYWORDS = ["out", "apply", "select", "plot", "getFields", "getScope", "detect", "foreach", "every"]
BUILTIN_KEYWORDS_WITHOUT_PROCESSING = ["asArr", "bool", "type", "quit", "rick", "input", "size", "asString", "repr", "arrOf"]
BUILTIN_KEYWORDS = ["midnight", "leet", "range", "asNum", "openURL", "abs", "divMod", "change", "macro", "fill"]
OBJECT_KEYWORDS = [k for k in BUILTIN_EXPECTED_ARGS if k not in (MATH_KEYWORDS + INTERNAL_KEYWORDS + BUILTIN_KEYWORDS)]

OPERATIONAL_NODES = ["AddNode", "SubNode", "MultNode", "DivNode", "ModulusNode", "ExpNode", "FloorDivNode"]

BUILT_IN_FIELDS = {"PI": Datatypes.Number(math.pi), "E": Datatypes.Number(math.e),
                   "GOLDEN": Datatypes.Number((1 + 5 ** 0.5) / 2), "H": Datatypes.Number(6.62607004 * (10 ** (-34))),
                   "ALPHABET": Datatypes.String("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"),
                   "NUMBERS": Datatypes.String("1234567890")}


def standardize(val):
    if isinstance(val, list):
        return val
    else:
        return [val]


def merge(output_list, list_to_append):
    for item in list_to_append:
        if item is not None:
            output_list.append(item)


def process_nums(argument_list):
    new = []
    for argument in argument_list:
        if isinstance(argument, Datatypes.Number):
            new.append(argument.get_num())
        else:
            new.append(argument)
    return new


def stringify(elem):
    if isinstance(elem, Datatypes.Number):
        elem = elem.get_num()
    if not isinstance(elem, (type(None), Datatypes.Function)):
        return repr(elem)


def convert_to_builtins(argument_list):
    return list(Datatypes.Array(argument_list).convert_to_builtins())


class Interpreter:
    def __init__(self, autoid=False):
        self.fields = {"global": BUILT_IN_FIELDS.copy()}
        self.backup_fields = {}
        self.scope = "global"
        self.output_lines = []
        self.autoid = autoid
        #self.lemmatizer = WordNetLemmatizer()

    def get_output(self, ast_list, printall=True):
        self.output_lines = []
        for ast in ast_list:
            out = standardize(self.evaluate(ast))
            out = [stringify(o) for o in out if o is not None]
            if printall:
                merge(self.output_lines, out)
        out = self.output_lines
        self.output_lines = []
        return out

    def evaluate(self, node):
        match type(node).__name__:
            case "FuncDeclareNode":
                self.evaluate(Datatypes.AssignNode(Datatypes.VariableNode(node.identifier), Datatypes.Function(node.arguments, node.body, node.identifier))) 
                if node.identifier in BUILTIN_EXPECTED_ARGS:
                    return Datatypes.String(f"Warning: Built-in function {node.identifier} has been overridden.")
                return Datatypes.Function(node.arguments, node.body, node.identifier)
            case "FuncCallNode":
                if isinstance(node.variable, Datatypes.FuncCallNode):
                    return self.evaluate(
                        Datatypes.FuncCallNode(node.variable.variable, [*node.arguments, *node.variable.arguments]))
                if node.variable.identifier in BUILTIN_EXPECTED_ARGS:
                    return self.builtin_handler(node)
                return self.function_call_handler(self.evaluate(node.variable), node)
            case name if name in OPERATIONAL_NODES:
                return self.operation_handler(node)
            case "AssignNode":
                assignment_value = self.evaluate(node.value)
                if isinstance(node.variable, Datatypes.BracketCallNode):
                    last_index = node.variable.index.pop()
                    arr = self.evaluate(node.variable)
                    arr[self.evaluate(last_index)] = assignment_value
                    node.variable.index.append(last_index)
                elif isinstance(node.variable.identifier, str):
                    global_value = self.fields["global"].get(node.variable.identifier)
                    super_scope = None
                    temp = self.scope.split(" >> ")
                    funcpath = " >> ".join(temp[:-1]) + " >> " if len(temp) > 1 else ""
                    super_scopes = temp[-1].split(" > ")
                    while len(super_scopes) > 0:
                        scope = funcpath + " > ".join(super_scopes)
                        result = self.fields[scope].get(node.variable.identifier)
                        if result is not None:
                            super_scope = scope
                            break
                        super_scopes.pop()
                    if super_scope is not None:
                        self.fields[super_scope][node.variable.identifier] = assignment_value
                    elif global_value is not None:
                        self.fields["global"][node.variable.identifier] = assignment_value
                    else:
                        self.fields[self.scope][node.variable.identifier] = assignment_value
                else:
                    raise SyntaxError(f"Cannot assign to type {type(node.variable.identifier).__name__}")
                return assignment_value
            case "SolveNode":
                _, expression = equation_solver.solve(node.left_side, node.right_side)
                return self.evaluate(expression)
            case "SolveAssignNode":
                variable, expression = equation_solver.solve(node.left_side, node.right_side)
                result = self.evaluate(expression)
                return self.evaluate(Datatypes.AssignNode(variable, result))
            case "BracketCallNode":
                arr = self.evaluate(node.identifier)
                for index in node.index:
                    if isinstance(index, Datatypes.RangeNode):
                        arr = arr.slice(self.evaluate(index.start), self.evaluate(index.stop), self.evaluate(index.step))
                    else:
                        arr = arr[self.evaluate(index)]
                return arr
            case "PostIncrementNode":
                pre_assignment_value = self.evaluate(node.factor)
                self.evaluate(Datatypes.AssignNode(node.factor, Datatypes.AddNode(node.factor, node.value)))
                return pre_assignment_value
            case "ArrayApplyNode":
                arr = self.evaluate(node.identifier).clone()
                if not hasattr(arr, "__iter__"):
                    raise TypeError(f"Element of type {type(arr).__name__} is not iterable.")
                if self.autoid:
                    singular = builtinfunctions.singularize(node.identifier, arr)
                    if singular:
                        ids = ["x", singular]
                    else:
                        ids = ["x"]
                else:
                    ids = ["x"]
                args = ids + ["i", "self"]
                for i, elem in enumerate(arr):
                    if len(args) == 3:
                        res = self.evaluate(Datatypes.FuncCallNode(Datatypes.Function(args, node.function), [elem, Datatypes.Number(i), arr]))
                    else:
                        res = self.evaluate(Datatypes.FuncCallNode(Datatypes.Function(args, node.function), [elem, elem, Datatypes.Number(i), arr]))
                    if isinstance(res, list):
                        if len(res) == 0:
                            continue
                        elif isinstance(res[0], Datatypes.Token) and res[0].type == Datatypes.DEL:
                            arr.delete()
                        else:
                            arr[Datatypes.Number(i)] = res[0]
                    else:
                        if isinstance(res, Datatypes.Token) and res.type == Datatypes.DEL:
                            arr.delete()
                        else:
                            arr[Datatypes.Number(i)] = res
                return arr
            case "ComparisonNode":
                return self.comparison_handler(node)
            case "BooleanNegationNode":
                boolean = self.evaluate(node.value)
                custom_bool = Datatypes.Bool(boolean)
                custom_bool.reverse()
                return custom_bool
            case "LogicalOperationNode":
                if node.operation == Datatypes.AND:
                    return Datatypes.Bool(
                        Datatypes.Bool(self.evaluate(node.a)) and Datatypes.Bool(self.evaluate(node.b)))
                else:
                    return Datatypes.Bool(
                        Datatypes.Bool(self.evaluate(node.a)) or Datatypes.Bool(self.evaluate(node.b)))
            case "IfNode":
                out = []
                results = []
                for block in node.blocks:
                    if (block["keyword"] in (Datatypes.IF, Datatypes.OR) and bool(self.evaluate(block["condition"]))) or \
                            block["keyword"] == Datatypes.ELSE:
                        results = standardize(block["body"])
                        break
                for statement in results:
                    line = standardize(self.evaluate(statement))
                    merge(out, line)
                    if "__return__" in self.fields[self.scope] or "__continue__" in self.fields[self.scope] \
                            or "__break__" in self.fields[self.scope]:
                        break
                if len(out) == 1:
                    return out[0]
                return out
            case "VariableNode":
                global_value = self.fields["global"].get(node.identifier)
                super_value = None
                temp = self.scope.split(" >> ")
                funcpath = " >> ".join(temp[:-1]) + " >> " if len(temp) > 1 else ""
                super_scopes = temp[-1].split(" > ")
                while len(super_scopes) > 0:
                    result = self.fields[funcpath + " > ".join(super_scopes)].get(node.identifier)
                    if result is not None:
                        super_value = result
                        break
                    super_scopes.pop()
                if super_value is not None:
                    result = super_value
                elif global_value is not None:
                    result = global_value
                elif node.identifier in BUILTIN_EXPECTED_ARGS:
                    result = Datatypes.VariableNode(node.identifier)
                else:
                    raise NameError(f"Name \"{node.identifier}\" is not defined.")
                return result
            case "ForNode":
                out = []
                self.scope = self.scope + " > ForLoop"
                self.fields[self.scope] = {}
                self.evaluate(node.assignment)
                while bool(self.evaluate(node.condition)):
                    for statement in node.statements:
                        lines = standardize(self.evaluate(statement))
                        merge(out, lines)
                        if "__break__" in self.fields[self.scope] or "__continue__" in self.fields[self.scope]:
                            break
                        if "__return__" in self.fields[self.scope]:
                            return out
                    if "__break__" in self.fields[self.scope]:
                        self.fields[self.scope].pop("__break__")
                        break
                    elif "__continue__" in self.fields[self.scope]:
                        self.fields[self.scope].pop("__continue__")
                    self.evaluate(node.increment)
                self.fields.pop(self.scope)
                self.scope = " > ".join(self.scope.split(" > ")[:-1])
                return out
            case "IterateNode":
                out = []
                iterable = self.evaluate(node.iterable)
                if len(node.items) == 2:
                    ids = [node.items[1]]
                    index_id = node.items[0]
                elif len(node.items) == 1:
                    ids = [node.items[0]]
                    index_id = "itercounter"
                else:
                    if self.autoid:
                        singular = builtinfunctions.singularize(node.iterable, iterable)
                        if singular:
                            ids = ["iterelem", singular]
                        else:
                            ids = ["iterelem"]
                    else:
                        ids = ["iterelem"]
                    index_id = "itercounter"
                self.scope = self.scope + " > IterLoop"
                self.fields[self.scope] = {}
                for i, element in enumerate(iterable):
                    for id in ids:
                        self.evaluate(Datatypes.AssignNode(Datatypes.VariableNode(id), element))
                    self.evaluate(Datatypes.AssignNode(Datatypes.VariableNode(index_id), Datatypes.Number(i)))
                    for statement in node.statements:
                        lines = standardize(self.evaluate(statement))
                        merge(out, lines)
                        if "__break__" in self.fields[self.scope] or "__continue__" in self.fields[self.scope]:
                            break
                        if "__return__" in self.fields[self.scope]:
                            return out
                    if "__break__" in self.fields[self.scope]:
                        self.fields[self.scope].pop("__break__")
                        break
                    elif "__continue__" in self.fields[self.scope]:
                        self.fields[self.scope].pop("__continue__")
                self.fields.pop(self.scope)
                self.scope = " > ".join(self.scope.split(" > ")[:-1])
                return out
            case "RangeNode":
                return Datatypes.Array([Datatypes.Number(num) for num in np.arange(
                    self.evaluate(node.start),
                    self.evaluate(node.stop),
                    self.evaluate(node.step)
                )])
            case "ReturnNode":
                if self.scope == "global":
                    raise SyntaxError("Return statement outside function")
                self.fields[self.scope]["__return__"] = self.evaluate(node.statement)
            case "ArrayCreateNode":
                new_arr = Datatypes.Array(node.items.copy())
                for i, elem in enumerate(new_arr):
                    new_arr[Datatypes.Number(i)] = self.evaluate(elem)
                return new_arr
            case "DictCreateNode":
                new_dict = Datatypes.Dictionary({})
                for item in node.items:
                    new_dict[self.evaluate(item[0])] = self.evaluate(item[1])
                return new_dict
            case "StringBuilderNode":
                tokens = node.tokens.copy()
                if len(tokens) == 0:
                    return Datatypes.String(node.string)
                strarr = node.string.split("#")
                new_string = ""
                for elem in strarr:
                    new_string += elem
                    if len(tokens) > 0:
                        new_string += str(self.evaluate(tokens.pop(0)))
                return Datatypes.String(new_string)
            case _:
                return node

    def rollback(self):
        self.fields = self.backup_fields
        self.scope = "global"
        self.output_lines = []

    def function_call_handler(self, func, node, optional_funcargs=dict()):
        delimiter = " > " if func.identifier == "Anonymous" else " >> "
        if not isinstance(func, Datatypes.Function):
            raise TypeError(f"{builtins.type(node).__name__} object is not callable")
        arguments = node.arguments
        if len(arguments) != len(func.arguments):
            raise TypeError(
                f"Expected {len(func.arguments)} arguments for function {func.identifier}, got {len(arguments)}.")
        new_function_scope = self.scope + delimiter + func.identifier
        self.fields[new_function_scope] = {}
        reached_kwargs = False
        for i, argument in enumerate(arguments):
            if isinstance(argument, Datatypes.AssignNode) and type(argument.value) not in (Datatypes.AddNode, Datatypes.SubNode):
                reached_kwargs = True
                if argument.variable.identifier in func.arguments:
                    self.fields[new_function_scope][argument.variable.identifier] = self.evaluate(argument.value)
                else:
                    raise TypeError(f"Function argument {argument.identifier} not found in function {func.identifier}.")
            elif reached_kwargs:
                raise SyntaxError("Positional arguments are not allowed after keyword arguments.")
            else:
                self.fields[new_function_scope][func.arguments[i]] = self.evaluate(argument)
        for k, v in optional_funcargs.items():
            self.fields[new_function_scope][k] = v
        self.scope = new_function_scope
        returned_result = None
        if isinstance(func.body, list):
            for statement in func.body:
                self.evaluate(statement)
                if "__return__" in self.fields[self.scope]:
                    returned_result = self.fields[self.scope]["__return__"]
                    if isinstance(returned_result, list) and len(returned_result) > 0:
                        returned_result = returned_result[0]
                    break
        else:
            returned_result = self.evaluate(func.body)
        self.fields.pop(self.scope)
        self.scope = delimiter.join(self.scope.split(delimiter)[:-1])
        return returned_result

    def builtin_handler(self, node):
        keyword = node.variable.identifier
        args = [self.evaluate(arg) for arg in node.arguments]
        arg_count = len(node.arguments)
        expected_arg_count = BUILTIN_EXPECTED_ARGS[keyword]
        if arg_count not in expected_arg_count:
            if len(expected_arg_count) == 1:
                raise TypeError(f"Expected {expected_arg_count[0]} arguments for function {keyword}, got {arg_count}.")
            else:
                TypeError(
                    f"Expected at least {expected_arg_count[0]} arguments for function {keyword}, got {arg_count}.")
        if keyword in INTERNAL_KEYWORDS:
            return getattr(Interpreter, keyword)(self, *args)
        elif keyword in BUILTIN_KEYWORDS:
            return getattr(builtinfunctions, keyword)(*convert_to_builtins(args))
        elif keyword in BUILTIN_KEYWORDS_WITHOUT_PROCESSING:
            return getattr(builtinfunctions, keyword)(*args)
        elif keyword in MATH_KEYWORDS:
            return Datatypes.Number(getattr(math, keyword)(*process_nums(args)))
        else:
            return getattr(builtins.type(args[0]), keyword)(*process_nums(args))

    def operation_handler(self, node):
        node_type = type(node).__name__
        a = self.evaluate(node.a)
        b = self.evaluate(node.b)
        try:
            match node_type:
                case "AddNode":
                    return a + b
                case "SubNode":
                    return a - b
                case "MultNode":
                    return a * b
                case "DivNode":
                    return a / b
                case "ModulusNode":
                    return a % b
                case "ExpNode":
                    return a.pow(b)
                case "FloorDivNode":
                    return a // b
        except TypeError:
            raise TypeError(
                f"Cannot use this mathematical operation on object of type {type(a)} and {type(b)}")

    def comparison_handler(self, node):
        if isinstance(node.a, Datatypes.ComparisonNode):
            return self.evaluate(
                Datatypes.LogicalOperationNode(node.a, Datatypes.ComparisonNode(node.a.b, node.b, node.operator),
                                               Datatypes.AND))
        a = self.evaluate(node.a)
        b = self.evaluate(node.b)
        operator = node.operator
        if isinstance(a, Datatypes.Bool):
            a = bool(a)
        if isinstance(b, Datatypes.Bool):
            b = bool(b)
        match operator:
            case Datatypes.COMP_EQUALS:
                result = Datatypes.Bool(a == b)
            case Datatypes.COMP_NOT_EQUALS:
                result = Datatypes.Bool(a != b)
            case Datatypes.GREATER_THAN:
                result = Datatypes.Bool(a > b)
            case Datatypes.LESS_THAN:
                result = Datatypes.Bool(a < b)
            case Datatypes.GREATER_OR_EQUALS:
                result = Datatypes.Bool(a >= b)
            case Datatypes.LESS_OR_EQUALS:
                result = Datatypes.Bool(a <= b)
            case Datatypes.IN:
                result = Datatypes.Bool(a in b)
            case _:
                raise Exception("An unknown error occurred")
        return result

    def plot(self, function, lower_rng=-5, upper_rng=5, increment=0.001):
        if increment < 0.0001:
            raise ValueError("Plotting increment can not be less than 0.0001")
        args = np.arange(lower_rng, upper_rng, increment)
        try:
            func_args = np.array(
                [self.evaluate(Datatypes.FuncCallNode(function, [arg])) for arg in args])
        except TypeError:
            raise TypeError("Only functions with exactly one argument can be plotted.")
        plt.rcParams["figure.autolayout"] = True
        plt.grid(visible=True, which="major", axis="both")
        plt.plot(args, func_args, c="orange", label=f"f(x)={function.identifier}(x)")
        plt.axvline(x=0)
        plt.axhline(y=0)
        plt.legend()
        plt.show()

    def out(self, *args):
        lines = []
        for arg in args:
            if not isinstance(arg, (type(None), Datatypes.Function)):
                lines.append(arg)
        if len(lines) == 0:
            return
        out = ""
        for line in lines:
            out += str(*process_nums([line])).replace(r"\n", "\n") + " "
        out = [out.strip()]
        merge(self.output_lines, out)
        return

    def apply(self, *args):
        for i, elem in enumerate(args[0]):
            res = self.evaluate(Datatypes.FuncCallNode(args[1], [elem]))
            if isinstance(res, list):
                args[0][Datatypes.Number(i)] = res[0]
            else:
                args[0][Datatypes.Number(i)] = res
        return args[0]
    
    def select(self, *args):
        new = args[0].clone()
        for elem in new:
            res = self.evaluate(Datatypes.FuncCallNode(args[1], [elem]))
            if isinstance(res, list):
                res = res[0]
            if not Datatypes.Bool(res):
                new.delete()
        return new
    
    def detect(self, *args):
        for i, elem in enumerate(args[0]):
            res = self.evaluate(Datatypes.FuncCallNode(args[1], [elem]))
            if isinstance(res, list):
                res = res[0]
            if Datatypes.Bool(res):
                return args[0][Datatypes.Number(i)]
        return None
    
    def every(self, *args):
        return self.apply(args[0].clone(), args[1]).all()
    
    def foreach(self, *args):
        out = []
        for elem in args[0]:
            lines = standardize(self.evaluate(Datatypes.FuncCallNode(args[1], [elem])))
            merge(out, lines)
        return out

    def getFields(self, *args):
        dict = Datatypes.Dictionary({})
        if len(args) == 1:
            for k, v in self.fields[args[0]].items():
                dict[Datatypes.String(k)] = v
            return dict
        for k, v in self.fields.items():
            dict[Datatypes.String(k)] = Datatypes.Dictionary({})
            for i,j in v.items(): 
                dict[Datatypes.String(k)][Datatypes.String(i)] = j
        return dict
    
    def getScope(self):
        return Datatypes.String(self.scope)
