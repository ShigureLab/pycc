from libcpp cimport bool

# cdef extern from "libvm.hpp" namespace "vm":


cdef extern from "libvm.hpp" namespace "vm":
    cdef enum Status:
        OK = 0
        MEMORY_ERROR = 1
    ctypedef long long int64
    cdef int64 *text
    cdef int LEA,  IMM,  JMP,  CALL, JZ,   JNZ,  ENT,  ADJ
    cdef int LEV,  LI,   LC,   SI,   SC,   PUSH, OR,   XOR
    cdef int AND,  EQ,   NE,   LT,   GT,   LE,   GE,   SHL
    cdef int SHR,  ADD,  SUB,  MUL,  DIV,  MOD,  OPEN, READ
    cdef int CLOS, PRTF, MALC, FREE, MSET, MCMP, EXIT

    bool test_cpp_connect(int)
    Status init_vm(int)
    void reset_vm(int)
    void free_vm()
    int64 run_vm(bool)

