from libvm cimport test_cpp_connect

cdef _test_cython_connect(int n):
    test_cpp_connect(n)
    print("test_cython_connect in cython code.")

def test_cython_connect(n: int):
    _test_cython_connect(n)
