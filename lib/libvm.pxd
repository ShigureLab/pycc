from libcpp cimport bool

cdef extern from "libvm.hpp" namespace "vm":
    ctypedef long long int64
    ctypedef int64 Register
    ctypedef int64* AddressRegister
    cdef int LEA,  IMM,  JMP,  CALL, JZ,   JNZ,  ENT,  ADJ
    cdef int LEV,  LI,   LC,   SI,   SC,   PUSH, OR,   XOR
    cdef int AND,  EQ,   NE,   LT,   GT,   LE,   GE,   SHL
    cdef int SHR,  ADD,  SUB,  MUL,  DIV,  MOD,  OPEN, READ
    cdef int CLOS, PRTF, MALC, FREE, MSET, MCMP, EXIT

    cdef cppclass VirtualMachineCpp:
        VirtualMachineCpp() except +
        VirtualMachineCpp(int poolsize) except +

        AddressRegister pc   # PC, 程序计数器
        AddressRegister bp   # BP, 基址指针
        AddressRegister sp   # SP, 堆栈指针
        Register ax          # 通用寄存器
        Register cycle
        int poolsize

        int64 *text,        # 代码段
        int64 *old_text,    # for dump text segment
        int64 *stack        # 栈区
        char *data          # 数据段
        void reset()
        void add_op(int64 op)
        int64 run(bool debug)
