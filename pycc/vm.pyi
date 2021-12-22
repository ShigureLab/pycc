from typing import Union
from enum import Enum

class Instruction(Enum):
    LEA: int
    IMM: int
    JMP: int
    CALL: int
    JZ: int
    JNZ: int
    ENT: int
    ADJ: int
    LEV: int
    LI: int
    LC: int
    SI: int
    SC: int
    PUSH: int
    OR: int
    XOR: int
    AND: int
    EQ: int
    NE: int
    LT: int
    GT: int
    LE: int
    GE: int
    SHL: int
    SHR: int
    ADD: int
    SUB: int
    MUL: int
    DIV: int
    MOD: int
    OPEN: int
    READ: int
    CLOS: int
    PRTF: int
    MALC: int
    FREE: int
    MSET: int
    MCMP: int
    EXIT: int

class VMStatus(Enum):
    INIT: int
    RUNNING: int
    EXIT: int
    ERROR: int

class VirtualMachine:
    poolsize: int
    pc: int
    bp: int
    sp: int
    ax: int
    cycle: int
    status: VMStatus
    def __init__(self, poolsize: int) -> None: ...
    def reset(self) -> None: ...
    def add_op(self, op: Union[Instruction, int, str]) -> None: ...
    def step(self, debug: bool) -> VMStatus: ...
    def run(self, debug: bool) -> int: ...
    def run_all_ops(self, debug: bool) -> int: ...
    def pc_offset(self) -> int: ...

def c_pointer_to_string(s_ptr: int) -> str: ...
def c_pointer_to_integer(i_ptr: int) -> int: ...
