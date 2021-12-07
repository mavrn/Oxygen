from lexer import Lexer
from parse import Parser
from interpreter import evaluate


if __name__ == '__main__':
   while True:
        inp = input(">>")
        lexer = Lexer(inp)
        tokens = lexer.gen_tokens()
        print(tokens)
        parser = Parser(tokens)
        tree = parser.parse()
        print(tree)
        print(evaluate(tree))

