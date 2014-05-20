from datatypes import sym, linked_list
from bytecodes import *

def compile_(ast):
    codes = [compile_expr(expr) for expr in ast]
    out = []
    for code in codes:
        out += code
    return out
                
def compile_expr(expr):
    if isinstance(expr, sym):
        return [(Bytecode.REF, expr)]
    elif isinstance(expr, linked_list):
        if expr[0] == sym('define'):
            out = []
            if not isinstance(expr[1], sym):
                raise AssertionError('Bad syntax in define')
            out += compile_expr(expr[2])
            out += [(Bytecode.DEF,expr[1])]
            out += [(Bytecode.PUSH, None)]
            return out
        elif expr[0] == sym('begin'):
            out = []
            for expr in begin:
                out += compile_expr(expr)
                out += [(Bytecode.POP,)]
            return out[:-1]

        elif expr[0] == sym('lambda'):
            func_label = label()
            end_label = label()
            args = expr[1]
            out = []
            out += [(Bytecode.LAMBDA, (func_label, len(args)))]
            out += [(Bytecode.GOTO, end_label)]
            out += [(Bytecode.LABEL, func_label)]
            for arg in args:
                if not isinstance(arg, sym):
                    raise AssertionError('Bad syntax in lambda')
                out += [(Bytecode.DEF, arg)]
            out += compile_expr(expr[2])
            out += [(Bytecode.RETURN,)]
            out += [(Bytecode.LABEL, end_label)]
            return out
        
        elif expr[0] == sym('if'):
            then_label = label()
            end_label = label()
            out = []
            out += compile_expr(expr[1])
            out += [(Bytecode.BRANCH,then_label)]
            out += compile_expr(expr[3])
            out += [(Bytecode.GOTO, end_label)]
            out += [(Bytecode.LABEL, then_label)]
            out += compile_expr(expr[2])
            out += [(Bytecode.LABEL, end_label)]
            return out

        else:
            args = len(expr) - 1
            out = []
            for sub_expr in reversed(expr):
                out += compile_expr(sub_expr)
            out += [(Bytecode.CALL, args)]
            return out
            
    else:
        return [(Bytecode.PUSH, expr)]

if __name__ == '__main__':
    import tokenizer
    import parser_
    while True:
        src = eval(input('compiler> '))
        tokens = tokenizer.tokenize(src)
        ast = parser_.parse(tokens)
        bytecodes = compile_(ast)
        for b in bytecodes:
            print(b)
