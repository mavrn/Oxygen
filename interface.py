from lexer import Lexer
from parse import Parser
from interpreter import Interpreter
import Datatypes
from fractions import Fraction

# TODO: add custom exceptions
# TODO: turn into class

inp_msg = ">> "
interpreter = Interpreter()


# debug: Will print lexer output and parser output additionally
# quit_after_exceptions: Will prevent program from quitting after reaching an exception.
def start_session(debug=False, quit_after_exceptions=False):
    global inp_msg
    while True:
        inp = input(inp_msg)
        if quit_after_exceptions:
            out = get_out(inp, debug)
            print_output(out)
        else:
            # This will do the same exact thing as the block above, but will catch any exceptions coming through
            # To make this possible, all fields are backed up, so they can be reverted to their original states
            # in case of an exception
            interpreter.backup_fields = interpreter.fields.copy()
            try:
                out = get_out(inp, debug)
            except Exception as e:
                interpreter.rollback()
                print(f"{type(e).__name__}: {e}")
                print_output([None])
            else:
                print_output(out)


def get_out(inp, debug):
    global inp_msg
    tokens_list = []
    open_blocks = 0
    lexer = Lexer(inp)
    tokens = lexer.gen_tokens()
    for token in tokens:
        tokens_list.append(token)
    if len(tokens) == 0:
        inp_msg = ">> "
        for _ in range(open_blocks):
            tokens_list[-1].append(Datatypes.Token(Datatypes.BLOCK_END))
    else:
        if tokens[0][0].type == Datatypes.ELSE and open_blocks > 0:
            open_blocks -= 1
            tokens_list[-2].append(Datatypes.Token(Datatypes.BLOCK_END))
        if tokens[-1][-1].type == Datatypes.BLOCK_END:
            open_blocks -= 1
            inp_msg = ">> "
        if tokens[-1][-1].type == Datatypes.ARROW:
            open_blocks += 1
        if open_blocks > 0:
            inp_msg = ".. "
            return
    if debug:
        for tokens in tokens_list:
            print(tokens)
    parser = Parser(tokens_list)
    ast_list = parser.parse()
    if debug:
        print(ast_list)
    return interpreter.get_output(ast_list)
# Instead of starting an interpreter session, this function will simply
# get the output from any input string and print the output
def run(input_string, debug=False):
    interpreter = Interpreter()
    lexer = Lexer(input_string)
    tokens_list = lexer.gen_tokens()
    if debug:
        for tokens in tokens_list:
            print(tokens)
    parser = Parser(tokens_list)
    ast_list = parser.parse()
    if debug:
        print(ast_list)
    output_lines = interpreter.get_output(ast_list)
    print_output(output_lines)


def print_output(output_lines):
    # Printing the result
    # Won't print anything if the result is None
    for line in output_lines:
        if line is not None:
            # Running some instance checks to make sure that the right thing is printed to the console
            if isinstance(line, Fraction):
                print(str(line))
            elif isinstance(line, float):
                print(Datatypes.String(line))
            elif isinstance(line, (Datatypes.Bool, Datatypes.String)):
                print(line)
            else:
                print(repr(line))


if __name__ == '__main__':
    start_session()
