import Datatypes
from interpreter import Interpreter
from lexer import Lexer
from parse import Parser
from collections import deque
import os



class Interface:
    def __init__(self, debug=False, quit_after_exceptions=False, printall=False, autoid=False):
        self.inp_msg = ">> "
        self.interpreter = Interpreter(autoid)
        self.debug = debug
        self.quit_after_exceptions = quit_after_exceptions
        self.printall = printall
        self.tokens_list = deque()
        self.open_blocks = 0
        self.open_if_blocks = deque()

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
                    self.tokens_list.clear()
                    self.active_if = False
                    self.open_blocks = 0
                else:
                    print_output(out)

    def get_out(self, user_input):
        tokens = Lexer(user_input).gen_tokens()
        token_types = [t.type for t in tokens]
        self.tokens_list.extend(tokens)
        self.tokens_list.append(Datatypes.Token(Datatypes.LINEBREAK))
        if len(tokens) == 0:
            if self.open_blocks == 0:
                self.inp_msg = ">> "
                self.open_if_blocks = deque()
            else:
                return []
        else:
            if token_types[0] not in (Datatypes.OR, Datatypes.ELSE) and self.open_if_blocks and self.open_blocks == self.open_if_blocks[-1]:
                self.open_if_blocks.pop()
            if token_types[0] in (Datatypes.IF, Datatypes.UNLESS):
                self.open_if_blocks.append(self.open_blocks)
            elif token_types[0] == Datatypes.ELSE:
                self.open_if_blocks.pop()
            if token_types[-1] in (Datatypes.ARROW, Datatypes.ITERATE_ARROW):
                self.open_blocks += 1
            self.open_blocks -= token_types.count(Datatypes.BLOCK_END)
            if self.open_blocks > 0 or self.open_if_blocks or token_types[-1] == Datatypes.COMMA:
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
        self.tokens_list = deque()
        result, loadreq = self.interpreter.get_output(ast_list, printall=self.printall)
        if loadreq:
            old = self.printall
            self.printall = False
            for req in loadreq:
                self.run_from_file(req)
            self.printall = old
        return result

    def run(self, input_string, return_out=False):
        lines = input_string.split("\n")
        output_lines = deque()
        out = deque()
        for line in lines:
            try:
                out = self.get_out(line)
            except Exception as e:
                print_output(self.interpreter.output_lines)
                raise e
            finally:
                if return_out:
                    output_lines.extend(out)
                else:
                    print_output(out)
        if return_out:
            return list(output_lines)

    def runlegacy(self, input_string, return_out=False):
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
                return list(out)
            else:
                print_output(out)
        except Exception as e:
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
    interface = Interface(quit_after_exceptions=True, autoid=True, printall=True)
    interface.start_session()
