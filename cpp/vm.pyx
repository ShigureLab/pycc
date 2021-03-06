from libc.stdlib cimport malloc
from libc.string cimport strcpy
from cython.operator cimport dereference

cimport libvm
from libvm cimport VirtualMachineCpp
from libvm cimport int64
from libvm cimport VMStatusCpp
from libvm cimport _send_integer_to_pointer

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
    PLAC = libvm.PLAC

class VMStatus(Enum):
    INIT = libvm.VM_INIT
    RUNNING = libvm.VM_RUNNING
    EXIT = libvm.VM_EXIT
    ERROR = libvm.VM_ERROR

cdef class VirtualMachine:
    cdef VirtualMachineCpp* vmcpp
    def __cinit__(self, int poolsize):
        self.vmcpp = new VirtualMachineCpp(poolsize)

    def __dealloc__(self):
        del self.vmcpp

    def reset(self):
        self.vmcpp.reset()

    def step(self, debug: bool = False) -> VMStatus:
        return VMStatus(self.vmcpp.step(debug))

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

    def put_int_onto_data(self, value: int) -> int:
        return self.vmcpp.put_int_onto_data(value)

    def run(self, debug: bool = False) -> int:
        return self.vmcpp.run(debug)

    def run_all_ops(self, debug: bool = False) -> int:
        return self.vmcpp.run_all_ops(debug)

    def pc_offset(self) -> int:
        return self.vmcpp.pc_offset()

    def get_op_pointer(self, offset: int = 0) -> int:
        return self.vmcpp.get_op_pointer(offset)

    def set_pc(self, pc: int) -> None:
        self.vmcpp.set_pc(pc)

    def show_ops(self) -> None:
        self.vmcpp.show_ops()

    def setup_main(self, main_ptr: int, argc: int = 0, argv: list[str] = 0)-> None :
        # TODO: argc, argv
        self.vmcpp.setup_main(main_ptr)

    @property
    def poolsize(self) -> int:
        return self.vmcpp.poolsize

    @property
    def pc(self) -> int:
        return <int64>self.vmcpp.pc

    @property
    def bp(self) -> int:
        return <int64>self.vmcpp.bp

    @property
    def sp(self) -> int:
        return <int64>self.vmcpp.sp

    @property
    def ax(self) -> int:
        return <int64>self.vmcpp.ax

    @property
    def cycle(self) -> int:
        return <int64>self.vmcpp.cycle

    @property
    def status(self) -> VMStatus:
        return VMStatus(self.vmcpp.status)

cdef bytes _c_pointer_to_string(int64 s_ptr):
    cdef bytes b_str = <char *>s_ptr
    return b_str

def c_pointer_to_string(s_ptr: int) -> str:
    b_str = _c_pointer_to_string(s_ptr)
    return b_str.decode()

cdef int _c_pointer_to_interger(int64 i_ptr):
    return dereference(<int *>i_ptr)

def c_pointer_to_integer(i_ptr: int) -> int:
    return _c_pointer_to_interger(i_ptr)

def send_integer_to_pointer(ptr: int, value: int) -> None:
    _send_integer_to_pointer(ptr, value)
