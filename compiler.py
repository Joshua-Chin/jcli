from datatypes import sym, linked_list
from bytecodes import *

def compile_(ast):
    out = []
    for expr in ast:
        try:
            out += compile_expr(expr)
        except RuntimeError as e:
            raise SyntaxError(e.message)
    return out

class line_no(tuple):pass
                
def compile_expr(expr):
    if isinstance(expr, sym):
        return [(Bytecode.REF, expr)]
    elif isinstance(expr, linked_list):
        if expr[0][0] == sym('define'):
            out = []
            if not isinstance(expr[1][0], sym) or len(expr) != 3:
                raise SyntaxError('Bad syntax in define')
            out += compile_expr(expr[2])
            out += [(Bytecode.DEF,expr[1])]
            out += [(Bytecode.PUSH, None)]
            return out
        elif expr[0][0] == sym('begin'):
            out = []
            for expr in expr[1:]:
                out += compile_expr(expr)
                out += [(Bytecode.POP,)]
            return out[:-1]

        elif expr[0][0] == sym('lambda'):
            if len(expr) != 3:
                raise SyntaxError('Bad syntax in lambda')
            func_label = label()
            end_label = label()
            args = expr[1][0]
            out = []
            func = []
            out += [(Bytecode.LAMBDA, (func, len(args)))]
            for arg in args:
                if not isinstance(arg, sym):
                    raise SyntaxError('Bad syntax in lambda')
                func += [(Bytecode.DEF, arg)]
            func += compile_expr(expr[2])
            func += [(Bytecode.RETURN,)]
            return out
        
        elif expr[0][0] == sym('if'):
            if len(expr) != 4:
                raise SyntaxError('Bad syntax in if')
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
            
    elif isinstance(expr, tuple):
        line = expr[1]
        try:
            ops = compile_expr(expr[0])
            return [line_no((op,line)) if not isinstance(op, line_no) else op for op in ops]
        except SyntaxError as e:
            raise RuntimeError("Syntax error at line %s: "%line+e.message)

    else:
        return [(Bytecode.PUSH, expr)]

if __name__ == '__main__':
    import tokenizer
    import parser_
    while True:
        src = raw_input('compiler> ')
        tokens = tokenizer.tokenize(src)
        ast = parser_.parse(tokens)
        bytecodes = compile_(ast)
        for b in bytecodes:
            print(b)
