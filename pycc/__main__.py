from pycc.core import test_cython_connect


def test_python_code():
    test_cython_connect(1)
    print("test_python_code in python code.")


def main():
    test_python_code()


if __name__ == "__main__":
    main()
