import argparse
import sys

from pycc.lexer import Lexer, Token
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
    with open(args.src, "r", encoding="utf-8") as f:
        source_code = f.read()

    # 词法分析
    lexer = Lexer(source_code)
    token_stream: list[Token] = []
    # for token in lexer:
    #     token_stream.append(token)
    token_stream = lexer.tokenize()
    print("词法分析结果：")
    print(token_stream)
    # 语法分析

    print("语法分析中……")
    parser = Parser(source_code, debug=True)
    ast = parser.start()
    ast.dump("ast.json")

    print("符号表：")
    for key in parser.symbols:
        print(key, ": ", parser.symbols[key])

    print("全部指令：")
    main_ptr = parser.symbols.get_symbol("main").value
    parser.vm.show_ops()
    parser.vm.setup_main(main_ptr)
    print("虚拟机运行中……")
    result = parser.vm.run(True)
    return result


if __name__ == "__main__":
    sys.exit(main())
