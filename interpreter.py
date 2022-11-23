import builtins
import math
import numpy as np
from matplotlib import pyplot as plt
import Datatypes
import builtinfunctions
import equation_solver
import os

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
                         "every": [2], "reverse": [1], "hasKey": [2], "hasValue": [2], "new": range(1,100),
                         "deepclone": [1], "load": range(1,100), "sameAs": [2], "instanceOf": [2]
                         }

MATH_KEYWORDS = ["sin", "cos", "tan", "asin", "acos", "atan", "sqrt", "factorial"]
INTERNAL_KEYWORDS = ["out", "apply", "select", "plot", "getFields", "getScope", "detect", "foreach", "every", "new", "load"]
BUILTIN_KEYWORDS_WITHOUT_PROCESSING = ["asArr", "bool", "type", "quit", "rick", "input", "size", "asString", "repr", "arrOf", "sameAs", "instanceOf"]
BUILTIN_KEYWORDS = ["midnight", "leet", "range", "asNum", "openURL", "abs", "divMod", "change", "fill"]
OBJECT_KEYWORDS = [k for k in BUILTIN_EXPECTED_ARGS if k not in (MATH_KEYWORDS + INTERNAL_KEYWORDS + BUILTIN_KEYWORDS)]

OPERATIONAL_NODES = [Datatypes.AddNode, Datatypes.SubNode, Datatypes.MultNode, Datatypes.DivNode, Datatypes.ModulusNode, Datatypes.ExpNode, Datatypes.FloorDivNode]

BUILT_IN_FIELDS = {"PI": Datatypes.Number(math.pi), "E": Datatypes.Number(math.e),
                   "GOLDEN": Datatypes.Number((1 + 5 ** 0.5) / 2), "H": Datatypes.Number(6.62607004 * (10 ** (-34))),
                   "ALPHABET": Datatypes.String("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"),
                   "NUMBERS": Datatypes.String("1234567890"), "String": Datatypes.String, "Number": Datatypes.Number, "Bool": Datatypes.Bool,
                   "Function": Datatypes.Function, "Array": Datatypes.Array, "Dictionary": Datatypes.Dictionary, "Class": Datatypes.Class
                   }


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
    return [argument.get_num() if isinstance(argument, Datatypes.Number) else argument for argument in argument_list]


def stringify(elem):
    if type(elem) in Datatypes.DATATYPES:
        return repr(elem)


def convert_to_builtins(argument_list):
    return [Datatypes.convert_to_builtin(arg) for arg in argument_list]


