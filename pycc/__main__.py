import argparse

from pycc.vm import VirtualMachine, test_cython_connect, Instruction, c_pointer_to_string


def test_python_code():
    test_cython_connect(1)
    print("test_python_code in python code.")


def test_vm():
    poolsize = 256 * 1024
    vm = VirtualMachine(poolsize)

    vm.reset()
    vm.add_op(Instruction.IMM)
    vm.add_op(1)
    vm.add_op(Instruction.PUSH)
    vm.add_op(Instruction.IMM)
    vm.add_op(2)
    vm.add_op(Instruction.ADD)
    vm.add_op(Instruction.PUSH)
    vm.add_op(Instruction.EXIT)
    print(vm.run(True))

    vm.reset()
    vm.add_op(Instruction.IMM)
    vm.add_op("345")
    vm.add_op(Instruction.PUSH)
    vm.add_op(Instruction.EXIT)
    print(c_pointer_to_string(vm.run(True)))

    vm2 = VirtualMachine(poolsize)
    vm2.add_op(Instruction.IMM)
    vm2.add_op(1)
    vm2.add_op(Instruction.PUSH)
    vm2.add_op(Instruction.IMM)
    vm2.add_op(2)
    vm2.add_op(Instruction.ADD)
    vm2.add_op(Instruction.PUSH)
    vm2.add_op(Instruction.EXIT)
    print(vm2.run(True))


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
