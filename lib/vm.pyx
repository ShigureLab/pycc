from libc.stdlib cimport malloc
from libc.string cimport strcpy

cimport libvm
from libvm cimport VirtualMachineCpp
from libvm cimport int64

from enum import Enum
from typing import Union

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
    cdef VirtualMachineCpp* vmcpp
    def __cinit__(self, int poolsize):
        self.vmcpp = new VirtualMachineCpp(poolsize)

    def __dealloc__(self):
        del self.vmcpp

    def reset(self):
        self.vmcpp.reset()

    def run(self, debug: bool) -> int:
        return self.vmcpp.run(debug)

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
        self.vmcpp.add_op(opcode)

cdef bytes _c_pointer_to_string(int64 s_ptr):
    cdef bytes b_str = <char *>s_ptr
    return b_str

def c_pointer_to_string(s_ptr: int) -> str:
    b_str = _c_pointer_to_string(s_ptr)
    return b_str.decode()
