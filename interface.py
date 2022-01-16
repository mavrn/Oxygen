from interpreter import evaluate
from lexer import Lexer, token
from parse import Parser
from Tokens import type_dict
from fractions import Fraction


# TODO: add comments
# TODO: add custom exceptions
# BUG: Case a(sqrt(x)) unexpected Exception


def start_session(fractions=False, debug=False):
    while True:
        inp = input(">>")
        lexer = Lexer(inp)
        tokens = lexer.gen_tokens()
        if debug:
            print(token_readable(tokens))
        parser = Parser(tokens)
        tree = parser.parse()
        if debug:
            print(tree)
        result = evaluate(tree)
        if result is not None:
            if result % 1 == 0:
                print(int(result))
            else:
                if fractions:
                    print(str(Fraction(result).limit_denominator()))
                else:
                    print(result)


# Debug
def token_readable(tokens):
    readable_tokens = []
    for unreadable_token in tokens:
        readable_token = token(type_dict.get(unreadable_token.type), unreadable_token.value)
        readable_tokens.append(readable_token)
    return readable_tokens


if __name__ == '__main__':
    start_session()
