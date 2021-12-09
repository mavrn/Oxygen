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
        variables[node.identifier] = evaluate(node.value)
    elif type(node).__name__ == "VariableNode":
        value = variables.get(node.identifier)
        if value is None:
            print(f"Name \"{node.identifier}\" is not defined.")
        else:
            return value
    else:
        return node
