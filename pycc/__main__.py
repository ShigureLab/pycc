import argparse

# from pycc.vm import VirtualMachine, Instruction, c_pointer_to_string, c_pointer_to_integer
from pycc.lexer import Token, match_comments, match_whitespace


def main():
    parser = argparse.ArgumentParser("pycc", description="A simple C compiler.")
    parser.add_argument("-s", dest="assembly", action="store_true", help="Compile to assembly.")
    parser.add_argument("-d", dest="debug", action="store_true", help="Enable debug mode.")
    parser.add_argument("src", type=str, help="Path to source file")
    args, extra_args = parser.parse_known_args()
    if extra_args:
        print("[INFO] Extra arguments: ", " ".join(extra_args))

    # 读入源代码
    with open(args.src, "r") as f:
        source_code = f.read()

    # 词法分析
    i = 0
    token_stream: list[Token] = []
    while i < len(source_code):
        print(source_code[i])
        # 匹配并跳过注释
        if match_obj := match_comments(source_code, i):
            comments = match_obj.group(0)
            i += len(comments)
            continue

        # 匹配并跳过空白字符
        if match_obj := match_whitespace(source_code, i):
            whitespace = match_obj.group(0)
            i += len(whitespace)
            continue

        # 匹配各种 token
        continue_flag = False
        for token_cls in Token.token_classes():
            if match_obj := token_cls.match(source_code, i):
                match_str = match_obj.group(0)
                i += len(match_str)
                token_stream.append(token_cls(match_str))
                # Python 无法直接跳出两层，因此通过 flag 来处理
                continue_flag = True
                continue
        if continue_flag:
            continue

        # 未预期的符号
        else:
            # i += 1
            raise Exception(f"Unexpected symbol: {source_code[i]}")
    print(token_stream)


if __name__ == "__main__":
    main()
