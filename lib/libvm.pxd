from libcpp cimport bool


cdef extern from "libvm.hpp" namespace "vm":
    bool test_cpp_connect(int)
