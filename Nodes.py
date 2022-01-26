from collections import namedtuple
import Tokens

# Includes all node types
AddNode = namedtuple("AddNode", ["a", "b"])
SubNode = namedtuple("SubNode", ["a", "b"])
MultNode = namedtuple("MultNode", ["a", "b"])
DivNode = namedtuple("DivNode", ["a", "b"])
ModulusNode = namedtuple("ModulusNode", ["a", "b"])
ExpNode = namedtuple("ExpNode", ["a", "b"])
AssignNode = namedtuple("AssignNode", ["identifier", "value"])
VariableNode = namedtuple("VariableNode", ["identifier"])
KeywordNode = namedtuple("KeywordNode", ["keyword", "value"])
FuncDeclareNode = namedtuple("FuncDeclareNode", ["identifier", "arguments", "body"])
FuncCallNode = namedtuple("FuncCallNode", ["identifier", "arguments"])
ComparisonNode = namedtuple("ComparisonNode", ["a", "b", "operator"])


def match_operator_to_node(operator_id):
    id = operator_id
    if id == Tokens.PLUS_ASSIGN:
        return AddNode
    elif id == Tokens.MINUS_ASSIGN:
        return SubNode
    elif id == Tokens.MULT_ASSIGN:
        return MultNode
    elif id == Tokens.DIV_ASSIGN:
        return DivNode
    else:
        return ModulusNode
