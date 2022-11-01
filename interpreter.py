import math
from webbrowser import get
import Datatypes
import numpy as np
from matplotlib import pyplot as plt
import builtins
import equation_solver
import builtinfunctions

BUILTIN_EXPECTED_ARGS = {"sin":[1], "cos":[1], "tan":[1], "asin":[1], "acos":[1], "atan":[1], "abs":[1], "sqrt":[1], "factorial":[1], "bool":[1],
            "plot":[3,4], "p":range(1,100), "midn":[3], "rick":[0], "leet":[1], "type":[1], "arr":[1], "apply":range(1,100),
            "append":[2], "union":[2], "intersection":[2], "l":[1], "join":[0,1], "rev":[1], "sum":[1], "slice": [1,2,3],
            "openurl":[1], "min":range(1,100), "max":range(1,100), "s":range(1,100), "split":[1,2], "n":[1], "difference":range(2,100),
            "count":range(2,100), "nummap":[1], "lower":[1], "upper":[1], "capitalize":[1], "strip":[1,2], "replace":[3], "isupper":[1],
            "islower":[1], "iscapitalized":[1], "input":[0], "sort":[1], "posof":[2], "combinations":[2], "allcombinations":[1],
            "permutations":[1], "mostcommon":[1,2], "multicombinations":[1,2], "removeduplicates":[1], "range":[1,2,3], "deleteAt":range(2,100), "pop":[1,2],}
        
MATH_KEYWORDS = ["sin", "cos", "tan", "asin", "acos", "atan", "sqrt", "factorial"]
INTERNAL_KEYWORDS = ["p", "plot"]
BUILTIN_KEYWORDS = ["midn", "rick", "leet", "range", "input", "l", "s", "n", "bool", "arr", "openurl", "abs", "type"] 
OBJECT_KEYWORDS = [k for k in BUILTIN_EXPECTED_ARGS if k not in (MATH_KEYWORDS+INTERNAL_KEYWORDS+BUILTIN_KEYWORDS)]

OPERATIONAL_NODES = ["AddNode", "SubNode", "MultNode", "DivNode", "ModulusNode", "ExpNode"]

BUILT_IN_FIELDS =  {"pi": math.pi, "e": math.e, "golden": (1 + 5 ** 0.5) / 2, "h": 6.62607004 * (10 ** (-34)), 
                    "alphabet": Datatypes.String("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"), "numbers": Datatypes.String("123456789")}


def standardize(val):
    if isinstance(val, list):
        return val
    else:
        return [val]

def merge(output_list, list_to_append):
    for item in list_to_append:
        if item is not None:
            output_list.append(item)


