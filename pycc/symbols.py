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


class IdLevel(Enum):
    BuildIn = 0
    Global = 1
    Local = 2


@dataclass
class Symbol:
    name: str = ""
    token_cls: Optional[Type[Token]] = None
    level: Optional[IdLevel] = None
    value: Any = None
    top_level: Optional["Symbol"] = None


SymbolTable = dict[str, Symbol]