class Interpreter:
    def __init__(self, autoid=False, filespace={}):
        self.fields = {"global": BUILT_IN_FIELDS.copy()}
        self.backup_fields = {}
        self.scope = "global"
        self.output_lines = []
        self.filespace = {}
        self.load_requests = []
        for file in os.listdir():
            if file.endswith(".oxy"):
                self.filespace[file.strip(".oxy")] = file
        self.autoid = autoid

    def get_output(self, ast_list, printall=True):
        self.output_lines = []
        self.load_requests = []
        for ast in ast_list:
            out = standardize(self.evaluate(ast))
            out = [stringify(o) for o in out]
            if printall:
                merge(self.output_lines, out)
        out = self.output_lines
        self.output_lines = []
        load_requests = self.load_requests
        self.load_requests = []
        return out, load_requests

    def evaluate(self, node):
        match type(node):
            case Datatypes.FuncCallNode:
                if isinstance(node.variable, Datatypes.FuncCallNode):
                    return self.evaluate(
                        Datatypes.FuncCallNode(node.variable.variable, [*node.arguments, *node.variable.arguments]))
                args = [arg if isinstance(arg, Datatypes.AssignNode) \
                    and type(arg.value) not in (Datatypes.AddNode, Datatypes.SubNode) else self.evaluate(arg) for arg in node.arguments]
                if len(args) > 0 and not node.force_skip_obj:
                    if type(args[0]) == Datatypes.Instance:
                        return self.instance_call_handler(node,args)
                    elif type(args[0]) == Datatypes.Class:
                        return self.class_call_handler(node,args)
                if node.variable.identifier in BUILTIN_EXPECTED_ARGS:
                    return self.builtin_handler(node.variable.identifier, args)
                if node.variable.identifier in self.fields["global"] or isinstance(node.variable, Datatypes.Function):
                    return self.function_call_handler(self.evaluate(node.variable), node, args)
                raise Exception()
            case name if name in OPERATIONAL_NODES:
                return self.operation_handler(node)
            case Datatypes.AssignNode:
                assignment_value = self.evaluate(node.value)
                if isinstance(node.variable, Datatypes.FuncCallNode) and len(node.variable.arguments) == 1 and\
                    isinstance(node.variable.arguments[0], Datatypes.VariableNode) and\
                    type(self.evaluate(Datatypes.VariableNode(node.variable.arguments[0].identifier))) == Datatypes.Instance:
                    current_instance = self.evaluate(Datatypes.VariableNode(node.variable.arguments[0].identifier))
                    setattr(current_instance, node.variable.variable.identifier, assignment_value)
                elif self.scope.startswith("##"):
                    current_class = self.fields["global"].get(self.scope.strip("##"))
                    if isinstance(assignment_value, Datatypes.Function):
                        if not assignment_value.is_static:
                            assignment_value.arguments.insert(0, "own")
                        assignment_value.identifier = "#" + current_class.identifier + " > " + assignment_value.identifier
                    setattr(current_class, node.variable.identifier, assignment_value)
                elif isinstance(node.variable, Datatypes.BracketCallNode):
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
                        if super_scopes[-1].startswith("#"):
                            called_class = self.fields["global"].get(super_scopes[-1].strip("#"))
                            try:
                                super_value = setattr(called_class, node.identifier, assignment_value)
                            except AttributeError:
                                pass
                            finally:
                                break
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
            case Datatypes.SolveNode:
                _, expression = equation_solver.solve(node.left_side, node.right_side)
                return self.evaluate(expression)
            case Datatypes.SolveAssignNode:
                variable, expression = equation_solver.solve(node.left_side, node.right_side)
                result = self.evaluate(expression)
                return self.evaluate(Datatypes.AssignNode(variable, result))
            case Datatypes.BracketCallNode:
                arr = self.evaluate(node.identifier)
                for index in node.index:
                    if isinstance(index, Datatypes.RangeNode):
                        arr = arr.slice(self.evaluate(index.start), self.evaluate(index.stop), self.evaluate(index.step))
                    else:
                        arr = arr[self.evaluate(index)]
                return arr
            case Datatypes.PostIncrementNode:
                pre_assignment_value = self.evaluate(node.factor)
                self.evaluate(Datatypes.AssignNode(node.factor, Datatypes.AddNode(node.factor, node.value)))
                return pre_assignment_value
            case Datatypes.ArrayApplyNode:
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
            case Datatypes.ComparisonNode:
                return self.comparison_handler(node)
            case Datatypes.BooleanNegationNode:
                return Datatypes.Bool(not self.evaluate(node.value))
            case Datatypes.LogicalOperationNode:
                if node.operation == Datatypes.AND:
                    return Datatypes.Bool(
                        Datatypes.Bool(self.evaluate(node.a)) and Datatypes.Bool(self.evaluate(node.b)))
                else:
                    return Datatypes.Bool(
                        Datatypes.Bool(self.evaluate(node.a)) or Datatypes.Bool(self.evaluate(node.b)))
            case Datatypes.IfNode:
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
            case Datatypes.VariableNode:
                global_value = self.fields["global"].get(node.identifier)
                filespace_value = self.filespace.get(node.identifier)
                super_value = None
                temp = self.scope.split(" >> ")
                funcpath = " >> ".join(temp[:-1]) + " >> " if len(temp) > 1 else ""
                super_scopes = temp[-1].split(" > ")
                while len(super_scopes) > 0:
                    if super_scopes[-1].startswith("#"):
                        called_class = self.fields["global"].get(super_scopes[-1].strip("#"))
                        try:
                            super_value = getattr(called_class, node.identifier)
                        except AttributeError:
                            pass
                        finally:
                            break
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
                elif filespace_value is not None:
                    result = filespace_value
                else:
                    raise NameError(f"Name \"{node.identifier}\" is not defined.")
                return result
            case Datatypes.ForNode:
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
            case Datatypes.IterateNode:
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
            case Datatypes.RangeNode:
                return Datatypes.Array([Datatypes.Number(num) for num in builtins.range(
                    self.evaluate(node.start).get_num(),
                    self.evaluate(node.stop).get_num(),
                    self.evaluate(node.step).get_num()
                )])
            case Datatypes.ReturnNode:
                if self.scope == "global":
                    raise SyntaxError("Return statement outside function")
                self.fields[self.scope]["__return__"] = self.evaluate(node.statement)
            case Datatypes.ArrayDeclareNode:
                new_arr = Datatypes.Array(node.items.copy())
                for i, elem in enumerate(new_arr):
                    new_arr[Datatypes.Number(i)] = self.evaluate(elem)
                return new_arr
            case Datatypes.DictDeclareNode:
                new_dict = Datatypes.Dictionary({})
                for item in node.items:
                    new_dict[self.evaluate(item[0])] = self.evaluate(item[1])
                return new_dict
            case Datatypes.ClassDeclareNode:
                constructor=None
                self.scope = "##"+node.identifier.identifier
                for i, statement in enumerate(node.body):
                    if isinstance(statement, Datatypes.AssignNode) and isinstance(statement.value, Datatypes.Function) and \
                        statement.value.identifier == "setup":
                        statement.value.arguments.insert(0, "own")
                        constructor = statement.value
                        node.body.pop(i)
                        break
                new_class =  Datatypes.Class(identifier=node.identifier.identifier ,constructor=constructor)
                self.fields["global"][node.identifier.identifier] = new_class
                for statement in node.body:
                    self.evaluate(statement)
                self.scope = "global"
            case Datatypes.StringBuilderNode:
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
        self.load_requests = []

    def function_call_handler(self, func, node, args, optional_funcargs=dict()):
        delimiter = " > " if func.identifier == "Anonymous" else " >> "
        if not isinstance(func, Datatypes.Function):
            raise TypeError(f"{builtins.type(node).__name__} object is not callable")
        if len(args) != len(func.arguments):
            raise TypeError(
                f"Expected {len(func.arguments)} arguments for function {func.identifier}, got {len(args)}.")
        new_function_scope = self.scope + delimiter + func.identifier
        self.fields[new_function_scope] = {}
        reached_kwargs = False
        for i, argument in enumerate(args):
            if isinstance(argument, Datatypes.AssignNode) and type(argument.value) not in (Datatypes.AddNode, Datatypes.SubNode):
                reached_kwargs = True
                if argument.variable.identifier in func.arguments:
                    self.fields[new_function_scope][argument.variable.identifier] = self.evaluate(argument.value)
                else:
                    raise TypeError(f"Function argument {argument.identifier} not found in function {func.identifier}.")
            elif reached_kwargs:
                raise SyntaxError("Positional arguments are not allowed after keyword arguments.")
            else:
                self.fields[new_function_scope][func.arguments[i]] = argument
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


    def class_call_handler(self, node, args):
        attr_id = node.variable.identifier
        attr_class = args.pop(0)
        try:
            attr = getattr(attr_class, attr_id)
        except AttributeError:
            return self.evaluate(Datatypes.FuncCallNode(node.variable, [attr_class]+args, True))
        if isinstance(attr, Datatypes.Function):
            return self.evaluate(Datatypes.FuncCallNode(attr, args))
        elif len(node.arguments) > 0:
            raise Exception(f"Attribute {attr_id} of class {attr_class} is not callable.")
        else:
            return attr

    def instance_call_handler(self, node, args):
        attr_id = node.variable.identifier
        attr_instance = args.pop(0)
        try:
            attr = getattr(attr_instance, attr_id)
        except AttributeError:
            try:
                attr = getattr(attr_instance.ownclass, attr_id)
            except AttributeError:
                return self.evaluate(Datatypes.FuncCallNode(node.variable, [attr_instance]+args, True))
        if isinstance(attr, Datatypes.Function):
            return self.evaluate(Datatypes.FuncCallNode(attr, [attr_instance, *args]))
        elif len(args) > 0:
            raise Exception(f"Attribute {attr_id} of instance {attr_instance} is not callable.")
        else:
            return attr

    def builtin_handler(self, funcname, args):
        arg_count = len(args)
        expected_arg_count = BUILTIN_EXPECTED_ARGS[funcname]
        if arg_count not in expected_arg_count:
            if len(expected_arg_count) == 1:
                raise TypeError(f"Expected {expected_arg_count[0]} arguments for function {funcname}, got {arg_count}.")
            else:
                TypeError(
                    f"Expected at least {expected_arg_count[0]} arguments for function {funcname}, got {arg_count}.")
        if funcname in INTERNAL_KEYWORDS:
            return getattr(Interpreter, funcname)(self, *args)
        elif funcname in BUILTIN_KEYWORDS:
            return getattr(builtinfunctions, funcname)(*convert_to_builtins(args))
        elif funcname in BUILTIN_KEYWORDS_WITHOUT_PROCESSING:
            return getattr(builtinfunctions, funcname)(*args)
        elif funcname in MATH_KEYWORDS:
            return Datatypes.Number(getattr(math, funcname)(*process_nums(args)))
        else:
            return getattr(builtins.type(args[0]), funcname)(*process_nums(args))

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
        
        if isinstance(a, Datatypes.Bool):
            a = bool(a)
        if isinstance(b, Datatypes.Bool):
            b = bool(b)
        match node.operator:
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
        args = [Datatypes.Number(num) for num in np.arange(lower_rng, upper_rng, increment)]
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

    def new(self, *args):
        called_class = self.evaluate(args[0])
        if not isinstance(called_class, Datatypes.Class):
            raise TypeError(f"Cannot initialize instance of type {type(args[0]).__name__}")
        new_instance = Datatypes.Instance(ownclass=called_class)
        self.evaluate(Datatypes.FuncCallNode(called_class.constructor, [new_instance, *args[1:]]))
        return new_instance

    def load(self, *args):
        for arg in args:
            self.load_requests.append(arg)