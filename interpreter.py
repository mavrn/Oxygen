import builtins
import math

import numpy as np
from matplotlib import pyplot as plt

import Datatypes
import builtinfunctions
import equation_solver

BUILTIN_EXPECTED_ARGS = {"sin": [1], "cos": [1], "tan": [1], "asin": [1], "acos": [1], "atan": [1], "abs": [1],
                         "sqrt": [1], "factorial": [1], "bool": [1], "plot": [3, 4], "p": range(1, 100),
                         "midnight": [3], "rick": [0], "leet": [1], "type": [1], "arr": [1], "apply": range(1, 100),
                         "append": [2], "union": [2], "intersection": [2], "l": [1], "join": [0, 1], "rev": [1],
                         "sum": [1], "slice": [1, 2, 3], "openurl": [1], "min": [1], "max": [1],
                         "s": [1], "split": [1, 2], "n": [1], "difference": range(2, 100),
                         "count": range(2, 100), "nummap": [1], "lower": [1], "upper": [1], "capitalize": [1],
                         "strip": [1, 2], "replace": [3], "isupper": [1], "islower": [1], "iscapitalized": [1],
                         "input": [0], "sort": [1], "posof": [2], "combinations": [2], "allcombinations": [1],
                         "permutations": [1], "mostcommon": [1, 2], "multicombinations": [1, 2],
                         "removeduplicates": [1], "range": [1, 2, 3], "delete_at": range(2, 100), "pop": [1, 2],
                         "getfields": [0, 1], "quit": [0], "remove_all": range(2, 100), "remove": range(2, 100),
                         "keys": [1], "values": [1], "flatten": [1], "getscope": [0], "clone": [1]}

MATH_KEYWORDS = ["sin", "cos", "tan", "asin", "acos", "atan", "sqrt", "factorial"]
INTERNAL_KEYWORDS = ["p", "apply", "plot", "getfields", "getscope"]
BUILTIN_KEYWORDS_WITHOUT_PROCESSING = ["arr", "bool", "type"]
BUILTIN_KEYWORDS = ["midnight", "rick", "leet", "range", "input", "l", "s", "n", "openurl", "abs", "quit"]
OBJECT_KEYWORDS = [k for k in BUILTIN_EXPECTED_ARGS if k not in (MATH_KEYWORDS + INTERNAL_KEYWORDS + BUILTIN_KEYWORDS)]

OPERATIONAL_NODES = ["AddNode", "SubNode", "MultNode", "DivNode", "ModulusNode", "ExpNode", "FloorDivNode"]

BUILT_IN_FIELDS = {"PI": Datatypes.Number(math.pi), "E": Datatypes.Number(math.e),
                   "GOLDEN": Datatypes.Number((1 + 5 ** 0.5) / 2), "H": Datatypes.Number(6.62607004 * (10 ** (-34))),
                   "ALPHABET": Datatypes.String("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"),
                   "NUMBERS": Datatypes.String("123456789")}


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
    if elem is not None:
        return repr(elem)


def convert_to_builtins(argument_list):
    return list(Datatypes.Array(argument_list).convert_to_builtins())