class Interpreter:
    def __init__(self):
        # Define global and local fields, which emulate global and local (function) scope
        self.fields = {"global": BUILT_IN_FIELDS.copy()}
        self.backup_fields = {}
        self.scope = "global"
        self.nested_scopes = []
        self.output_lines = []

    def remove_decimals(self, elem):
        if isinstance(elem, float) and elem%1==0:
            return int(elem)
        return elem

    def stringify(self, elem):
        if isinstance(elem, float) and elem%1 == 0:
            elem = int(elem)
        if elem is not None:
            return repr(self.remove_decimals(elem)).replace(r'\n', '\n')

    def convert_to_builtins(self, arglist):
        return list(Datatypes.Array(arglist).convert_to_builtins())        

    def get_output(self, ast_list, printall=True):
        self.output_lines = []
        for ast in ast_list:
            out = standardize(self.evaluate(ast))
            out = [self.stringify(o) for o in out if o is not None]
            if printall:
                merge(self.output_lines, out)
        return self.output_lines

    # Will evaluate the ast (parser output) recursively
    def evaluate(self, node):
        node_type = builtinfunctions.type(node)
        if node_type == "FuncDeclareNode":
            self.fields["global"][node.identifier] = Datatypes.Function(node.arguments, node.body, node.identifier)
            if node.identifier in BUILTIN_EXPECTED_ARGS:
                return Datatypes.String(f"Warning: Built-in function {node.identifier} has been overridden.")
        elif node_type == "FuncCallNode":
            return self.function_call_handler(node)
        elif node_type == "PeriodCallNode":
            return self.period_call_handler(node)
        elif node_type in OPERATIONAL_NODES:
            return self.operation_handler(node)
        elif node_type == "AssignNode":
            assignment_value = self.evaluate(node.value)
            print(type(assignment_value).__name__)
            if isinstance(node.identifier, Datatypes.ArrayCallNode):
                last_index = node.identifier.index.pop()
                arr = self.evaluate(node.identifier)
                arr[self.evaluate(last_index)] = assignment_value
                node.identifier.index.append(last_index)
            else:
                global_value = self.fields["global"].get(node.identifier)
                local_value = self.fields[self.scope].get(node.identifier)
                if local_value is not None:
                    self.fields[self.scope][node.identifier] = assignment_value
                elif global_value is not None:
                    self.fields["global"][node.identifier] = assignment_value
                else:
                    self.fields[self.scope][node.identifier] = assignment_value
            return assignment_value
        elif node_type == "SolveNode":
            _, expression = equation_solver.solve(node.left_side, node.right_side)
            return self.evaluate(expression)
        elif node_type == "SolveAssignNode":
            variable, expression = equation_solver.solve(node.left_side, node.right_side)
            result = self.evaluate(expression)
            return self.evaluate(Datatypes.AssignNode(variable.identifier, result))
        elif node_type == "ArrayCallNode":
            arr = self.evaluate(node.identifier)
            for index in node.index:
                if isinstance(index, Datatypes.RangeNode):
                    arr = arr.slice(self.evaluate(index.start), self.evaluate(index.stop), self.evaluate(index.step) )
                else:
                    arr = arr[self.evaluate(index)]
            return arr
        elif node_type == "ArrayApplyNode":
            arr = self.evaluate(node.identifier)
            if not isinstance(arr, float):
                arr = arr.copy()
            self.fields["global"]["__arrfunc"] = Datatypes.Function(["x", "i", "self"], node.function, "__arrfunc")
            funcargs = {}
            if self.scope != "global":
                for k, v in self.fields[self.scope].items():
                    funcargs[k] = v                
            if hasattr(arr, "__iter__"):
                for i, elem in enumerate(arr):
                    res = self.function_call_handler(Datatypes.FuncCallNode("__arrfunc", [elem, i, arr]), funcargs)
                    if isinstance(res, list):
                        if len(res) == 0:
                            continue
                        elif isinstance(res[0], Datatypes.Token) and res[0].type == Datatypes.DEL:
                            arr.delete()
                        else:
                            arr[i] = res[0]
                    else:
                        if isinstance(res, Datatypes.Token) and res.type == Datatypes.DEL:
                            arr.delete()
                        else:
                            arr[i] = res
                return arr
            else:
                return self.evaluate(Datatypes.AssignNode(node.identifier, self.function_call_handler(Datatypes.FuncCallNode("__arrfunc", [arr, 0, arr]))))
        elif node_type == "ComparisonNode":
            return self.comparison_handler(node)
        elif node_type == "BooleanNegationNode":
            boolean = self.evaluate(node.value)
            custom_bool = Datatypes.Bool(boolean)
            custom_bool.rev()
            return custom_bool
        elif node_type == "BooleanConversionNode":
            return Datatypes.Bool(self.evaluate(node.value))
        elif node_type == "ContainsNode":
            return Datatypes.Bool(self.evaluate(node.item) in self.evaluate(node.iterable))
        elif node_type == "LogicalOperationNode":
            if node.operation == Datatypes.AND:
                return Datatypes.Bool(
                    Datatypes.Bool(self.evaluate(node.a)) and Datatypes.Bool(self.evaluate(node.b)))
            else:
                return Datatypes.Bool(
                    Datatypes.Bool(self.evaluate(node.a)) or Datatypes.Bool(self.evaluate(node.b)))
        elif node_type == "IfNode":
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
        elif node_type == "VariableNode":
            # Will check for a local field first, then a global one, and finally raise an exception if
            # both fields are nonexistent
            global_value = self.fields["global"].get(node.identifier)
            local_value = self.fields[self.scope].get(node.identifier)
            if local_value is not None:
                result = local_value
            elif global_value is not None:
                result = global_value
            else:
                raise NameError(f"Name \"{node.identifier}\" is not defined.")
            return result
        elif node_type == "RepNode":
            reps = self.evaluate(node.repetitions)
            if not isinstance(reps, float) or reps < 0 or reps % 1 != 0:
                raise ValueError(f"Invalid repetition count, expected a whole positive number, got {reps}")
            out = []
            for i in range(int(reps)):
                self.fields["global"][node.count_identifier] = float(i)
                for statement in node.statements:
                    lines = standardize(self.evaluate(statement))
                    if "__break__" in self.fields[self.scope] or "__continue__" in self.fields[self.scope]:
                        break
                    if "__return__" in self.fields[self.scope]:
                        return out
                    merge(out, lines)
                else:
                    continue
                if "__break__" in self.fields[self.scope]:
                    self.fields[self.scope].pop("__break__")
                    break
                elif "__continue__" in self.fields[self.scope]:
                    self.fields[self.scope].pop("__continue__")
                self.fields[self.scope].pop(node.count_identifier)
            return out
        elif node_type == "ForNode":
            self.evaluate(node.assignment)
            out = []
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
            self.fields[self.scope].pop(node.assignment.identifier)
            return out
        elif node_type == "ForEachNode":
            out = []
            id = node.item
            iterable = self.evaluate(node.iterable)
            for element in iterable:
                self.evaluate(Datatypes.AssignNode(id, element))
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
            self.fields[self.scope].pop(id)
            return out
        elif node_type == "IterateNode":
            out=[]
            if len(node.items) == 2:
                id = node.items[1]
                index_id = node.items[0]
            elif len(node.items) == 1:
                id = node.items[0]
                index_id = "_i"
            elif len(node.items) == 0:
                id = "_x"
                index_id = "_i"
            iterable = self.evaluate(node.iterable)
            for i, element in enumerate(iterable):
                self.evaluate(Datatypes.AssignNode(id, element))
                self.evaluate(Datatypes.AssignNode(index_id, i))
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
            self.fields[self.scope].pop(id)
            return out
        elif node_type == "RangeNode":
            return Datatypes.Array(list(np.arange(node.start,node.stop,node.step)))
        elif node_type == "ReturnNode":
            if self.scope == "global":
                raise SyntaxError("Return statement outside function")
            self.fields[self.scope]["__return__"] = self.evaluate(node.statement)
        elif node_type == "BreakNode":
            self.fields[self.scope]["__break__"] = Datatypes.Bool(True)
        elif node_type == "ContinueNode":
            self.fields[self.scope]["__continue__"] = Datatypes.Bool(True)
        elif node_type == "Array":
            temp = Datatypes.Array(node.contents.copy())
            for i, elem in enumerate(temp):
                temp[i] = self.evaluate(elem)
            return temp
        else:
            return node

    def rollback(self):
        self.fields = self.backup_fields
        self.scope = "global"
        self.nested_scopes = []
        self.output_lines = []

    # Will handle all nodes of type FuncCallNode
    def function_call_handler(self, node, optional_funcargs = {}):
        # Fetches the function and its name from the global fields
        func = self.fields["global"].get(node.identifier)
        # If none is found, the function might be a built-in one. If not, an error will be risen
        if func is None:
            if node.identifier in BUILTIN_EXPECTED_ARGS:
                return self.builtin_handler(node)
            else:
                raise NameError(f"No function found with name {node.identifier}")
        # If the field previously fetched is not a function (i.e. a float value), an error will be risen
        elif not isinstance(func, Datatypes.Function):
            raise TypeError(f"{builtins.type(node).__name__} object is not callable")
        # The arguments the user has called the function with are saved
        arguments = node.arguments
        # The numbers of the called and defined arguments have to match, else an error will be risen
        if len(arguments) != len(func.arguments):
            raise TypeError(
                f"Expected {len(func.arguments)} arguments for function {node.identifier}, got {len(arguments)}.")
        # The arguments the function was called with are now assigned
        # to the identifiers in the order they were previously defined in the function.
        # The arguments will be assigned to the local fields
        self.fields[node.identifier + str(len(self.nested_scopes) + 1)] = {}
        for i, argument in enumerate(arguments):
            self.fields[node.identifier + str(len(self.nested_scopes) + 1)][func.arguments[i]] = self.evaluate(argument)
        for k, v in optional_funcargs.items():
            self.fields[node.identifier + str(len(self.nested_scopes) + 1)][k] = v
        self.nested_scopes.append(self.scope)
        self.scope = node.identifier + str(len(self.nested_scopes))
        # Now that the variables are assigned, the function body can be evaluated
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
        # Local fields will be cleared after the function ends, just like in any other language
        self.fields[self.scope].clear()
        self.scope = self.nested_scopes.pop()
        return returned_result

    # Will handle all built-in functions
    def builtin_handler(self, node):
        keyword = node.identifier
        args = [self.evaluate(arg) for arg in node.arguments]
        arg_count = len(node.arguments)
        expected_arg_count = BUILTIN_EXPECTED_ARGS[keyword]
        if arg_count not in expected_arg_count:
            if len(expected_arg_count) == 1:
                raise TypeError(f"Expected {expected_arg_count[0]} arguments for function {keyword}, got {arg_count}.")
            else:
                TypeError(f"Expected at least {expected_arg_count[0]} arguments for function {keyword}, got {arg_count}.")
        if keyword in INTERNAL_KEYWORDS:
            return getattr(Interpreter, keyword)(self, *self.convert_to_builtins(args))
        elif keyword in BUILTIN_KEYWORDS:
            return getattr(builtinfunctions, keyword)(*self.convert_to_builtins(args))
        elif keyword in MATH_KEYWORDS:
            return getattr(math, keyword)(*self.convert_to_builtins(args))
        elif keyword == "apply":
            return self.apply(*args)
        else:
            return getattr(builtins.type(args[0]), keyword)(*args)

    # Will handle any type of simple operation
    def operation_handler(self, node):
        node_type = builtinfunctions.type(node)
        a = self.evaluate(node.a)
        b = self.evaluate(node.b)
        try:
            if node_type == "AddNode":
                return a + b
            elif node_type == "SubNode":
                return a - b
            elif node_type == "MultNode":
                return a * b
            elif node_type == "DivNode":
                return a / b
            elif node_type == "ModulusNode":
                return a % b
            elif node_type == "ExpNode":
                return a ** b
        except TypeError as e:
            raise TypeError(f"Cannot use this mathematical operation on object of type {builtinfunctions.type(a)} and {builtinfunctions.type(b)}")

    # Will handle any type of simple comparison
    def comparison_handler(self, node):
        # Will convert any chained comparison correctly. ie. converts (2<3<5) to (2<3 & 3<5)
        if isinstance(node.a, Datatypes.ComparisonNode):
            return self.evaluate(
                Datatypes.LogicalOperationNode(node.a, Datatypes.ComparisonNode(node.a.b, node.b, node.operator),
                                               Datatypes.AND))
        a = self.evaluate(node.a)
        b = self.evaluate(node.b)
        operator = node.operator
        # Fetches the boolean value of the Bool datatype to be able to evaluate it in python
        if isinstance(a, Datatypes.Bool):
            a = bool(a)
        if isinstance(b, Datatypes.Bool):
            b = bool(b)
        if operator == Datatypes.COMP_EQUALS:
            result = Datatypes.Bool(a == b)
        elif operator == Datatypes.COMP_NOT_EQUALS:
            result = Datatypes.Bool(a != b)
        elif operator == Datatypes.GREATER_THAN:
            result = Datatypes.Bool(a > b)
        elif operator == Datatypes.LESS_THAN:
            result = Datatypes.Bool(a < b)
        elif operator == Datatypes.GREATER_OR_EQUALS:
            result = Datatypes.Bool(a >= b)
        elif operator == Datatypes.LESS_OR_EQUALS:
            result = Datatypes.Bool(a <= b)
        else:
            raise Exception("An unknown error occurred")
        return result

    def period_call_handler(self, node):
        if isinstance(node.right_side, Datatypes.FuncCallNode):
            return self.function_call_handler(Datatypes.FuncCallNode(node.right_side.identifier, [node.left_side, *node.right_side.arguments]))
        elif isinstance(node.right_side, Datatypes.VariableNode) and (node.right_side.identifier in BUILTIN_EXPECTED_ARGS or isinstance(self.fields["global"].get(node.right_side.identifier), Datatypes.Function)):
            return self.function_call_handler(Datatypes.FuncCallNode(node.right_side.identifier, [node.left_side]))
        else:
            raise Exception("pos1")
            
    def plot(self, function, lower_rng=-5, upper_rng=5, increment=0.001):
        if increment < 0.0001:
            raise ValueError("Plotting increment can not be less than 0.0001")
        args = np.arange(lower_rng, upper_rng, increment)
        try:
            func_args = np.array([self.function_call_handler(Datatypes.FuncCallNode(function.identifier, [arg])) for arg in args])
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
            out += str(line) + " "
        out = [out.strip()]
        merge(self.output_lines, out)
        return

    def apply(self, *args):
        for i, elem in enumerate(args[0]):
            res = self.function_call_handler(Datatypes.FuncCallNode(args[1].identifier, [elem]))
            if isinstance(res, list):
                args[0][i] = res[0]
            else:
                args[0][i] = res
        return args[0]