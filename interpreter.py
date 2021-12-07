def evaluate(tree):
    if type(tree).__name__ == "AddNode":
        return evaluate(tree.n1) + evaluate(tree.n2)
    elif type(tree).__name__ == "SubNode":
        return evaluate(tree.n1) - evaluate(tree.n2)
    elif type(tree).__name__ == "MultNode":
        return evaluate(tree.n1) * evaluate(tree.n2)
    elif type(tree).__name__ == "DivNode":
        return evaluate(tree.n1) / evaluate(tree.n2)
    else:
        return tree
