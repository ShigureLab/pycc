import re
from dataclasses import dataclass
from typing import Any, Optional
from enum import Enum


class CType(Enum):

    int = 0
    float = 1
    char = 2
    ptr = 3

    # TODO: ptr to type


@dataclass
class Token:
    value: Any = None
    regexp = re.compile(r"")
    has_value = False

    def __init__(self, string: str):
        if self.has_value:
            self.value = string

    @classmethod
    def match(cls, string: str, pos: int):
        return cls.regexp.match(string, pos)

    @classmethod
    def token_classes(cls):
        return cls.__subclasses__()


class Num(Token):
    value: int
    regexp = re.compile(r"\d+")
    has_value = True

    def __init__(self, string: str):
        # TODO: 二进制、八进制、浮点数支持
        self.value = eval(string)


# class Fun(Token):
# class Sys(Token):
# class Glo(Token):
# class Loc(Token):
# class Id(Token):
# class Char(Token):
# class Else(Token):
# class Enum(Token):
# class If(Token):
class Int(Token):
    value: None
    regexp = re.compile(r"int")


class Return(Token):
    value: None
    regexp = re.compile(r"return")


class Sizeof(Token):
    value: None
    regexp = re.compile(r"sizeof")


# class While(Token):
# class Assign(Token):
# class Cond(Token):
# class Lor(Token):
# class Lan(Token):
# class Or(Token):
# class Xor(Token):
# class And(Token):
# class Eq(Token):
# class Ne(Token):
# class Lt(Token):
# class Gt(Token):
# class Le(Token):
# class Ge(Token):
# class Shl(Token):
# class Shr(Token):
# class Add(Token):
# class Sub(Token):
# class Mul(Token):
# class Div(Token):
# class Mod(Token):
# class Inc(Token):
# class Dec(Token):
# class Brak(Token):


def match_comments(string: str, pos: int) -> Optional[re.Match[str]]:
    regexp_comments_double_slash = re.compile(r"//[\s\S]*?(\n|$)")
    regexp_comments_slash_star = re.compile(r"/\*[\s\S]*?\*/")
    if string.startswith("//", pos):
        match_obj = regexp_comments_double_slash.match(string, pos)
        assert match_obj is not None, "[Error] Unterminated comment"
        return match_obj
    elif string.startswith("/*", pos):
        match_obj = regexp_comments_slash_star.match(string, pos)
        assert match_obj is not None, "[Error] Unterminated comment"
        return match_obj
    else:
        return None


def match_whitespace(string: str, pos: int) -> Optional[re.Match[str]]:
    regexp_whitespace = re.compile(r"[\s]+")
    return regexp_whitespace.match(string, pos)
