from enum import Enum
from dataclasses import dataclass
from typing import Type, Any, Optional


class IdType(Enum):
    Void = 0
    Int = 1
    Float = 2
    Char = 3
    Ptr = 4

    # TODO: ptr to type


class IdClass(Enum):
    Sys = 0
    Func = 1
    Var = 2


class IdLevel(Enum):
    BuiltIn = 0
    Global = 1
    Local = 2

    def __add__(self, level: int) -> "IdLevel":
        return self.__class__(self.value + level)

    def __sub__(self, level: int) -> "IdLevel":
        return self.__class__(self.value - level)


@dataclass
class Symbol:
    name: str = ""
    cls: Optional[IdClass] = None
    data_type: Optional[IdType] = None
    level: Optional[IdLevel] = None
    value: Any = None


class SymbolTable(dict[str, Symbol]):
    def __init__(self):
        super().__init__()
        self.scope_id_cnt: int = 0  # 用于标识最大作用域标号
        self.scope_id: int = self.scope_id_cnt  # 用于标识当前作用域
        self.level: int = 0  # 用于标识当前作用域层级
        self.scope_stack: list[int] = []

    def enter_scope(self):
        self.scope_stack.append(self.scope_id)
        self.level += 1
        self.scope_id_cnt += 1
        self.scope_id = self.scope_id_cnt

    def leave_scope(self):
        self.level -= 1
        self.scope_id = self.scope_stack.pop()

    def set_symbol(self, symbol: Symbol) -> Symbol:
        if self.get(self.calc_key(symbol.name, self.scope_id)):
            raise Exception(f"name {symbol.name} already exists")
        self[self.calc_key(symbol.name, self.scope_id)] = symbol
        return symbol

    def get_symbol(self, name: str) -> Symbol:
        for scope_id in reversed(self.scope_stack + [self.scope_id]):
            if (symbol := self.get(self.calc_key(name, scope_id))) is not None:
                return symbol
        raise Exception(f"name {name} is not defined")

    @staticmethod
    def calc_key(name: str, level: int) -> str:
        return f"{name}@{level}"
