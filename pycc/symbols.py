from enum import Enum
from dataclasses import dataclass
from pycc.lexer import Token
from typing import Type, Any, Optional


class IdType(Enum):

    int = 0
    float = 1
    char = 2
    ptr = 3

    # TODO: ptr to type


class IdScope(Enum):
    Local = 0
    Global = 1


@dataclass
class Symbol:
    name: str = ""
    token_cls: Optional[Type[Token]] = None
    scope: Optional[IdScope] = None
    value: Any = None
    global_token_cls: Optional[Type[Token]] = None
    global_scope: Optional[IdScope] = None
    global_value: Any = None


SymbolTable = dict[str, Symbol]
