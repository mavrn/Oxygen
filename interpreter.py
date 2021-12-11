import math
from collections import namedtuple

function = namedtuple("function", ["arguments", "body"])
fields = {}
OperationNodes = ["AddNode", "SubNode", "MultNode", "DivNode", "ModulusNode", "ExpNode"]


def evaluate(node):
    if type(node).__name__ == "FuncDeclareNode":
        fields[node.identifier] = function(node.arguments, node.body)
    elif type(node).__name__ == "FuncCallNode":
        return function_call_handler(node)
    elif type(node).__name__ in OperationNodes:
        return operation_handler(node)
    elif type(node).__name__ == "AssignNode":
        assignment_value = evaluate(node.value)
        fields[node.identifier] = assignment_value
        return assignment_value
    elif type(node).__name__ == "VariableNode":
        value = fields.get(node.identifier)
        if value is None:
            raise NameError(f"Name \"{node.identifier}\" is not defined.")
        else:
            return value
    elif type(node).__name__ == "KeywordNode":
        return keyword_handler(node)
    else:
        return node


def function_call_handler(node):
    func = fields.get(node.identifier)
    arguments = node.arguments
    for i, argument in enumerate(arguments):
        arguments[i] = evaluate(argument)
    if len(arguments) != len(func.arguments):
        raise SyntaxError(f"Expected {len(func.arguments)} arguments, got {len(arguments)} ")
    for i, argument in enumerate(arguments):
        fields[func.arguments[i]] = argument
    result = evaluate(func.body)
    for argument in func.arguments:
        del fields[argument]
    return result


def keyword_handler(node):
    keyword = node.keyword
    if keyword == "sqrt":
        return math.sqrt(evaluate(node.value))
    elif keyword == "sin":
        return math.sin(evaluate(node.value))
    elif keyword == "cos":
        return math.cos(evaluate(node.value))
    elif keyword == "tan":
        return math.tan(evaluate(node.value))
    elif keyword == "factorial":
        result = evaluate(node.value)
        if result % 1 == 0:
            return math.factorial(int(result))
        else:
            raise TypeError(f"Expected type int, got type {type(node.value).__name__}")
    else:
        raise Exception(f"Unknown exception occurred while handling the keyword {keyword}")


def operation_handler(node):
    if type(node).__name__ == "AddNode":
        return evaluate(node.a) + evaluate(node.b)
    elif type(node).__name__ == "SubNode":
        return evaluate(node.a) - evaluate(node.b)
    elif type(node).__name__ == "MultNode":
        return evaluate(node.a) * evaluate(node.b)
    elif type(node).__name__ == "DivNode":
        return evaluate(node.a) / evaluate(node.b)
    elif type(node).__name__ == "ModulusNode":
        return evaluate(node.a) % evaluate(node.b)
    elif type(node).__name__ == "ExpNode":
        return evaluate(node.a) ** evaluate(node.b)
