import re
from dataclasses import dataclass
from typing import Any, Optional, Union

from pycc.utils import logger


@dataclass
class Token:
    value: Any = None
    regexp = re.compile(r"")
    has_value = False
    result_group: Union[str, int] = 0

    def __init__(self, string: str = ""):
        self.value = None

    @classmethod
    def match(cls, string: str, pos: int):
        return cls.regexp.match(string, pos)

    @classmethod
    def token_classes(cls):
        return cls.__subclasses__()

    def __repr__(self):
        if self.has_value:
            return f"<{self.__class__.__name__}, {self.value}>"
        return f"<{self.__class__.__name__}>"


class Num(Token):
    value: int
    regexp = re.compile(r"(?P<match>0|[1-9][0-9]*)[^a-zA-Z]")
    result_group = "match"
    has_value = True

    def __init__(self, string: str):
        # TODO: 二进制、八进制、浮点数支持
        self.value = eval(string)


class Chr(Token):
    value: str
    regexp = re.compile(r"'[\s\S]'")
    has_value = True

    def __init__(self, string: str):
        self.value = string[1:-1]


class Enum(Token):
    value: None
    result_group = "match"
    regexp = re.compile(r"(?P<match>enum)([^a-zA-Z0-9_]|$)")


class If(Token):
    value: None
    result_group = "match"
    regexp = re.compile(r"(?P<match>if)([^a-zA-Z0-9_]|$)")


class Else(Token):
    value: None
    result_group = "match"
    regexp = re.compile(r"(?P<match>else)([^a-zA-Z0-9_]|$)")


class While(Token):
    value: None
    result_group = "match"
    regexp = re.compile(r"(?P<match>while)([^a-zA-Z0-9_]|$)")


class Int(Token):
    value: None
    result_group = "match"
    regexp = re.compile(r"(?P<match>int)([^a-zA-Z0-9_]|$)")


class Char(Token):
    value: None
    result_group = "match"
    regexp = re.compile(r"(?P<match>char)([^a-zA-Z0-9_]|$)")


class Void(Token):
    value: None
    result_group = "match"
    regexp = re.compile(r"(?P<match>void)([^a-zA-Z0-9_]|$)")


class Float(Token):
    value: None
    result_group = "match"
    regexp = re.compile(r"(?P<match>float)([^a-zA-Z0-9_]|$)")


class Return(Token):
    value: None
    result_group = "match"
    regexp = re.compile(r"(?P<match>return)([^a-zA-Z0-9_]|$)")


class Sizeof(Token):
    value: None
    result_group = "match"
    regexp = re.compile(r"(?P<match>sizeof)([^a-zA-Z0-9_]|$)")


class Tilde(Token):
    value: None
    regexp = re.compile(r"~")


class Comma(Token):
    value: None
    regexp = re.compile(r",")


class Lsqubrak(Token):  # [
    value: None
    regexp = re.compile(r"\[")


class Rsqubrak(Token):  # ]
    value: None
    regexp = re.compile(r"\]")


class Lparbrak(Token):  # (
    value: None
    regexp = re.compile(r"\(")


class Rparbrak(Token):  # )
    value: None
    regexp = re.compile(r"\)")


class Lcurbrak(Token):  # {
    value: None
    regexp = re.compile(r"\{")


class Rcurbrak(Token):  # }
    value: None
    regexp = re.compile(r"\}")


class Lor(Token):
    value: None
    regexp = re.compile(r"\|\|")


class Lan(Token):
    value: None
    regexp = re.compile(r"\&\&")


class Or(Token):
    value: None
    regexp = re.compile(r"\|")


class Xor(Token):
    value: None
    regexp = re.compile(r"\^")


class And(Token):
    value: None
    regexp = re.compile(r"\&")


class Eq(Token):
    value: None
    regexp = re.compile(r"==")


class Ne(Token):
    value: None
    regexp = re.compile(r"\!=")


class Le(Token):

    value: None
    regexp = re.compile(r"<=")


class Ge(Token):
    value: None
    regexp = re.compile(r">=")


class Lt(Token):
    value: None
    regexp = re.compile(r"<")


class Gt(Token):
    value: None
    regexp = re.compile(r">")


class Shl(Token):
    value: None
    regexp = re.compile(r"<<")


class Shr(Token):
    value: None
    regexp = re.compile(r">>")


class Assign(Token):
    value: None
    regexp = re.compile(r"=")


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


class Mod(Token):
    value: None
    regexp = re.compile(r"%")


class Inc(Token):
    value: None
    regexp = re.compile(r"\+\+")


class Dec(Token):
    value: None
    regexp = re.compile(r"\-\-")


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
                    match_str = match_obj.group(token_cls.result_group)
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
