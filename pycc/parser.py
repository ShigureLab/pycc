from pycc.lexer import Id, Token, Num, Lexer, Mul, Div
from typing import Type, Optional


class Parser:
    source_code: str
    lexer: Lexer
    current_token: Optional[Token]

    def __init__(self, source_code: str):
        self.source_code = source_code
        self.lexer = Lexer(source_code)
        self.current_token = self.next_token()

    def term(self):
        return self.factor() * self.term_tail()

    def term_tail(self) -> int:
        """factor * term_tail1 / term_tail2 * term_tail3"""
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
            self.current_token = self.next_token()
        else:
            raise Exception(f"Unexpected symbol: {self.current_token}")

    def next_token(self) -> Optional[Token]:
        try:
            return self.lexer.__next__()
        except StopIteration:
            return None
