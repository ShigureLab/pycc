from types import LambdaType
from typing import Optional, Type

from pycc.lexer import (
    Add,
    Assign,
    Char,
    Chr,
    Comma,
    Div,
    Else,
    Float,
    Id,
    If,
    Int,
    Lcurbrak,
    Lexer,
    Lparbrak,
    Mul,
    Num,
    Rcurbrak,
    Return,
    Rparbrak,
    Semi,
    Sub,
    Token,
    Void,
    While,
)
from pycc.symbols import IdLevel, IdType, Symbol, SymbolTable
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
        self.symbols.enter_scope()
        self.base_type = IdType.Int
        self.index_of_bp = 0
        self.debug = debug

    def __del__(self):
        self.symbols.leave_scope()

    def expr(self) -> int:
        if self.debug:
            logger.debug("expr:", self.current_token)
        value = self.sum_expr()
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
            value = self.sum_expr()
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

    def type(self):
        if self.debug:
            logger.debug("type:", self.current_token)
        if isinstance(self.current_token, Int):
            self.match(Int)
            self.base_type = IdType.Int
        elif isinstance(self.current_token, Float):
            self.match(Float)
            self.base_type = IdType.Float
        elif isinstance(self.current_token, Char):
            self.match(Char)
            self.base_type = IdType.Char
        elif isinstance(self.current_token, Void):
            self.match(Void)
            self.base_type = IdType.Void
        else:
            raise Exception(f"Unexpected symbol: {self.current_token}")

    def declare(self):
        if self.debug:
            logger.debug("declare:", self.current_token)
        self.type()
        id_token = self.current_token
        assert isinstance(id_token, Id)
        self.match(Id)
        # if self.symbols.level == IdLevel.Global.value:
        #     data_ptr = vm.put_int_onto_data(0)
        #     vm.add_op(vm.)

        symbol = Symbol(
            name=id_token.value,
            token_cls=Id,
            data_type=self.base_type,
            level=IdLevel(self.symbols.level),
            value=0,  # TODO
        )

        if (tail_value := self.declare_tail()) is not None:
            symbol.value = tail_value

        self.symbols.set_symbol(symbol)

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
        if isinstance(self.current_token, Id):
            self.match(Id)
            self.match(Assign)
            self.expr()
            self.match(Semi)
        elif isinstance(self.current_token, (Int, Float, Char, Void)):
            self.declare()
            self.match(Semi)
        elif isinstance(self.current_token, Return):
            self.match(Return)
            self.expr()
            self.match(Semi)
        elif isinstance(self.current_token, If):
            self.match(If)
            self.match(Lparbrak)
            self.expr()
            self.match(Rparbrak)
            self.stmt()
            self.else_branch()
        elif isinstance(self.current_token, While):
            self.match(While)
            self.match(Lparbrak)
            self.expr()
            self.match(Rparbrak)
            self.stmt()
        elif isinstance(self.current_token, Lcurbrak):
            self.match(Lcurbrak)
            self.stmts()
            self.match(Rcurbrak)

    def else_branch(self):
        if self.debug:
            logger.debug("else_branch:", self.current_token)
        if isinstance(self.current_token, Else):
            self.match(Else)
            self.stmt()

    def stmts(self):
        if self.debug:
            logger.debug("stmts:", self.current_token)
        if isinstance(self.current_token, (Id, Num, Chr, Lparbrak, Int, Float, Char, Void, Return, If, While)):
            self.stmt()
            self.stmts()
        # elif isinstance(self.current_token, (Id, Num, Chr, Lparbrak, Int, Float, Char, Void, Return, If, While)):

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

    def return_type(self):
        if self.debug:
            logger.debug("return_type:", self.current_token)
        if isinstance(self.current_token, Int):
            self.match(Int)
        elif isinstance(self.current_token, Float):
            self.match(Float)
            # self.base_type = IdType.Float
        elif isinstance(self.current_token, Char):
            self.match(Char)
            # self.base_type = IdType.Char
        elif isinstance(self.current_token, Void):
            self.match(Void)

    def start(self):
        if self.debug:
            logger.debug("start:",self.current_token)
        if isinstance(self.current_token, (Int, Float, Char, Void)):
            self.start_tail()
            self.start()
    
    def start_tail(self):
        if self.debug:
            logger.debug("start_tail:",self.current_token)
        self.type()
        self.match(Id)
        if isinstance(self.current_token, Lparbrak):
            self.match(Lparbrak)
            self.func_params()
            self.match(Rparbrak)
            if isinstance(self.current_token, Lcurbrak):
                self.match(Lcurbrak)
                self.stmts()
                self.match(Rcurbrak)
            elif isinstance(self.current_token, Semi):
                self.match(Semi)
        else:
            self.declare_tail()
            self.match(Semi)

    def func_params(self):
        if self.debug:
            logger.debug("func_params:", self.current_token)
        if isinstance(self.current_token, (Int, Float, Char, Void)):
            self.type()
            self.match(Id)
            self.func_params_tail()
    
    def func_params_tail(self):
        if self.debug:
            logger.debug("func_params_tail:", self.current_token)
        if isinstance(self.current_token, Comma):
            self.match(Comma)
            self.type()
            self.match(Id)
            self.func_params_tail()

    