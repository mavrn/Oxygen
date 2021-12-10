from interpreter import evaluate
from lexer import Lexer
from parse import Parser

if __name__ == '__main__':
    while True:
        inp = input(">>")
        lexer = Lexer(inp)
        tokens = lexer.gen_tokens()
        #print(tokens)
        parser = Parser(tokens)
        tree = parser.parse()
        #print(tree)
        result = evaluate(tree)
        if result is not None:
            if result % 1 == 0:
                print(int(result))
            else:
                print(result)
