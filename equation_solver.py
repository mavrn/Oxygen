# WORK IN PROGRESS

import Datatypes

solver_dict = {"AddNode": Datatypes.SubNode, "SubNode": Datatypes.AddNode, "MultNode": Datatypes.DivNode,
    "DivNode": Datatypes.MultNode, }


def solve(left_expr, right_expr):
    left_type = type(left_expr).__name__
    right_type = type(right_expr).__name__
    if left_type == "VariableNode":
        return left_expr, right_expr
    elif right_type == "VariableNode":
        return right_expr, left_expr
    if left_type != "float":
        if left_type == "ExpNode" and left_expr.b == 2:
            return solve(left_expr.a, Datatypes.FuncCallNode("sqrt", [right_expr]))
        elif left_type in ("AddNode", "MultNode"):
            if type(left_expr.a).__name__ == "VariableNode":
                variable = left_expr.a
                other = left_expr.b
            else:
                variable = left_expr.b
                other = left_expr.a
            return solve(variable, solver_dict.get(left_type)(right_expr, other))
        elif left_type in ("SubNode", "DivNode"):
            variable = left_expr.a
            other = left_expr.b
            return solve(variable, solver_dict.get(left_type)(right_expr, other))
    else:
        return solve(right_expr, left_expr)
