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

def test_cython_connect(n: int) -> None: ...

class VirtualMachine:
    poolsize: int
    def __init__(self, poolsize: int) -> None: ...
    def reset(self) -> None: ...
    def run(self, debug: bool) -> int: ...
    def add_op(self, op: Union[Instruction, int, str]) -> None: ...

def c_pointer_to_string(s_ptr: int) -> str: ...
