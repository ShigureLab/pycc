from typing import Optional, Type

from pycc.lexer import (
    Add,
    Chr,
    Comma,
    Div,
    Id,
    Int,
    Lexer,
    Lparbrak,
    Mul,
    Num,
    Return,
    Rparbrak,
    Semi,
    Sub,
    Token,
    Char,
    Float,
    Void,
    Assign,
)
from pycc.symbols import IdLevel, Symbol, SymbolTable
from pycc.utils import logger


class Parser:
    source_code: str
    lexer: Lexer
    current_token: Optional[Token]
    current_level: int
    debug: bool

    def __init__(self, source_code: str, debug: bool = False):
        self.source_code = source_code
        self.lexer = Lexer(source_code)
        self.current_token = self.next_token()
        self.symbols = SymbolTable()
        self.current_symbol = Symbol()
        # TODO: 处理 BuildIns
        self.current_level = 1
        self.debug = debug

    def assign_expr(self):
        if self.debug:
            logger.debug("assign_expr:", self.current_token)
        if isinstance(self.current_token, Id):
            symbol_key = f"{self.current_token.value}@{self.current_level}"
            self.match(Id)
            self.match(Assign)
            value = self.assign_expr()
            self.symbols[symbol_key].value = value
        else:
            value = self.sum_expr()
        return value

    def expr(self) -> int:
        if self.debug:
            logger.debug("expr:", self.current_token)
        value = self.assign_expr()
        if (tail_value := self.expr_tail()) is not None:
            value = tail_value
        return value

    def expr_tail(self) -> int:
        """ """
        if self.debug:
            logger.debug("expr_tail:", self.current_token)
        value = None
        if isinstance(self.current_token, Comma):
            self.match(Comma)
            value = self.assign_expr()
            if (tail_value := self.expr_tail()) is not None:
                value = tail_value
        return value

    def sum_expr(self):
        if self.debug:
            logger.debug("sum_expr:", self.current_token)
        return self.term() + self.sum_expr_tail()

    def sum_expr_tail(self) -> int:
        """term + sum_expr_tail1 - sum_expr_tail2 + sum_expr_tail3"""
        if self.debug:
            logger.debug("sum_expr_tail:", self.current_token)
        value = 0
        if isinstance(self.current_token, Add):
            self.match(Add)
            value += self.term()
            value += self.sum_expr_tail()
        elif isinstance(self.current_token, Sub):
            self.match(Sub)
            value -= self.term()
            value += self.sum_expr_tail()
        return value

    def term(self):
        if self.debug:
            logger.debug("term:", self.current_token)
        return self.factor() * self.term_tail()

    def term_tail(self) -> int:
        """factor * term_tail1 / term_tail2 * term_tail3"""
        if self.debug:
            logger.debug("term_tail:", self.current_token)
        value = 1
        if isinstance(self.current_token, Mul):
            self.match(Mul)
            value *= self.factor()
            value *= self.term_tail()
        elif isinstance(self.current_token, Div):
            self.match(Div)
            value /= self.factor()
            value *= self.term_tail()
        return value

    def factor(self) -> int:
        if self.debug:
            logger.debug("factor:", self.current_token)
        value = 0
        if isinstance(self.current_token, Id):
            # TODO: 符号表
            self.match(Id)
            # value = self.current_token.value
        elif isinstance(self.current_token, Num):
            value = self.current_token.value
            self.match(Num)
        # elif isinstance(self.current_token, Chr):
        #     value = self.current_token.value
        #     self.match(Chr)
        elif isinstance(self.current_token, Lparbrak):
            self.match(Lparbrak)
            value = self.expr()
            self.match(Rparbrak)
        else:
            raise Exception(f"Unexpected symbol: {self.current_token}")
        return value

    def type(self) -> Type[Token]:
        if self.debug:
            logger.debug("type:", self.current_token)
        id_type: Type[Token]
        if isinstance(self.current_token, Int):
            self.match(Int)
            id_type = Int
        elif isinstance(self.current_token, Float):
            self.match(Float)
            id_type = Float
        elif isinstance(self.current_token, Char):
            self.match(Char)
            id_type = Char
        elif isinstance(self.current_token, Void):
            self.match(Void)
            id_type = Void
        else:
            raise Exception(f"Unexpected symbol: {self.current_token}")
        return id_type

    def declare(self):
        if self.debug:
            logger.debug("declare:", self.current_token)
        id_type = self.type()

        assert isinstance(self.current_token, Id)
        id_token = self.current_token
        self.match(Id)
        id_symbol = self.current_symbol
        id_symbol.token_cls = id_type

        if (tail_value := self.declare_tail()) is not None:
            id_symbol.value = tail_value

    def declare_tail(self):
        if self.debug:
            logger.debug("declare_tail:", self.current_token)
        value = None
        if isinstance(self.current_token, Assign):
            self.match(Assign)
            value = self.expr()
        return value

    def stmt(self):
        if self.debug:
            logger.debug("stmt:", self.current_token)
        if isinstance(self.current_token, (Id, Num, Chr, Lparbrak)):
            print(self.expr())
            self.match(Semi)
        elif isinstance(self.current_token, (Int, Float, Char, Void)):
            self.declare()
            self.match(Semi)
        elif isinstance(self.current_token, Return):
            self.match(Return)
            self.expr()
            self.match(Semi)

    def stmts(self):
        if self.debug:
            logger.debug("stmts:", self.current_token)
        if isinstance(self.current_token, (Id, Num, Chr, Lparbrak, Int, Float, Char, Void, Return)):
            self.stmt()
            self.stmts()

    def match(self, token_cls: Type[Token]):
        if isinstance(self.current_token, token_cls):
            if self.debug:
                logger.debug("match {} -> {}".format(self.current_token, token_cls.__name__))
            if token_cls is Id:
                self.current_symbol.level = IdLevel(self.current_level)
                self.current_symbol.name = self.current_token.value
                self.current_symbol.token_cls = Id
                self.symbols[f"{self.current_symbol.name}@{self.current_level}"] = self.current_symbol
                self.current_symbol = Symbol()
            self.current_token = self.next_token()
        else:
            raise Exception(f"Unexpected symbol: {self.current_token}")

    def next_token(self) -> Optional[Token]:
        try:
            return self.lexer.__next__()
        except StopIteration:
            return None
