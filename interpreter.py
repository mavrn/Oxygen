import math
from collections import namedtuple

function = namedtuple("function", ["arguments", "body"])
global_fields = {"pi": math.pi, "e": math.e}
local_fields = {}
OperationNodes = ["AddNode", "SubNode", "MultNode", "DivNode", "ModulusNode", "ExpNode"]
KEYWORDS = ["sin", "cos", "tan", "asin", "acos", "atan", "abs", "sqrt", "factorial"]


def evaluate(node, scope="global"):
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
        if scope == "local":
            assignment_value = evaluate(node.value, scope="local")
            local_fields[node.identifier] = assignment_value
            return assignment_value
        elif scope == "global":
            assignment_value = evaluate(node.value)
            global_fields[node.identifier] = assignment_value
            return assignment_value
        else:
            raise Exception("An unknown exception occured.")
    elif node_type == "VariableNode":
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


def function_call_handler(node):
    func = global_fields.get(node.identifier)
    if func is None:
        if node.identifier in KEYWORDS:
            return keyword_handler(node)
        else:
            raise NameError(f"No callable function found with name {node.identifier}")
    arguments = node.arguments
    if len(arguments) != len(func.arguments):
        raise TypeError(
            f"Expected {len(func.arguments)} arguments for function {node.identifier}, got {len(arguments)}.")
    for i, argument in enumerate(arguments):
        local_fields[func.arguments[i]] = evaluate(argument, "local")
    result = evaluate(func.body)
    local_fields.clear()
    return result


def keyword_handler(node):
    keyword = node.identifier
    if len(node.arguments) != 1:
        raise SyntaxError(f"Expected 1 argument, got {len(node.arguments)}")
    argument = evaluate(node.arguments[0])
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


def operation_handler(node):
    node_type = type(node).__name__
    if node_type == "AddNode":
        return evaluate(node.a) + evaluate(node.b)
    elif node_type == "SubNode":
        return evaluate(node.a) - evaluate(node.b)
    elif node_type == "MultNode":
        return evaluate(node.a) * evaluate(node.b)
    elif node_type == "DivNode":
        return evaluate(node.a) / evaluate(node.b)
    elif node_type == "ModulusNode":
        return evaluate(node.a) % evaluate(node.b)
    elif node_type == "ExpNode":
        return evaluate(node.a) ** evaluate(node.b)