class Interpreter:
    def __init__(self):
        self.fields = {"global": BUILT_IN_FIELDS.copy()}
        self.backup_fields = {}
        self.scope = "global"
        self.output_lines = []

    def get_output(self, ast_list, printall=True):
        self.output_lines = []
        for ast in ast_list:
            out = standardize(self.evaluate(ast))
            out = [stringify(o) for o in out if o is not None]
            if printall:
                merge(self.output_lines, out)
        return self.output_lines

    def evaluate(self, node):
        match type(node).__name__:
            case "FuncDeclareNode":
                self.fields["global"][node.identifier] = Datatypes.Function(node.arguments, node.body, node.identifier)
                if node.identifier in BUILTIN_EXPECTED_ARGS:
                    return Datatypes.String(f"Warning: Built-in function {node.identifier} has been overridden.")
            case "FuncCallNode":
                return self.function_call_handler(node)
            case "PeriodCallNode":
                return self.period_call_handler(node)
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
                arr = self.evaluate(node.identifier)
                if not hasattr(arr, "__iter__"):
                    raise TypeError(f"Element of type {type(arr).__name__} is not iterable.")
                arr = arr.clone()
                self.fields["global"]["__arrfunc"] = Datatypes.Function(["x", "i", "self"], node.function, "__arrfunc")
                funcargs = {} if self.scope == "global" else self.fields[self.scope]
                for i, elem in enumerate(arr):
                    res = self.function_call_handler(Datatypes.FuncCallNode("__arrfunc", [elem, Datatypes.Number(i), arr]), funcargs)
                                                    
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
                custom_bool.rev()
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
                        return out
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
                if len(node.items) == 2:
                    id = node.items[1]
                    index_id = node.items[0]
                elif len(node.items) == 1:
                    id = node.items[0]
                    index_id = "_i"
                else:
                    id = "_x"
                    index_id = "_i"
                iterable = self.evaluate(node.iterable)
                self.scope = self.scope + " > IterLoop"
                self.fields[self.scope] = {}
                for i, element in enumerate(iterable):
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
                return Datatypes.Array(list(np.arange(
                    self.evaluate(node.start),
                    self.evaluate(node.stop),
                    self.evaluate(node.step)
                )))
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
            case _:
                return node

    def rollback(self):
        self.fields = self.backup_fields
        self.scope = "global"
        self.output_lines = []

    def function_call_handler(self, node, optional_funcargs=dict()):
        func = self.fields["global"].get(node.identifier)
        if func is None:
            if node.identifier in BUILTIN_EXPECTED_ARGS:
                return self.builtin_handler(node)
            else:
                raise NameError(f"No function found with name {node.identifier}")
        elif not isinstance(func, Datatypes.Function):
            raise TypeError(f"{builtins.type(node).__name__} object is not callable")
        arguments = node.arguments
        if len(arguments) != len(func.arguments):
            raise TypeError(
                f"Expected {len(func.arguments)} arguments for function {node.identifier}, got {len(arguments)}.")
        new_function_scope = self.scope + " >> " + node.identifier
        self.fields[new_function_scope] = {}
        reached_kwargs = False
        for i, argument in enumerate(arguments):
            if isinstance(argument, Datatypes.AssignNode) and type(argument.value) not in (Datatypes.AddNode, Datatypes.SubNode):
                reached_kwargs = True
                if argument.variable.identifier in func.arguments:
                    self.fields[new_function_scope][argument.variable.identifier] = self.evaluate(argument.value)
                else:
                    raise TypeError(f"Function argument {argument.identifier} not found in function {node.identifier}.")
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
                    if isinstance(returned_result, list):
                        returned_result = returned_result[0]
                    break
        else:
            returned_result = self.evaluate(func.body)
        self.fields[self.scope].clear()
        self.scope = " >> ".join(self.scope.split(" >> ")[:-1])
        return returned_result

    def builtin_handler(self, node):
        keyword = node.identifier
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

    def period_call_handler(self, node):
        if isinstance(node.right_side, Datatypes.FuncCallNode):
            return self.function_call_handler(
                Datatypes.FuncCallNode(node.right_side.identifier, [node.left_side, *node.right_side.arguments]))
        elif isinstance(node.right_side, Datatypes.VariableNode) and (
                        node.right_side.identifier in BUILTIN_EXPECTED_ARGS or isinstance(
                            self.fields["global"].get(node.right_side.identifier), Datatypes.Function)):
            return self.function_call_handler(Datatypes.FuncCallNode(node.right_side.identifier, [node.left_side]))
        else:
            raise Exception("pos1")

    def plot(self, function, lower_rng=-5, upper_rng=5, increment=0.001):
        if increment < 0.0001:
            raise ValueError("Plotting increment can not be less than 0.0001")
        args = np.arange(lower_rng, upper_rng, increment)
        try:
            func_args = np.array(
                [self.function_call_handler(Datatypes.FuncCallNode(function.identifier, [arg])) for arg in args])
        except TypeError:
            raise TypeError("Only functions with exactly one argument can be plotted.")
        plt.rcParams["figure.autolayout"] = True
        plt.grid(visible=True, which="major", axis="both")
        plt.plot(args, func_args, c="orange", label=f"f(x)={function.identifier}(x)")
        plt.axvline(x=0)
        plt.axhline(y=0)
        plt.legend()
        plt.show()

    def p(self, *args):
        lines = []
        for arg in args:
            if arg is not None:
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
            res = self.function_call_handler(Datatypes.FuncCallNode(args[1].identifier, [elem]))
            if isinstance(res, list):
                args[0][Datatypes.Number(i)] = res[0]
            else:
                args[0][Datatypes.Number(i)] = res
        return args[0]

    def getfields(self, *args):
        if len(args) == 1:
            return self.fields[args[0]]
        return self.fields
    
    def getscope(self):
        return self.scope
