from lexer import Lexer
from parse import Parser
from interpreter import Interpreter
import Datatypes


# TODO: add custom exceptions


# fractions: Will convert the output into an approximate fraction
# debug: Will print lexer output and parser output additionally
# quit_after_exceptions: Will prevent program from quitting after reaching an exception.
# Setting this to False is experimental and can lead to unexpected behaviour
def start_session(debug=False, quit_after_exceptions=False):
    interpreter = Interpreter()
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
            result = interpreter.evaluate(tree)
        else:
            # This will do the same exact thing as the block above, but will catch any exceptions coming through
            # To make this possible, all fields are backed up, so they can be reverted to their original states
            # in case of an exception
            interpreter.backup_global_fields = interpreter.global_fields.copy()
            interpreter.backup_local_fields = interpreter.local_fields.copy()
            try:
                lexer = Lexer(inp)
                tokens = lexer.gen_tokens()
                if debug:
                    print(token_readable(tokens))
                parser = Parser(tokens)
                tree = parser.parse()
                if debug:
                    print(tree)
                result = interpreter.evaluate(tree)
            except Exception as e:
                interpreter.revert()
                print(f"{type(e).__name__}: {e}")
                result = None

        # Printing the result
        # Won't print anything if the result is None
        if result is not None:
            if isinstance(result, (str, Datatypes.Bool)):
                print(result)
            elif isinstance(result, float):
                if result % 1 == 0:
                    print(int(result))
                else:
                    print(result)
            elif not isinstance(result, float):
                print("Object:", repr(result))
            # Will print result without decimals in case of a whole number


# For debug purposes
# Makes the lexer tokens readable by matching the IDs to the Tokens.type_dict
def token_readable(tokens):
    readable_tokens = [Datatypes.token(
        Datatypes.type_dict.get(unreadable_token.type),
        unreadable_token.value)
        for unreadable_token in tokens]
    return readable_tokens


if __name__ == '__main__':
    start_session()
