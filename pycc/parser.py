import json
from typing import Optional, Type, Union

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
    Mod,
    Num,
    Rcurbrak,
    Return,
    Rparbrak,
    Semi,
    Sub,
    Token,
    Void,
    While,
    Lan,
    Lor,
    Xor,
    Or,
    And,
    Eq,
    Ne,
    Gt,
    Lt,
    Ge,
    Le,
)
from pycc.symbols import IdLevel, IdType, Symbol, SymbolTable, IdClass
from pycc.utils import logger
from pycc.vm import Instruction, VirtualMachine, send_integer_to_pointer

AST = Union[dict[str, "AST"], str]


class Node:
    def __init__(self, name: str):
        self.name = name
        self.children: list["Node"] = []
        self.is_terminal = False

    def add_node(self, node: "Node"):
        self.children.append(node)

    def to_ast(self) -> AST:
        if not self.children:
            return "<empty>"
        ast: AST = {}
        for child in self.children:
            ast[child.name] = child.to_ast()
        return ast

    def dump(self, file: str):
        with open(file, "w", encoding="utf-8") as f:
            json.dump(self.to_ast(), f, indent=2)


class TerminalNode(Node):
    def __init__(self, name: str):
        super().__init__(name)
        self.is_terminal = True

    def to_ast(self) -> AST:
        return self.name


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
        self.base_type = IdType.Int
        self.preset_buildins()
        self.symbols.enter_scope()
        self.debug = debug
        self.vm = VirtualMachine(256 * 1024)
        self.func_bp_index = 0
        self.func_num_params = 0
        self.func_num_local_vars = 0

    def __del__(self):
        self.symbols.leave_scope()

    def preset_buildins(self):
        system_calls = ["open", "read", "close", "printf", "malloc", "free", "memset", "memcmp"]

        for i in range(Instruction.EXIT.value - Instruction.OPEN.value):
            symbol = Symbol(
                name=system_calls[i],
                cls=IdClass.Sys,
                data_type=self.base_type,
                level=IdLevel(self.symbols.level),
                value=Instruction.OPEN.value + i,
            )
            self.symbols.set_symbol(symbol)

    def reset_func_recorders(self):
        self.func_bp_index = 0
        self.func_num_params = 0
        self.func_num_local_vars = 0

    def expr(self):
        node = Node("expr")
        if self.debug:
            logger.debug("expr:", self.current_token)
        node.add_node(self.lor_expr())
        return node

    def lor_expr(self):
        node = Node("lor_expr")
        if self.debug:
            logger.debug("lor_expr:", self.current_token)
        node.add_node(self.land_expr())
        node.add_node(self.lor_expr_tail())
        return node

    def lor_expr_tail(self):
        node = Node("lor_expr_tail")
        if self.debug:
            logger.debug("lor_expr_tail:", self.current_token)
        if isinstance(self.current_token, Lor):
            node.add_node(self.match(Lor))
            self.vm.add_op(Instruction.JNZ)
            self.vm.add_op(Instruction.PLAC)
            addr = self.vm.get_op_pointer(-1)
            node.add_node(self.land_expr())
            send_integer_to_pointer(addr, self.vm.get_op_pointer(0))
            node.add_node(self.lor_expr_tail())
        return node

    def land_expr(self):
        node = Node("land_expr")
        if self.debug:
            logger.debug("land_expr:", self.current_token)
        node.add_node(self.or_expr())
        node.add_node(self.land_expr_tail())
        return node

    def land_expr_tail(self):
        node = Node("land_expr_tail")
        if self.debug:
            logger.debug("land_expr_tail:", self.current_token)
        if isinstance(self.current_token, Lan):
            node.add_node(self.match(Lan))
            self.vm.add_op(Instruction.JZ)
            self.vm.add_op(Instruction.PLAC)
            addr = self.vm.get_op_pointer(-1)
            node.add_node(self.or_expr())
            send_integer_to_pointer(addr, self.vm.get_op_pointer(0))
            node.add_node(self.land_expr_tail())
        return node

    def or_expr(self):
        node = Node("or_expr")
        if self.debug:
            logger.debug("or_expr:", self.current_token)
        node.add_node(self.xor_expr())
        node.add_node(self.or_expr_tail())
        return node

    def or_expr_tail(self):
        node = Node("or_expr_tail")
        if self.debug:
            logger.debug("or_expr_tail:", self.current_token)
        if isinstance(self.current_token, Or):
            node.add_node(self.match(Or))
            self.vm.add_op(Instruction.PUSH)
            node.add_node(self.xor_expr())
            self.vm.add_op(Instruction.OR)
            node.add_node(self.or_expr_tail())
        return node

    def xor_expr(self):
        node = Node("xor_expr")
        if self.debug:
            logger.debug("xor_expr:", self.current_token)
        node.add_node(self.and_expr())
        node.add_node(self.xor_expr_tail())
        return node

    def xor_expr_tail(self):
        node = Node("xor_expr_tail")
        if self.debug:
            logger.debug("xor_expr_tail:", self.current_token)
        if isinstance(self.current_token, Xor):
            node.add_node(self.match(Xor))
            self.vm.add_op(Instruction.PUSH)
            node.add_node(self.and_expr())
            self.vm.add_op(Instruction.XOR)
            node.add_node(self.xor_expr_tail())
        return node

    def and_expr(self):
        node = Node("and_expr")
        if self.debug:
            logger.debug("and_expr:", self.current_token)
        node.add_node(self.equal_expr())
        node.add_node(self.and_expr_tail())
        return node

    def and_expr_tail(self):
        node = Node("and_expr_tail")
        if self.debug:
            logger.debug("and_expr_tail:", self.current_token)
        if isinstance(self.current_token, And):
            node.add_node(self.match(And))
            self.vm.add_op(Instruction.PUSH)
            node.add_node(self.equal_expr())
            self.vm.add_op(Instruction.AND)
            node.add_node(self.and_expr_tail())
        return node

    def equal_expr(self):
        node = Node("equal_expr")
        if self.debug:
            logger.debug("equal_expr:", self.current_token)
        node.add_node(self.compare_expr())
        node.add_node(self.equal_expr_tail())
        return node

    def equal_expr_tail(self):
        node = Node("equal_expr_tail")
        if self.debug:
            logger.debug("equal_expr_tail:", self.current_token)
        if isinstance(self.current_token, Eq):
            node.add_node(self.match(Eq))
            self.vm.add_op(Instruction.PUSH)
            node.add_node(self.compare_expr())
            self.vm.add_op(Instruction.EQ)
            node.add_node(self.equal_expr_tail())
        elif isinstance(self.current_token, Ne):
            node.add_node(self.match(Ne))
            self.vm.add_op(Instruction.PUSH)
            node.add_node(self.compare_expr())
            self.vm.add_op(Instruction.NE)
            node.add_node(self.equal_expr_tail())
        return node

    def compare_expr(self):
        node = Node("compare_expr")
        if self.debug:
            logger.debug("compare_expr:", self.current_token)
        node.add_node(self.sum_expr())
        node.add_node(self.compare_expr_tail())
        return node

    def compare_expr_tail(self):
        node = Node("compare_expr_tail")
        if self.debug:
            logger.debug("compare_expr_tail:", self.current_token)
        if isinstance(self.current_token, Lt):
            node.add_node(self.match(Lt))
            self.vm.add_op(Instruction.PUSH)
            node.add_node(self.sum_expr())
            self.vm.add_op(Instruction.LT)
            node.add_node(self.compare_expr_tail())
        elif isinstance(self.current_token, Gt):
            node.add_node(self.match(Gt))
            self.vm.add_op(Instruction.PUSH)
            node.add_node(self.sum_expr())
            self.vm.add_op(Instruction.GT)
            node.add_node(self.compare_expr_tail())
        elif isinstance(self.current_token, Le):
            node.add_node(self.match(Le))
            self.vm.add_op(Instruction.PUSH)
            node.add_node(self.sum_expr())
            self.vm.add_op(Instruction.LE)
            node.add_node(self.compare_expr_tail())
        elif isinstance(self.current_token, Ge):
            node.add_node(self.match(Ge))
            self.vm.add_op(Instruction.PUSH)
            node.add_node(self.sum_expr())
            self.vm.add_op(Instruction.GE)
            node.add_node(self.compare_expr_tail())
        return node

    def sum_expr(self):
        node = Node("sum_expr")
        if self.debug:
            logger.debug("sum_expr:", self.current_token)
        node.add_node(self.term())
        node.add_node(self.sum_expr_tail())
        return node

    def sum_expr_tail(self):
        """term + sum_expr_tail1 - sum_expr_tail2 + sum_expr_tail3"""
        node = Node("sum_expr_tail")
        if self.debug:
            logger.debug("sum_expr_tail:", self.current_token)
        if isinstance(self.current_token, Add):
            node.add_node(self.match(Add))
            self.vm.add_op(Instruction.PUSH)
            node.add_node(self.term())
            self.vm.add_op(Instruction.ADD)
            node.add_node(self.sum_expr_tail())
        elif isinstance(self.current_token, Sub):
            node.add_node(self.match(Sub))
            self.vm.add_op(Instruction.PUSH)
            node.add_node(self.term())
            self.vm.add_op(Instruction.SUB)
            node.add_node(self.sum_expr_tail())
        return node

    def term(self):
        node = Node("term")
        if self.debug:
            logger.debug("term:", self.current_token)
        node.add_node(self.factor())
        node.add_node(self.term_tail())
        return node

    def term_tail(self):
        """factor * term_tail1 / term_tail2 * term_tail3"""
        node = Node("term_tail")
        if self.debug:
            logger.debug("term_tail:", self.current_token)
        if isinstance(self.current_token, Mul):
            node.add_node(self.match(Mul))
            self.vm.add_op(Instruction.PUSH)
            node.add_node(self.factor())
            self.vm.add_op(Instruction.MUL)
            node.add_node(self.term_tail())
        elif isinstance(self.current_token, Div):
            node.add_node(self.match(Div))
            self.vm.add_op(Instruction.PUSH)
            node.add_node(self.factor())
            self.vm.add_op(Instruction.DIV)
            node.add_node(self.term_tail())
        elif isinstance(self.current_token, Mod):
            node.add_node(self.match(Mod))
            self.vm.add_op(Instruction.PUSH)
            node.add_node(self.factor())
            self.vm.add_op(Instruction.MOD)
            node.add_node(self.term_tail())
        return node

    def factor(self):
        node = Node("factor")
        if self.debug:
            logger.debug("factor:", self.current_token)
        if isinstance(self.current_token, Id):
            symbol = self.symbols.get_symbol(self.current_token.value)
            node.add_node(self.match(Id))
            if symbol.cls == IdClass.Var:
                if IdLevel(symbol.level) == IdLevel.Global:
                    # 取全局变量
                    self.vm.add_op(Instruction.IMM)
                    self.vm.add_op(symbol.value)
                    self.vm.add_op(Instruction.LI)
                else:
                    # 取局部变量
                    self.vm.add_op(Instruction.LEA)
                    self.vm.add_op(self.func_bp_index - symbol.value)
                    self.vm.add_op(Instruction.LI)
            elif symbol.cls == IdClass.Func or symbol.cls == IdClass.Sys:
                assert isinstance(self.current_token, Lparbrak)
                # 函数调用
                node.add_node(self.match(Lparbrak))
                num_args = 0
                while not isinstance(self.current_token, Rparbrak):
                    node.add_node(self.expr())
                    self.vm.add_op(Instruction.PUSH)
                    num_args += 1
                    if not isinstance(self.current_token, Comma):
                        break
                    node.add_node(self.match(Comma))
                node.add_node(self.match(Rparbrak))
                if symbol.cls == IdClass.Func:
                    # 用户函数
                    self.vm.add_op(Instruction.CALL)
                    self.vm.add_op(symbol.value)
                else:
                    # 系统函数
                    self.vm.add_op(symbol.value)
                if num_args > 0:
                    self.vm.add_op(Instruction.ADJ)
                    self.vm.add_op(num_args)
        elif isinstance(self.current_token, Num):
            self.vm.add_op(Instruction.IMM)
            self.vm.add_op(self.current_token.value)
            node.add_node(self.match(Num))
        elif isinstance(self.current_token, Chr):
            self.vm.add_op(Instruction.IMM)
            self.vm.add_op(ord(self.current_token.value))
            node.add_node(self.match(Chr))
        elif isinstance(self.current_token, Lparbrak):
            node.add_node(self.match(Lparbrak))
            node.add_node(self.expr())
            node.add_node(self.match(Rparbrak))
        else:
            raise Exception(f"Unexpected symbol: {self.current_token}")
        return node

    def type(self):
        node = Node("type")
        if self.debug:
            logger.debug("type:", self.current_token)
        if isinstance(self.current_token, Int):
            node.add_node(self.match(Int))
            self.base_type = IdType.Int
        elif isinstance(self.current_token, Float):
            node.add_node(self.match(Float))
            self.base_type = IdType.Float
        elif isinstance(self.current_token, Char):
            node.add_node(self.match(Char))
            self.base_type = IdType.Char
        elif isinstance(self.current_token, Void):
            node.add_node(self.match(Void))
            self.base_type = IdType.Void
        else:
            raise Exception(f"Unexpected symbol: {self.current_token}")
        return node

    def declare(self):
        # 局部变量声明
        node = Node("declare")
        if self.debug:
            logger.debug("declare:", self.current_token)
        node.add_node(self.type())
        id_token = self.current_token
        assert isinstance(id_token, Id)
        node.add_node(self.match(Id))
        assert IdLevel(self.symbols.level) == IdLevel.Local
        self.func_num_local_vars += 1

        symbol = Symbol(
            name=id_token.value,
            cls=IdClass.Var,
            data_type=self.base_type,
            level=IdLevel(self.symbols.level),
            value=self.func_bp_index + self.func_num_local_vars,
        )

        self.symbols.set_symbol(symbol)
        return node

    def stmt(self):
        node = Node("stmt")
        if self.debug:
            logger.debug("stmt:", self.current_token)
        if isinstance(self.current_token, Id):
            id_name = self.current_token.value
            symbol = self.symbols.get_symbol(id_name)
            if IdLevel(symbol.level) == IdLevel.Global:
                self.vm.add_op(Instruction.IMM)
                self.vm.add_op(symbol.value)
            else:
                self.vm.add_op(Instruction.LEA)
                self.vm.add_op(self.func_bp_index - symbol.value)
            self.vm.add_op(Instruction.PUSH)
            node.add_node(self.match(Id))
            node.add_node(self.match(Assign))
            node.add_node(self.expr())
            node.add_node(self.match(Semi))

            self.vm.add_op(Instruction.SI)
        elif isinstance(self.current_token, (Int, Float, Char, Void)):
            node.add_node(self.declare())
            node.add_node(self.match(Semi))
        elif isinstance(self.current_token, Return):
            node.add_node(self.match(Return))
            node.add_node(self.expr())
            node.add_node(self.match(Semi))
            self.vm.add_op(Instruction.LEV)
        elif isinstance(self.current_token, If):
            node.add_node(self.match(If))
            node.add_node(self.match(Lparbrak))
            node.add_node(self.expr())
            node.add_node(self.match(Rparbrak))
            self.vm.add_op(Instruction.JZ)
            self.vm.add_op(Instruction.PLAC)  # placeholder for jump address
            jump_address = self.vm.get_op_pointer(-1)
            node.add_node(self.stmt())
            if isinstance(self.current_token, Else):
                node.add_node(self.match(Else))
                jump_to = self.vm.get_op_pointer(2)
                send_integer_to_pointer(jump_address, jump_to)
                self.vm.add_op(Instruction.JMP)
                self.vm.add_op(Instruction.PLAC)
                jump_address = self.vm.get_op_pointer(-1)
                node.add_node(self.stmt())
            jump_to = self.vm.get_op_pointer(0)
            send_integer_to_pointer(jump_address, jump_to)
        elif isinstance(self.current_token, While):
            node.add_node(self.match(While))

            loop_start = self.vm.get_op_pointer(0)

            node.add_node(self.match(Lparbrak))
            node.add_node(self.expr())
            node.add_node(self.match(Rparbrak))

            self.vm.add_op(Instruction.JZ)
            self.vm.add_op(Instruction.PLAC)
            loop_end = self.vm.get_op_pointer(-1)

            node.add_node(self.stmt())

            self.vm.add_op(Instruction.JMP)
            self.vm.add_op(loop_start)
            send_integer_to_pointer(loop_end, self.vm.get_op_pointer(0))
        elif isinstance(self.current_token, Lcurbrak):
            node.add_node(self.match(Lcurbrak))
            node.add_node(self.stmts())
            node.add_node(self.match(Rcurbrak))
        return node

    def else_branch(self):
        node = Node("else_branch")
        if self.debug:
            logger.debug("else_branch:", self.current_token)
        if isinstance(self.current_token, Else):
            node.add_node(self.match(Else))
            node.add_node(self.stmt())
        return node

    def stmts(self):
        node = Node("stmts")
        if self.debug:
            logger.debug("stmts:", self.current_token)
        if isinstance(self.current_token, (Id, Num, Chr, Lparbrak, Int, Float, Char, Void, Return, If, While)):
            node.add_node(self.stmt())
            node.add_node(self.stmts())
        return node

    def start(self):
        node = Node("start")
        if self.debug:
            logger.debug("start:", self.current_token)
        if isinstance(self.current_token, (Int, Float, Char, Void)):
            node.add_node(self.start_tail())
            node.add_node(self.start())
        return node

    def start_tail(self):
        node = Node("start_tail")
        if self.debug:
            logger.debug("start_tail:", self.current_token)
        node.add_node(self.type())
        id_token = self.current_token
        node.add_node(self.match(Id))
        assert isinstance(id_token, Id)
        if isinstance(self.current_token, Lparbrak):
            # 函数声明
            func_ptr = self.vm.get_op_pointer(offset=0)
            symbol = Symbol(
                name=id_token.value,
                cls=IdClass.Func,
                data_type=self.base_type,
                level=IdLevel(self.symbols.level),
                value=func_ptr,
            )
            self.symbols.set_symbol(symbol)
            self.symbols.enter_scope()
            self.reset_func_recorders()
            node.add_node(self.match(Lparbrak))
            node.add_node(self.func_params())
            node.add_node(self.match(Rparbrak))
            if isinstance(self.current_token, Lcurbrak):
                node.add_node(self.match(Lcurbrak))
                while isinstance(self.current_token, (Int, Char, Void, Float)):
                    self.declare()
                    self.match(Semi)
                self.vm.add_op(Instruction.ENT)
                self.vm.add_op(self.func_num_local_vars)
                node.add_node(self.stmts())
                node.add_node(self.match(Rcurbrak))
                self.vm.add_op(Instruction.LEV)
            self.symbols.leave_scope()
        else:
            # 全局变量声明
            assert IdLevel(self.symbols.level) == IdLevel.Global
            data_ptr = self.vm.put_int_onto_data(0)
            symbol = Symbol(
                name=id_token.value,
                cls=IdClass.Var,
                data_type=self.base_type,
                level=IdLevel(self.symbols.level),
                value=data_ptr,
            )

            node.add_node(self.match(Semi))
            self.symbols.set_symbol(symbol)
        return node

    def func_params(self):
        node = Node("func_params")
        if self.debug:
            logger.debug("func_params:", self.current_token)
        while isinstance(self.current_token, (Int, Float, Char, Void)):
            node.add_node(self.type())
            id_token = self.current_token
            node.add_node(self.match(Id))
            assert isinstance(id_token, Id)
            symbol = Symbol(
                name=id_token.value,
                cls=IdClass.Var,
                data_type=self.base_type,
                level=IdLevel(self.symbols.level),
                value=self.func_num_params,
            )
            self.func_num_params += 1
            self.func_bp_index = self.func_num_params + 1
            self.symbols.set_symbol(symbol)
            if not isinstance(self.current_token, Comma):
                break
            node.add_node(self.match(Comma))
        return node

    def match(self, token_cls: Type[Token]):
        if isinstance(self.current_token, token_cls):
            node = TerminalNode(str(self.current_token))
            if self.debug:
                logger.debug(f"match {self.current_token} -> {token_cls.__name__}")
            self.current_token = self.next_token()
            return node
        else:
            raise Exception(f"{self.current_token} does not match {token_cls.__name__}")

    def next_token(self) -> Optional[Token]:
        try:
            return self.lexer.__next__()
        except StopIteration:
            return None
