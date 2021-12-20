from libcpp cimport bool


cdef extern from "libcore.hpp" namespace "core":
    bool test_cpp_connect(int)
