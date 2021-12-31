import re
from dataclasses import dataclass
from typing import Any


@dataclass
class Token:
    value: Any = None
    regexp = re.compile(r"")

    def __init__(self, string: str):
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

    def __init__(self, string: str):
        # TODO: 二进制、八进制、浮点数支持
        self.value = eval(string)
