from interpreter import evaluate
from lexer import Lexer, token
from parse import Parser
from Tokens import type_dict
from fractions import Fraction
import traceback


# TODO: add comments
# TODO: add custom exceptions


def start_session(fractions=False, debug=False, dont_quit_after_exceptions=False):
    while True:
        inp = input(">>")
        if dont_quit_after_exceptions:
            try:
                lexer = Lexer(inp)
                tokens = lexer.gen_tokens()
                if debug:
                    print(token_readable(tokens))
                parser = Parser(tokens)
                tree = parser.parse()
                if debug:
                    print(tree)
                result = evaluate(tree)
            except Exception as e:
                print(e)
                result = None
        else:
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
            if isinstance(result, str):
                print(result)
            elif result % 1 == 0:
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
