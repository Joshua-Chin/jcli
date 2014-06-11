from datatypes import sym, linked_list
from bytecodes import *

def compile_(ast):
    out = []
    for expr in ast:
        try:
            out += compile_expr(expr)
        except RuntimeError as e:
            raise SyntaxError(e.args[0])
    return out

class line_no(tuple):pass
                
def compile_expr(expr):
    if isinstance(expr, sym):
        return [(Bytecode.REF, expr)]
    elif isinstance(expr, linked_list):
        if expr[0][0] == sym('define'):
            out = []
            if len(expr) != 3 or not isinstance(expr[1][0], sym):
                raise SyntaxError('Bad syntax in define')
            out += compile_expr(expr[2])
            out += [(Bytecode.DEF,expr[1][0])]
            out += [(Bytecode.REF,expr[1][0])]
            return out
        elif expr[0][0] == sym('begin'):
            out = []
            for expr in expr[1:]:
                out += compile_expr(expr)
                out += [(Bytecode.POP,)]
            return out[:-1]

        elif expr[0][0] == sym('lambda'):
            if len(expr) != 3 or not isinstance(expr[1][0], linked_list):
                raise SyntaxError('Bad syntax in lambda')
            func_label = label()
            end_label = label()
            args = expr[1][0]
            out = []
            func = []
            out += [(Bytecode.LAMBDA, (func, len(args)))]
            for arg in args:
                if not isinstance(arg[0], sym):
                    raise SyntaxError('Bad syntax in lambda')
                func += [(Bytecode.DEF, arg[0])]
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
        try:
            return syntax_lines(compile_expr(expr[0]), expr[1])
        except SyntaxError as e:
            raise RuntimeError("Syntax error at line %s: "%expr[1]+e.args[0])
    else:
        return [(Bytecode.PUSH, expr)]

def syntax_lines(expr, line):
    out = []
    for op in expr:
        if isinstance(op, line_no):
            out.append(op)
        elif op[0] == Bytecode.LAMBDA:
            codes = op[1][0]
            codes = syntax_lines(codes, line)
            out.append(line_no(((op[0], (codes, op[1][1])), line)))
        else:
            out.append(line_no((op,line)))
    return out

if __name__ == '__main__':
    import tokenizer
    import parser_
    try:
        raw_input
    except NameError:
        raw_input = input
    while True:
        src = raw_input('compiler> ')
        tokens = tokenizer.tokenize(src)
        ast = parser_.parse(tokens)
        bytecodes = compile_(ast)
        for b in bytecodes:
            print(b)
