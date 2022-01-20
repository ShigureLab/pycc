from pycc.symbols import SymbolTable, Symbol


def test_symbols():
    symbols = SymbolTable()
    # scope 0 level 0
    built_in_printf = symbols.set_symbol(Symbol(name="printf"))
    built_in_sizeof = symbols.set_symbol(Symbol(name="sizeof"))

    symbols.enter_scope()
    # scope 1 level 1
    assert symbols.scope_id == 1
    assert symbols.level == 1
    global_a = symbols.set_symbol(Symbol(name="a"))
    global_b = symbols.set_symbol(Symbol(name="b"))
    assert symbols.get_symbol("a") is global_a

    symbols.enter_scope()
    # scope 2 level 2
    assert symbols.scope_id == 2
    assert symbols.level == 2
    scope_2_a = symbols.set_symbol(Symbol(name="a"))
    scope_2_c = symbols.set_symbol(Symbol(name="c"))
    assert symbols.get_symbol("a") is scope_2_a
    assert symbols.get_symbol("b") is global_b
    assert symbols.get_symbol("c") is scope_2_c
    assert symbols.get_symbol("printf") is built_in_printf
    symbols.leave_scope()
    # scope 1 level 1
    assert symbols.scope_id == 1
    assert symbols.level == 1

    symbols.enter_scope()
    # scope 3 level 2
    assert symbols.scope_id == 3
    assert symbols.level == 2
    scope_3_a = symbols.set_symbol(Symbol(name="a"))
    assert symbols.get_symbol("a") is scope_3_a
    assert symbols.get_symbol("a") is not scope_2_a
    assert symbols.get_symbol("printf") is built_in_printf
    assert symbols.get_symbol("sizeof") is built_in_sizeof
    symbols.leave_scope()
    # scope 1 level 1
    assert symbols.scope_id == 1
    assert symbols.level == 1
    symbols.leave_scope()
    # scope 0 level 0
    assert symbols.scope_id == 0
    assert symbols.level == 0
