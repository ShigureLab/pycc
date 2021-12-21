import argparse

from pycc.vm import VirtualMachine, test_cython_connect


def test_python_code():
    test_cython_connect(1)
    print("test_python_code in python code.")


def test_vm():
    vm = VirtualMachine(256 * 1024)


def main():
    # Just for test.
    test_python_code()
    test_vm()

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
