from pycc.lexer import Id, Token, Num, Lexer, Mul, Div, Add, Sub
from typing import Type, Optional
from pycc.utils import logger


class Parser:
    source_code: str
    lexer: Lexer
    current_token: Optional[Token]
    debug: bool

    def __init__(self, source_code: str, debug: bool = False):
        self.source_code = source_code
        self.lexer = Lexer(source_code)
        self.current_token = self.next_token()
        self.debug = debug

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
        elif isinstance(self.current_token, Chr):
            value = self.current_token.value
            self.match(Chr)
        elif isinstance(self.current_token, Lpar):
            self.match(Lpar)
            value = self.expr()
            self.match(Rpar)
        else:
            raise Exception(f"Unexpected symbol: {self.current_token}")
        return value

    def match(self, token_cls: Type[Token]):
        if isinstance(self.current_token, token_cls):
            if self.debug:
                logger.debug("match {} -> {}".format(self.current_token, token_cls.__name__))
            self.current_token = self.next_token()
        else:
            raise Exception(f"Unexpected symbol: {self.current_token}")

    def next_token(self) -> Optional[Token]:
        try:
            return self.lexer.__next__()
        except StopIteration:
            return None
