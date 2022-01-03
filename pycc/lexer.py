import re
from dataclasses import dataclass
from typing import Any, Optional

from pycc.utils import logger


@dataclass
class Token:
    value: Any = None
    regexp = re.compile(r"")
    has_value = False

    def __init__(self, string: str = ""):
        self.value = None

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


class Chr(Token):
    value: str
    regexp = re.compile(r"'[\s\S]'")
    has_value = True

    def __init__(self, string: str):
        self.value = string


# class Fun(Token):
# class Sys(Token):
# class Glo(Token):
# class Loc(Token):
# class Enum(Token):
# class If(Token):
# class Else(Token):
# class While(Token):
class Int(Token):
    value: None
    regexp = re.compile(r"int^[a-zA-Z_]")


class Char(Token):
    value: None
    regexp = re.compile(r"char^[a-zA-Z_]")


class Void(Token):
    value: None
    regexp = re.compile(r"void^[a-zA-Z_]")


class Float(Token):
    value: None
    regexp = re.compile(r"float^[a-zA-Z_]")


class Return(Token):
    value: None
    regexp = re.compile(r"return^[a-zA-Z_]")


class Sizeof(Token):
    value: None
    regexp = re.compile(r"sizeof^[a-zA-Z_]")


class Assign(Token):
    value: None
    regexp = re.compile(r"=")


class Tilde(Token):
    value: None
    regexp = re.compile(r"~")


class Comma(Token):
    value: None
    regexp = re.compile(r",")


# class Lsqbrac(Token): # [
# class Rsqbrac(Token): # ]
class Lpar(Token):  # (
    value: None
    regexp = re.compile(r"\(")


class Rpar(Token):  # )
    value: None
    regexp = re.compile(r"\)")


# class Lcubrac(Token): # {
# class Rcubrac(Token): # }
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
class Add(Token):
    value: None
    regexp = re.compile(r"\+")


class Sub(Token):
    value: None
    regexp = re.compile(r"-")


class Mul(Token):
    value: None
    regexp = re.compile(r"\*")


class Div(Token):
    value: None
    regexp = re.compile(r"/")


# class Mod(Token):
# class Inc(Token):
# class Dec(Token):
class Semi(Token):
    value: None
    regexp = re.compile(r";")


class Id(Token):
    value: str
    regexp = re.compile(r"[a-zA-Z_][a-zA-Z0-9_]*")
    has_value = True

    def __init__(self, string: str):
        self.value = string


def match_comments(string: str, pos: int) -> Optional[re.Match[str]]:
    regexp_comments_double_slash = re.compile(r"//[\s\S]*?(\n|$)")
    regexp_comments_slash_star = re.compile(r"/\*[\s\S]*?\*/")
    if string.startswith("//", pos):
        match_obj = regexp_comments_double_slash.match(string, pos)
        assert match_obj is not None, f"{logger.ERROR_BADGE} Unterminated comment"
        return match_obj
    elif string.startswith("/*", pos):
        match_obj = regexp_comments_slash_star.match(string, pos)
        assert match_obj is not None, f"{logger.ERROR_BADGE} Unterminated comment"
        return match_obj
    else:
        return None


def match_whitespace(string: str, pos: int) -> Optional[re.Match[str]]:
    regexp_whitespace = re.compile(r"[\s]+")
    return regexp_whitespace.match(string, pos)


class Lexer:
    source_pointer: int = 0

    def __init__(self, source_code: str):
        self.source_pointer = 0
        self.source_code = source_code

    def __iter__(self):
        return self

    def __next__(self) -> Token:
        if self.source_pointer < len(self.source_code):
            # 匹配并跳过注释
            if match_obj := match_comments(self.source_code, self.source_pointer):
                comments = match_obj.group(0)
                self.source_pointer += len(comments)
                return self.__next__()

            # 匹配并跳过空白字符
            if match_obj := match_whitespace(self.source_code, self.source_pointer):
                whitespace = match_obj.group(0)
                self.source_pointer += len(whitespace)
                return self.__next__()

            # 匹配各种 token
            for token_cls in Token.token_classes():
                if match_obj := token_cls.match(self.source_code, self.source_pointer):
                    match_str = match_obj.group(0)
                    self.source_pointer += len(match_str)
                    if token_cls.has_value:
                        return token_cls(match_str)
                    else:
                        return token_cls()

            # 未预期的符号
            else:
                # i += 1
                raise Exception(f"Unexpected symbol: {self.source_code[self.source_pointer]}")
        else:
            raise StopIteration

    def tokenize(self):
        token_stream: list[Token] = []
        for token in self:
            token_stream.append(token)
        return token_stream
