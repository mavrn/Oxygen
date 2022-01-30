from lexer import Lexer
from parse import Parser
from interpreter import Interpreter
import Datatypes
from fractions import Fraction


# TODO: add custom exceptions


# debug: Will print lexer output and parser output additionally
# quit_after_exceptions: Will prevent program from quitting after reaching an exception.
def start_session(debug=False, quit_after_exceptions=False):
    interpreter = Interpreter()
    while True:
        inp = input(">>")
        if quit_after_exceptions:
            # Will go through the interpreting process and print the interim results if debug is set to True
            lexer = Lexer(inp)
            tokens_list = lexer.gen_tokens()
            if debug:
                for tokens in tokens_list:
                    print(tokens)
            parser = Parser(tokens_list)
            tree_list = parser.parse()
            if debug:
                print(tree_list)
            output_lines = interpreter.get_output(tree_list)
        else:
            # This will do the same exact thing as the block above, but will catch any exceptions coming through
            # To make this possible, all fields are backed up, so they can be reverted to their original states
            # in case of an exception
            interpreter.backup_fields = interpreter.fields.copy()
            try:
                lexer = Lexer(inp)
                tokens_list = lexer.gen_tokens()
                if debug:
                    for tokens in tokens_list:
                        print(tokens)
                parser = Parser(tokens_list)
                tree_list = parser.parse()
                if debug:
                    print(tree_list)
                output_lines = interpreter.get_output(tree_list)
            except Exception as e:
                interpreter.rollback()
                print(f"{type(e).__name__}: {e}")
                output_lines = [None]

        # Printing the result
        # Won't print anything if the result is None
        for line in output_lines:
            if line is not None:
                # Running some instance checks to make sure that the right thing is printed to the console
                if isinstance(line, Fraction):
                    print(str(line))
                elif isinstance(line, float):
                    # Will print result without decimals in case of a whole number
                    if line % 1 == 0:
                        print(int(line))
                    else:
                        print(line)
                else:
                    print(repr(line))


if __name__ == '__main__':
    start_session()
