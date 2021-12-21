from pycc.vm import test_cython_connect, VirtualMachine


def test_python_code():
    test_cython_connect(1)
    print("test_python_code in python code.")


def test_vm():
    vm = VirtualMachine(256 * 1024)


def main():
    test_python_code()
    test_vm()


if __name__ == "__main__":
    main()
