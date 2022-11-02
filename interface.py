from lexer import Lexer
from parse import Parser
from interpreter import Interpreter
import Datatypes
# TODO: add custom and more precise exceptions (i.e. store token positions)


class Interface:
    def __init__(self, debug=False, quit_after_exceptions=False, printall=False):
        self.inp_msg = ">> "
        self.interpreter = Interpreter()
        self.debug = debug
        self.quit_after_exceptions = quit_after_exceptions
        self.tokens_list = []
        self.open_blocks = 0
        self.active_if = False
        self.printall = printall
        self.inp = ""

    # debug: Will print lexer output and parser output additionally
    # quit_after_exceptions: Will prevent program from quitting after reaching an exception.
    def start_session(self):

        while True:
            try:
                self.inp = input(self.inp_msg)
            except KeyboardInterrupt:
                exit(0)
            if self.quit_after_exceptions:
                out = self.get_out()
                self.print_output(out)
            else:
                # This will do the same exact thing as the block above, but will catch any exceptions coming through
                # To make this possible, all fields are backed up, so they can be reverted to their original states
                # in case of an exception
                self.interpreter.backup_fields = self.interpreter.fields.copy()
                try:
                    out = self.get_out()
                except Exception as e:
                    self.interpreter.rollback()
                    print(f"{type(e).__name__}: {e}")
                    self.tokens_list = []
                    self.active_if = False
                    self.open_blocks = 0
                else:
                    self.print_output(out)

    def get_out(self):
        lexer = Lexer(self.inp)
        tokens = lexer.gen_tokens()
        for token in tokens:
            self.tokens_list.append(token)
        self.tokens_list.append(Datatypes.Token(Datatypes.LINEBREAK))
        if len(tokens) == 0:
            self.inp_msg = ">> "
            self.active_if = False
            self.open_blocks = 0
        else:
            for token in tokens:
                if token.type in (Datatypes.ARROW, Datatypes.LCURLY):
                    if token.type == Datatypes.ARROW and tokens[-1].type != Datatypes.ARROW:
                        continue
                    else:
                        self.open_blocks += 1
                elif token.type in (Datatypes.BLOCK_END, Datatypes.RCURLY):
                    self.open_blocks -= 1
                elif token.type == Datatypes.IF:
                    self.active_if = True
                elif token.type == Datatypes.ELSE:
                    self.active_if = False
            if self.open_blocks > 0 or self.active_if:
                self.inp_msg = ".. "
                return [None]
            else:
                self.inp_msg = ">> "
        if self.debug:
            for tokens in self.tokens_list:
                print(tokens)
        parser = Parser(self.tokens_list)
        ast_list = parser.parse()
        if self.debug:
            print(ast_list)
        self.tokens_list = []
        return self.interpreter.get_output(ast_list)

    # Instead of starting an interpreter session, this function will simply
    # get the output from any input string and print the output

    def run(self, input_string, return_out=False):
        lexer = Lexer(input_string)
        tokens = lexer.gen_tokens()
        if self.debug:
            for token in tokens:
                if token.type == Datatypes.LINEBREAK:
                    print()
                else:
                    print(token, "; ", end="")
            print()
        parser = Parser(tokens)
        ast_list = parser.parse()
        if self.debug:
            print(ast_list)
        output_lines = self.interpreter.get_output(ast_list, self.printall)
        if return_out:
            return output_lines
        else:
            self.print_output(output_lines)

    def run_from_file(self, filepath):
        with open(filepath) as program:
            program = program.read()
        self.run(program)

    def print_output(self, output_lines):
        # Printing the result
        # Won't print anything if the result is None#
        for line in output_lines:
            if line is not None:
                print(line)


def quit():
    exit()


if __name__ == '__main__':
    interface = Interface()
    interface.start_session()
