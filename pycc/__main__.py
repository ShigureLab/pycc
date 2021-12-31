import argparse

# from pycc.vm import VirtualMachine, Instruction, c_pointer_to_string, c_pointer_to_integer
from pycc.lexer import Token


def main():
    parser = argparse.ArgumentParser("pycc", description="A simple C compiler.")
    parser.add_argument("-s", dest="assembly", action="store_true", help="Compile to assembly.")
    parser.add_argument("-d", dest="debug", action="store_true", help="Enable debug mode.")
    parser.add_argument("src", type=str, help="Path to source file")
    args, extra_args = parser.parse_known_args()
    if extra_args:
        print("[INFO] Extra arguments: ", " ".join(extra_args))

    with open(args.src, "r") as f:
        source_code = f.read()

    i = 0
    token_stream: list[Token] = []
    while i < len(source_code):
        for token_cls in Token.token_classes():
            if match_obj := token_cls.match(source_code, i):
                match_str = match_obj.group(0)
                i += len(match_str)
                token_stream.append(token_cls(match_str))
        else:
            i += 1
    print(token_stream)


if __name__ == "__main__":
    main()
