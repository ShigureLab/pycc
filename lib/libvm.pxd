from libcpp cimport bool

# cdef extern from "libvm.hpp" namespace "vm":


cdef extern from "libvm.hpp" namespace "vm":
    cdef enum Status:
        OK = 0
        MEMORY_ERROR = 1
    ctypedef long long int64
    bool test_cpp_connect(int)
    Status init_vm(int)
    void reset_vm(int)
    void free_vm()
    int64 run_vm(bool)

