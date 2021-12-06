from lexer import Lexer
from parse import Parser


if __name__ == '__main__':
    while True:
        inp = input(">>")
        lexer = Lexer(inp)
        tokens = lexer.gen_tokens()
        print(tokens)
        parser = Parser(tokens)
        print(parser.parse())

