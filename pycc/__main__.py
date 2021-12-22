import argparse

from pycc.vm import VirtualMachine, Instruction, c_pointer_to_string


def main():
    # Just for test.
    # test_vm()

    parser = argparse.ArgumentParser("pycc", description="A simple C compiler.")
    parser.add_argument("-s", dest="assembly", action="store_true", help="Compile to assembly.")
    parser.add_argument("-d", dest="debug", action="store_true", help="Enable debug mode.")
    parser.add_argument(
        "src",
        type=str,
    )
    args, extra_args = parser.parse_known_args()
    if extra_args:
        print("[INFO] Extra arguments: ", " ".join(extra_args))


if __name__ == "__main__":
    main()
