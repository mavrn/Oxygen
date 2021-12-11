from interpreter import evaluate
from lexer import Lexer, token
from parse import Parser
from Tokens import type_dict


# TODO: add comments
# TODO: add custom exceptions


def main():
    while True:
        inp = input(">>")
        lexer = Lexer(inp)
        tokens = lexer.gen_tokens()
        # print(token_readable(tokens))
        parser = Parser(tokens)
        tree = parser.parse()
        # print(tree)
        result = evaluate(tree)
        if result is not None:
            if result % 1 == 0:
                print(int(result))
            else:
                print(result)


# Debug
def token_readable(tokens):
    readable_tokens = []
    for unreadable_token in tokens:
        readable_token = token(type_dict.get(unreadable_token.type), unreadable_token.value)
        readable_tokens.append(readable_token)
    return readable_tokens


if __name__ == '__main__':
    main()
