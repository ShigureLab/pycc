import argparse

# from pycc.vm import VirtualMachine, Instruction, c_pointer_to_string, c_pointer_to_integer
from pycc.lexer import Token, match_comments, match_whitespace, Lexer
from pycc.lexer import Int
from pycc.parser import Parser
from pycc.utils import logger


def main():
    parser = argparse.ArgumentParser("pycc", description="A simple C compiler.")
    parser.add_argument("-s", dest="assembly", action="store_true", help="Compile to assembly.")
    parser.add_argument("-d", dest="debug", action="store_true", help="Enable debug mode.")
    parser.add_argument("src", type=str, help="Path to source file")
    args, extra_args = parser.parse_known_args()
    if extra_args:
        logger.info("Extra arguments: ", " ".join(extra_args))

    # 读入源代码
    with open(args.src, "r") as f:
        source_code = f.read()

    # 词法分析
    lexer = Lexer(source_code)
    token_stream: list[Token] = []
    # for token in lexer:
    #     token_stream.append(token)
    token_stream = lexer.tokenize()
    print(token_stream)
    # 语法分析
    parser = Parser(source_code, debug=True)
    print(parser.sum_expr())


if __name__ == "__main__":
    main()
