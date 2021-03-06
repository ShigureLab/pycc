from libcpp cimport bool

cdef extern from "include/libvm.hpp" namespace "vm":
    ctypedef long long int64
    ctypedef int64 Register
    ctypedef int64* AddressRegister
    cdef int LEA,  IMM,  JMP,  CALL, JZ,   JNZ,  ENT,  ADJ
    cdef int LEV,  LI,   LC,   SI,   SC,   PUSH, OR,   XOR
    cdef int AND,  EQ,   NE,   LT,   GT,   LE,   GE,   SHL
    cdef int SHR,  ADD,  SUB,  MUL,  DIV,  MOD,  OPEN, READ
    cdef int CLOS, PRTF, MALC, FREE, MSET, MCMP, EXIT, PLAC

    cdef enum VMStatusCpp 'vm::VMStatusCpp':
        VM_INIT 'vm::VMStatusCpp::INIT'
        VM_RUNNING  'vm::VMStatusCpp::RUNNING'
        VM_EXIT 'vm::VMStatusCpp::EXIT'
        VM_ERROR 'vm::VMStatusCpp::ERROR'

    cdef cppclass VirtualMachineCpp:
        VirtualMachineCpp() except +
        VirtualMachineCpp(int poolsize) except +

        AddressRegister pc   # PC, 程序计数器
        AddressRegister bp   # BP, 基址指针
        AddressRegister sp   # SP, 堆栈指针
        Register ax          # 通用寄存器
        Register cycle
        int poolsize
        VMStatusCpp status

        int64 *text,        # 代码段
        int64 *old_text,    # for dump text segment
        int64 *stack        # 栈区
        char *data          # 数据段
        void reset()
        void add_op(int64 op)
        int64 put_int_onto_data(int value)
        VMStatusCpp step(bool debug)
        int64 run(bool debug)
        int64 run_all_ops(bool debug)
        int pc_offset()
        int64 get_op_pointer(int offset)
        void set_pc(int64 pc)
        void show_ops()
        void setup_main(int64 main_ptr, int argc = 0, char **argv = nullptr)

cdef extern from "include/libvm.hpp" namespace "common":
    ctypedef long long int64
    void _send_integer_to_pointer(int64 ptr, int64 value)
