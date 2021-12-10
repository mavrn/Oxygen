import math

variables = {}


def evaluate(node):
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
    elif type(node).__name__ == "AssignNode":
        assignment_value = evaluate(node.value)
        variables[node.identifier] = assignment_value
        return assignment_value
    elif type(node).__name__ == "VariableNode":
        value = variables.get(node.identifier)
        if value is None:
            print(f"Name \"{node.identifier}\" is not defined.")
        else:
            return value
    elif type(node).__name__ == "ExpNode":
        return evaluate(node.a) ** evaluate(node.b)
    elif type(node).__name__ == "KeywordNode":
        return keyword_handler(node)
    else:
        return node


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
        if node.value % 1 == 0:
            return math.factorial(int(evaluate(node.value)))
        else:
            raise TypeError(f"Expected type int, got type {type(node.value).__name__}")
    else:
        raise Exception(f"Unknown exception occurred while handling the keyword {keyword}")
