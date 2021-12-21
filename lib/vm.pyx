from libvm cimport test_cpp_connect
from libvm cimport reset_vm
from libvm cimport free_vm
from libvm cimport init_vm
from libvm cimport run_vm

cdef _test_cython_connect(int n):
    test_cpp_connect(n)
    print("test_cython_connect in cython code.")

def test_cython_connect(n: int):
    _test_cython_connect(n)

cdef class VirtualMachine:
    cdef int poolsize
    def __cinit__(self, int poolsize):
        self.poolsize = poolsize
        init_vm(poolsize)

    def reset(self):
        reset_vm(self.poolsize)

    def run(self, debug: bool):
        return run_vm(debug)

    def __dealloc__(self):
        free_vm()
