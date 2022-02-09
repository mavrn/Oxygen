import math
import Datatypes
import numpy as np
from matplotlib import pyplot as plt
from fractions import Fraction
import equation_solver

KEYWORDS = ["sin", "cos", "tan", "asin", "acos", "atan", "abs", "sqrt", "factorial", "bool", "plot", "fraction",
            "print"]
OPERATIONAL_NODES = ["AddNode", "SubNode", "MultNode", "DivNode", "ModulusNode", "ExpNode"]


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
        self.global_fields = {"pi": math.pi, "e": math.e, "golden": (1 + 5 ** 0.5) / 2, "h": 6.62607004 * (10 ** (-34))}
        self.fields = {"global": self.global_fields}
        self.backup_fields = {}
        self.scope = "global"
        self.prev_scope = ""
        self.return_value = None
        self.output_lines = []

    def get_output(self, ast_list):
        self.output_lines = []
        for ast in ast_list:
            out = standardize(self.evaluate(ast))
            merge(self.output_lines, out)
        return self.output_lines

    # Will evaluate the ast (parser output) recursively
    def evaluate(self, node):
        node_type = type(node).__name__
        if node_type == "FuncDeclareNode":
            self.fields["global"][node.identifier] = Datatypes.Function(node.arguments, node.body)
            if node.identifier in KEYWORDS:
                return Datatypes.String(f"Warning: Built-in function {node.identifier} has been overridden.")
        elif node_type == "FuncCallNode":
            return self.function_call_handler(node)
        elif node_type in OPERATIONAL_NODES:
            return self.operation_handler(node)
        elif node_type == "AssignNode":
            assignment_value = self.evaluate(node.value)
            global_value = self.fields["global"].get(node.identifier)
            if global_value is not None:
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
        elif node_type == "ComparisonNode":
            return self.comparison_handler(node)
        elif node_type == "BooleanNegationNode":
            boolean = self.evaluate(node.value)
            custom_bool = Datatypes.Bool(boolean)
            custom_bool.reverse()
            return custom_bool
        elif node_type == "BooleanConversionNode":
            return Datatypes.Bool(self.evaluate(node.value))
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
                    results = standardize(self.evaluate(block["body"]))
                    break
            for statement in results:
                line = standardize(self.evaluate(statement))
                merge(out, line)
            return out
        elif node_type == "VariableNode":
            # Will check for a local field first, then a global one, and finally raise an exception if
            # both fields are nonexistent
            global_value = self.fields["global"].get(node.identifier)
            local_value = self.fields[self.scope].get(node.identifier)
            if local_value is not None:
                return local_value
            elif global_value is not None:
                return global_value
            else:
                raise NameError(f"Name \"{node.identifier}\" is not defined.")
        elif node_type == "RepNode":
            reps = self.evaluate(node.repetitions)
            if not isinstance(reps, float) or reps < 0 or reps % 1 != 0:
                raise ValueError(f"Invalid repetition count, expected a whole positive number, got {reps}")
            out = []
            for i in range(int(reps)):
                self.fields["global"][node.count_identifier] = float(i)
                for statement in node.statements:
                    lines = standardize(self.evaluate(statement))
                    merge(out, lines)
            return out
        elif node_type == "ForNode":
            self.evaluate(node.assignment)
            out = []
            while bool(self.evaluate(node.condition)):
                for statement in node.statements:
                    lines = standardize(self.evaluate(statement))
                    merge(out, lines)
                self.evaluate(node.increment)
            return out
        elif node_type == "KeywordNode":
            return self.keyword_handler(node)
        elif node_type == "ReturnNode":
            self.return_value = self.evaluate(node.statement)
        else:
            return node

    def rollback(self):
        self.fields = self.backup_fields
        self.scope = "global"
        self.return_value = None
        self.output_lines = []

    # Will handle all nodes of type FuncCallNode
    def function_call_handler(self, node):
        # Fetches the function and its name from the global fields
        func = self.fields["global"].get(node.identifier)
        node_type = type(func).__name__
        # If none is found, the function might be a built-in one. If not, an error will be risen
        if func is None:
            if node.identifier in KEYWORDS:
                return self.keyword_handler(node)
            else:
                raise NameError(f"No function found with name {node.identifier}")
        # If the field previously fetched is not a function (i.e. a float value), an error will be risen
        elif node_type != "Function":
            raise TypeError(f"{node_type} object is not callable")
        # The arguments the user has called the function with are saved
        arguments = node.arguments
        # The numbers of the called and defined arguments have to match, else an error will be risen
        if len(arguments) != len(func.arguments):
            raise TypeError(
                f"Expected {len(func.arguments)} arguments for function {node.identifier}, got {len(arguments)}.")
        # The arguments the function was called with are now assigned
        # to the identifiers in the order they were previously defined in the function.
        # The arguments will be assigned to the local fields
        self.fields[node.identifier] = {}
        for i, argument in enumerate(arguments):
            self.fields[node.identifier][func.arguments[i]] = self.evaluate(argument)
        self.prev_scope = self.scope
        self.scope = node.identifier
        # Now that the variables are assigned, the function body can be evaluated
        result = None
        if isinstance(func.body, list):
            for statement in func.body:
                self.evaluate(statement)
                if self.return_value is not None:
                    result = self.return_value
                    self.return_value = None
                    break
        else:
            result = self.evaluate(func.body)
        # Local fields will be cleared after the function ends, just like in any other language
        self.scope = self.prev_scope
        return result

    # Will handle all built-in functions
    def keyword_handler(self, node):
        keyword = node.identifier
        arg_count = len(node.arguments)
        if keyword == "plot":
            if arg_count not in (3, 4):
                raise TypeError(f"Expected 3 to 4 arguments for function {keyword}, got {arg_count}.")
            args = [node.arguments[0].identifier, *[self.evaluate(arg) for arg in node.arguments[1:]]]
            return self.plot_handler(*args)
        elif arg_count != 1 and keyword != "print":
            raise TypeError(f"Expected 1 argument for function {keyword}, got {arg_count}.")
        arg = self.evaluate(node.arguments[0])
        # Will match the identifier to the pre-defined keywords and operate accordingly
        if keyword == "sqrt":
            return math.sqrt(arg)
        elif keyword == "sin":
            return math.sin(arg)
        elif keyword == "cos":
            return math.cos(arg)
        elif keyword == "tan":
            return math.tan(arg)
        elif keyword == "factorial":
            if arg % 1 == 0:
                return float(math.factorial(int(arg)))
            else:
                raise TypeError(f"Expected type int, got type {type(arg).__name__}")
        elif keyword == "asin":
            return math.asin(arg)
        elif keyword == "acos":
            return math.acos(arg)
        elif keyword == "atan":
            return math.atan(arg)
        elif keyword == "abs":
            return abs(arg)
        elif keyword == "bool":
            return Datatypes.Bool(arg)
        elif keyword == "fraction":
            return Fraction(arg).limit_denominator()
        elif keyword == "print":
            lines = []
            for arg in node.arguments:
                lines.append(standardize(self.evaluate(arg)))
            for line in lines:
                lines_to_str = [Datatypes.String(item) for item in line]
                merge(self.output_lines, lines_to_str)
        else:
            raise Exception(f"Unknown exception occurred while handling the keyword {keyword}")

    # Will handle any type of simple operation
    def operation_handler(self, node):
        node_type = type(node).__name__
        a = self.evaluate(node.a)
        b = self.evaluate(node.b)
        for operand in [a, b]:
            if not isinstance(operand, float):
                raise TypeError("Cannot use mathematical operations on object of type " + type(operand).__name__)
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

    def plot_handler(self, function, lower_rng, upper_rng, increment=0.001):
        if increment < 0.0001:
            raise ValueError("Plotting increment can not be less than 0.0001")
        args = []
        i = lower_rng
        while i <= upper_rng:
            args.append(i)
            i += increment
        try:
            func_args = [self.function_call_handler(Datatypes.FuncCallNode(function, [arg])) for arg in args]
        except TypeError:
            raise TypeError("Only functions with exactly one argument can be plotted.")
        arg_arr = np.array(args)
        func_arg_arr = np.array(func_args)
        plt.rcParams["figure.autolayout"] = True
        plt.grid(visible=True, which="major", axis="both")
        plt.plot(arg_arr, func_arg_arr, c="orange", label=f"f(x)={function}(x)")
        plt.axvline(x=0)
        plt.axhline(y=0)
        plt.legend()
        plt.show()
