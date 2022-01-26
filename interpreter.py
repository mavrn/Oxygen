import math
from collections import namedtuple
import Nodes, Tokens, Datatypes

# Defines a function consisting of the arguments and the body
function = namedtuple("function", ["arguments", "body"])
# Define global and local fields, which emulate global and local (function) scope
global_fields = {"pi": math.pi, "e": math.e, "golden": (1 + 5 ** 0.5) / 2, "h": 6.62607004 * (10 ** (-34))}
local_fields = {}
OperationNodes = ["AddNode", "SubNode", "MultNode", "DivNode", "ModulusNode", "ExpNode"]
KEYWORDS = ["sin", "cos", "tan", "asin", "acos", "atan", "abs", "sqrt", "factorial"]


# Will evaluate the tree (parser output) recursively
def evaluate(node):
    node_type = type(node).__name__
    if node_type == "FuncDeclareNode":
        global_fields[node.identifier] = function(node.arguments, node.body)
        if node.identifier in KEYWORDS:
            return f"Warning: Built-in function {node.identifier} has been overridden."
    elif node_type == "FuncCallNode":
        return function_call_handler(node)
    elif node_type in OperationNodes:
        return operation_handler(node)
    elif node_type == "AssignNode":
        assignment_value = evaluate(node.value)
        global_fields[node.identifier] = assignment_value
        return assignment_value
    elif node_type == "ComparisonNode":
        return comparison_handler(node)
    elif node_type == "BooleanNegationNode":
        bool = evaluate(node.value)
        custom_bool = Datatypes.Bool(bool)
        custom_bool.reverse()
        return custom_bool
    elif node_type == "LogicalOperationNode":
        if node.operation == Tokens.AND:
            return Datatypes.Bool(
                Datatypes.Bool(evaluate(node.a)).boolean_value and Datatypes.Bool(evaluate(node.b)).boolean_value)
        else:
            return Datatypes.Bool(
                Datatypes.Bool(evaluate(node.a)).boolean_value or Datatypes.Bool(evaluate(node.b)).boolean_value)
    elif node_type == "VariableNode":
        # Will check for a local field first, then a global one, and finally raise an exception if
        global_value = global_fields.get(node.identifier)
        local_value = local_fields.get(node.identifier)
        if local_value is not None:
            return local_value
        elif global_value is not None:
            return global_value
        else:
            raise NameError(f"Name \"{node.identifier}\" is not defined.")
    elif node_type == "KeywordNode":
        return keyword_handler(node)
    else:
        return node


# Will handle all nodes of type FuncCallNode
def function_call_handler(node):
    # Fetches the function and its name from the global fields
    func = global_fields.get(node.identifier)
    node_type = type(func).__name__
    # If none is found, the function might be a built-in one. If not, an error will be risen
    if func is None:
        if node.identifier in KEYWORDS:
            return keyword_handler(node)
        else:
            raise NameError(f"No callable function found with name {node.identifier}")
    # If the field previously fetched is not a function (i.e. a float value), an error will be risen
    elif node_type != "function":
        raise TypeError(f"{node_type} object is not callable")
    # The arguments the user has called the function with are saved
    arguments = node.arguments
    # The numbers of the called and defined arguments have to match, else an error will be risen
    if len(arguments) != len(func.arguments):
        raise TypeError(
            f"Expected {len(func.arguments)} arguments for function {node.identifier}, got {len(arguments)}.")
    # The arguments the function was called with are now assigned
    # with the names and order they were previously defined in the function.
    # The arguments will be assigned to the local fields
    for i, argument in enumerate(arguments):
        local_fields[func.arguments[i]] = evaluate(argument)
    # Now that the variables are assigned, the function body can be evaluated
    result = evaluate(func.body)
    # Local fields will be cleared after the function ends, just like in any other language
    local_fields.clear()
    return result


# Will handle any type of KeywordNode
def keyword_handler(node):
    keyword = node.identifier
    # As all the built-in functions only accept one argument,
    # so the program raises an error if called with more or less arguments
    if len(node.arguments) != 1:
        raise SyntaxError(f"Expected 1 argument, got {len(node.arguments)}")
    argument = evaluate(node.arguments[0])
    # Will match the identifier to the pre-defined keywords and operate accordingly
    if keyword == "sqrt":
        return math.sqrt(argument)
    elif keyword == "sin":
        return math.sin(argument)
    elif keyword == "cos":
        return math.cos(argument)
    elif keyword == "tan":
        return math.tan(argument)
    elif keyword == "factorial":
        if argument % 1 == 0:
            return math.factorial(int(argument))
        else:
            raise TypeError(f"Expected type int, got type {type(argument).__name__}")
    elif keyword == "asin":
        return math.asin(argument)
    elif keyword == "acos":
        return math.acos(argument)
    elif keyword == "atan":
        return math.atan(argument)
    elif keyword == "abs":
        return abs(argument)
    else:
        raise Exception(f"Unknown exception occurred while handling the keyword {keyword}")


# Will handle any type of simple operation
def operation_handler(node):
    node_type = type(node).__name__
    a = evaluate(node.a)
    b = evaluate(node.b)
    if not isinstance(a, float):
        raise TypeError("Cannot use mathematical operations on object of type " + type(a).__name__)
    if not isinstance(b, float):
        raise TypeError("Cannot use mathematical operations on object of type " + type(b).__name__)
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
def comparison_handler(node):
    operator = node.operator
    a = evaluate(node.a)
    b = evaluate(node.b)
    if not isinstance(a, float):
        raise TypeError("Cannot operate on object of type " + type(a).__name__)
    if not isinstance(b, float):
        raise TypeError("Cannot operate on object of type " + type(b).__name__)
    if operator == Tokens.COMP_EQUALS:
        return Datatypes.Bool(a == b)
    elif operator == Tokens.COMP_NOT_EQUALS:
        return Datatypes.Bool(a != b)
    elif operator == Tokens.GREATER_THAN:
        return Datatypes.Bool(a > b)
    elif operator == Tokens.LESS_THAN:
        return Datatypes.Bool(a < b)
    elif operator == Tokens.GREATER_OR_EQUALS:
        return Datatypes.Bool(a >= b)
    elif operator == Tokens.LESS_OR_EQUALS:
        return Datatypes.Bool(a <= b)
    else:
        raise Exception("An unknown error occurred")
