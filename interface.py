import Datatypes
from interpreter import Interpreter
from lexer import Lexer
from parse import Parser

class Interface:
    def __init__(self, debug=False, quit_after_exceptions=False, printall=False, autoid=False):
        self.inp_msg = ">> "
        self.interpreter = Interpreter(autoid)
        self.debug = debug
        self.quit_after_exceptions = quit_after_exceptions
        self.printall = printall
        self.tokens_list = []
        self.open_blocks = 0
        self.active_if = False

    def start_session(self):
        while True:
            try:
                user_input = input(self.inp_msg)
            except KeyboardInterrupt:
                exit(0)
            if self.quit_after_exceptions:
                try:
                    out = self.get_out(user_input)
                    print_output(out)
                except Exception as e:
                    out = self.interpreter.output_lines
                    print_output(out)
                    raise(e)
            else:
                self.interpreter.backup_fields = self.interpreter.fields.copy()
                try:
                    out = self.get_out(user_input)
                except Exception as e:
                    print_output(self.interpreter.output_lines)
                    self.interpreter.rollback()
                    print(f"{type(e).__name__}: {e}")
                    self.tokens_list = []
                    self.active_if = False
                    self.open_blocks = 0
                else:
                    print_output(out)

    def get_out(self, user_input):
        lexer = Lexer(user_input)
        tokens = lexer.gen_tokens()
        self.tokens_list.extend(tokens)
        self.tokens_list.append(Datatypes.Token(Datatypes.LINEBREAK))
        if len(tokens) == 0:
            self.inp_msg = ">> "
            self.active_if = False
            self.open_blocks = 0
        else:
            for token in tokens:
                if token.type in (Datatypes.ARROW, Datatypes.ITERATE_ARROW):
                    if token.type in (Datatypes.ARROW, Datatypes.ITERATE_ARROW) and tokens[-1].type not in (Datatypes.ARROW, Datatypes.ITERATE_ARROW):
                        continue
                    else:
                        self.open_blocks += 1
                elif token.type == Datatypes.BLOCK_END:
                    self.open_blocks -= 1
                elif token.type == Datatypes.IF:
                    self.active_if = True
                elif token.type == Datatypes.ELSE:
                    self.active_if = False
            if self.open_blocks > 0 or self.active_if:
                self.inp_msg = ".. "
                return []
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
        try:
            out = self.interpreter.get_output(ast_list, printall=self.printall)
            if return_out:
                return out
            else:
                print_output(out)
        except Exception as e:
            if not return_out:
                print_output(self.interpreter.output_lines)
            raise(e)

    def run_from_file(self, filepath):
        with open(filepath) as program:
            program = program.read()
        self.run(program)


def print_output(output_lines):
    for line in output_lines:
        print(line) 

if __name__ == '__main__':
    interface = Interface()
    interface.start_session()
