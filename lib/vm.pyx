from libc.stdlib cimport malloc
from libc.string cimport strcpy

cimport libvm
from libvm cimport test_cpp_connect
from libvm cimport reset_vm
from libvm cimport free_vm
from libvm cimport init_vm
from libvm cimport run_vm
from libvm cimport text
from libvm cimport int64

from enum import Enum
from typing import Union

cdef _test_cython_connect(int n):
    test_cpp_connect(n)
    print("test_cython_connect in cython code.")

def test_cython_connect(n: int):
    _test_cython_connect(n)

class Instruction(Enum):
    LEA = libvm.LEA
    IMM = libvm.IMM
    JMP = libvm.JMP
    CALL = libvm.CALL
    JZ = libvm.JZ
    JNZ = libvm.JNZ
    ENT = libvm.ENT
    ADJ = libvm.ADJ
    LEV = libvm.LEV
    LI = libvm.LI
    LC = libvm.LC
    SI = libvm.SI
    SC = libvm.SC
    PUSH = libvm.PUSH
    OR = libvm.OR
    XOR = libvm.XOR
    AND = libvm.AND
    EQ = libvm.EQ
    NE = libvm.NE
    LT = libvm.LT
    GT = libvm.GT
    LE = libvm.LE
    GE = libvm.GE
    SHL = libvm.SHL
    SHR = libvm.SHR
    ADD = libvm.ADD
    SUB = libvm.SUB
    MUL = libvm.MUL
    DIV = libvm.DIV
    MOD = libvm.MOD
    OPEN = libvm.OPEN
    READ = libvm.READ
    CLOS = libvm.CLOS
    PRTF = libvm.PRTF
    MALC = libvm.MALC
    FREE = libvm.FREE
    MSET = libvm.MSET
    MCMP = libvm.MCMP
    EXIT = libvm.EXIT

cdef class VirtualMachine:
    cdef int poolsize
    cdef int curr
    def __cinit__(self, int poolsize):
        self.poolsize = poolsize
        self.curr = 0
        init_vm(poolsize)

    def __dealloc__(self):
        free_vm()

    def reset(self):
        self.curr = 0
        reset_vm(self.poolsize)

    def run(self, debug: bool) -> int:
        return run_vm(debug)

    def add_op(self, op: Union[Instruction, int, str]):
        cdef int64 opcode = 0
        cdef bytes b_str
        cdef char* c_str
        if isinstance(op, Instruction):
            opcode = op.value
        elif isinstance(op, int):
            opcode = op
        elif isinstance(op, str):
            b_str = op.encode()
            c_str = <char *>malloc((len(op) + 1) * sizeof(char))  # 在堆区申请一块空间存放字符串
            strcpy(c_str, b_str)
            opcode = <int64>c_str
        text[self.curr] = opcode
        self.curr += 1


def c_pointer_to_string(s_ptr: int64) -> str:
    cdef bytes b_str = <char *>s_ptr
    return b_str.decode()
