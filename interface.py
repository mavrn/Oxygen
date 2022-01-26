from fractions import Fraction

from Tokens import type_dict
from interpreter import evaluate
from lexer import Lexer, token
from parse import Parser


# TODO: add custom exceptions


# fractions: Will convert the output into an approximate fraction
# debug: Will print lexer output and parser output additionally
# quit_after_exceptions: Will prevent program from quitting after reaching an exception.
# Setting this to False is experimental and can lead to unexpected behaviour
def start_session(fractions=False, debug=False, quit_after_exceptions=True):
    while True:
        inp = input(">>")
        if quit_after_exceptions:
            # Will go through the interpreting process and print the interim results if debug is set to True
            lexer = Lexer(inp)
            tokens = lexer.gen_tokens()
            if debug:
                print(token_readable(tokens))
            parser = Parser(tokens)
            tree = parser.parse()
            if debug:
                print(tree)
            result = evaluate(tree)
        else:
            # This will do the same exact thing as the block above, but will catch any exceptions coming through
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
                print(f"{type(e).__name__}: {e}")
                result = None

        # Printing the result
        # Won't print anything if the result is None
        if result is not None:
            if isinstance(result, str):
                print(result)
            elif not isinstance(result, float):
                print("Object:", repr(result))
            # Will print result without decimals in case of a whole number
            elif result % 1 == 0:
                print(int(result))
            else:
                if fractions:
                    # Prints an approximate fraction if fractions is set to True
                    print(str(Fraction(result).limit_denominator()))
                else:
                    print(result)


# For debug purposes
# Makes the lexer tokens readable by matching the IDs to the Tokens.type_dict
def token_readable(tokens):
    readable_tokens = [token(
        type_dict.get(unreadable_token.type),
        unreadable_token.value)
        for unreadable_token in tokens]
    return readable_tokens


if __name__ == '__main__':
    start_session()
