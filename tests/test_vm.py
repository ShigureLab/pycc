import pytest
from pycc.vm import VirtualMachine, Instruction, c_pointer_to_string, c_pointer_to_integer


poolsize = 256 * 1024


@pytest.mark.parametrize(
    "a, b",
    [
        (10, 20),
        (9, -10),
        (1000, -1000),
    ],
)
def test_add(a: int, b: int):
    global poolsize
    vm = VirtualMachine(poolsize)

    vm.add_op(Instruction.IMM)
    vm.add_op(a)
    vm.add_op(Instruction.PUSH)
    vm.add_op(Instruction.IMM)
    vm.add_op(b)
    vm.add_op(Instruction.ADD)
    vm.add_op(Instruction.PUSH)
    vm.add_op(Instruction.EXIT)

    result = vm.run(True)
    assert result == a + b


@pytest.mark.parametrize(
    "a, b",
    [
        (1, -1),
        (0, 100),
    ],
)
def test_multiply(a: int, b: int):
    global poolsize
    vm = VirtualMachine(poolsize)

    vm.add_op(Instruction.IMM)
    vm.add_op(a)
    vm.add_op(Instruction.PUSH)
    vm.add_op(Instruction.IMM)
    vm.add_op(b)
    vm.add_op(Instruction.MUL)
    vm.add_op(Instruction.PUSH)
    vm.add_op(Instruction.EXIT)

    result = vm.run(True)
    assert result == a * b


@pytest.mark.parametrize(
    "s",
    [
        "123",
        "456",
    ],
)
def test_string(s: str):
    global poolsize
    vm = VirtualMachine(poolsize)

    vm.add_op(Instruction.IMM)
    vm.add_op(s)
    vm.add_op(Instruction.PUSH)
    vm.add_op(Instruction.EXIT)

    result = c_pointer_to_string(vm.run(True))
    assert result == s


@pytest.mark.parametrize(
    "a, b, c, d",
    [
        (1, 6, 0, -100),
    ],
)
def test_reset_add(a: int, b: int, c: int, d: int):
    global poolsize
    vm = VirtualMachine(poolsize)

    vm.add_op(Instruction.IMM)
    vm.add_op(a)
    vm.add_op(Instruction.PUSH)
    vm.add_op(Instruction.IMM)
    vm.add_op(b)
    vm.add_op(Instruction.ADD)
    vm.add_op(Instruction.PUSH)
    vm.add_op(Instruction.EXIT)

    result = vm.run(True)
    assert result == a + b

    vm.reset()
    vm.add_op(Instruction.IMM)
    vm.add_op(c)
    vm.add_op(Instruction.PUSH)
    vm.add_op(Instruction.IMM)
    vm.add_op(d)
    vm.add_op(Instruction.ADD)
    vm.add_op(Instruction.PUSH)
    vm.add_op(Instruction.EXIT)

    result = vm.run(True)
    assert result == c + d


def test_registers():
    global poolsize
    a, b = 1, 2
    vm = VirtualMachine(poolsize)
    assert c_pointer_to_integer(vm.pc) == 0
    assert c_pointer_to_integer(vm.bp) == 0
    assert c_pointer_to_integer(vm.sp) == 0

    vm.add_op(Instruction.IMM)
    vm.add_op(a)
    vm.add_op(Instruction.PUSH)
    vm.add_op(Instruction.IMM)
    vm.add_op(b)
    vm.add_op(Instruction.ADD)
    vm.add_op(Instruction.PUSH)
    vm.add_op(Instruction.EXIT)

    result = vm.run(True)

    vm.reset()
    assert c_pointer_to_integer(vm.pc) == 0
    assert c_pointer_to_integer(vm.bp) == 0
    assert c_pointer_to_integer(vm.sp) == 0
    assert result == a + b


@pytest.mark.parametrize(
    "a",
    [
        10086,
        -1111,
    ],
)
def test_global_declare(a: int):
    global poolsize
    vm = VirtualMachine(poolsize)

    ptr_a = vm.put_int_onto_data(a)
    vm.add_op(Instruction.IMM)
    vm.add_op(ptr_a)
    vm.add_op(Instruction.LI)
    vm.add_op(Instruction.PUSH)
    vm.add_op(Instruction.EXIT)

    result = vm.run(True)
    assert result == a


@pytest.mark.parametrize(
    "a, b",
    [
        (9999, -8888),
    ],
)
def test_global_add(a: int, b: int):
    global poolsize
    vm = VirtualMachine(poolsize)

    ptr_a = vm.put_int_onto_data(a)
    ptr_b = vm.put_int_onto_data(b)
    vm.add_op(Instruction.IMM)
    vm.add_op(ptr_a)
    vm.add_op(Instruction.LI)
    vm.add_op(Instruction.PUSH)
    vm.add_op(Instruction.IMM)
    vm.add_op(ptr_b)
    vm.add_op(Instruction.LI)
    vm.add_op(Instruction.ADD)
    vm.add_op(Instruction.PUSH)
    vm.add_op(Instruction.EXIT)

    result = vm.run(True)
    assert result == a + b
