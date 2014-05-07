from jcli_datatypes import linked_list, sym, quote, closure, car, cdr, cons, null

import jcli_tokenizer
import jcli_parser
import operator

jcli_globals = {
    sym('+'): operator.add,
    sym('-'): operator.sub,
    sym('*'): operator.mul,
 #   sym('/'): operator.div,
    sym('='): operator.eq,
    sym('or'): lambda x,y: x or y,
    sym('and'): lambda x,y: x and y,
    sym('not'): lambda x: not x,
    sym('cons'): cons,
    sym('car'): car,
    sym('cdr'): cdr,}

def eval(string):
    asts = jcli_parser.parse(string)
    return list(map(lambda ast: eval_ast(ast, jcli_globals), asts))


def eval_ast(ast, env):
    while isinstance(ast, jcli_parser.syntax):
        ast = simplify(ast.value, env)
    if isinstance(ast, quote):
        return ast.value
    return ast
    
def simplify(expr, env):
    if isinstance(expr, sym):
        return env[expr]
    elif isinstance(expr, linked_list):
        f = expr[0].value
        if f == sym('define'):
            env[expr[1].value] = eval_ast(expr[2], env)
        elif f == sym('lambda'):
            arg_names = expr[1].value
            body = expr[2]
            def function(*args):
                c = closure(env)
                for arg_name, arg in zip(arg_names, args):
                    c[arg_name.value] = arg
                    return eval_ast(body, c)
            return function
        elif f == sym('if'):
            if eval_ast(expr[1], env):
                return expr[2]
            else:
                return expr[3]
        elif f == sym('quote'):
            return quote(jcli_parser.syntax_to_list(expr[1]))
        elif f == sym('begin'):
            out = None
            for sub_expr in cdr(expr):
                out = eval_ast(sub_expr, env)
            return out
        else:
            return apply(
                eval_ast(expr[0], env),
                map(lambda x: eval_ast(x, env), cdr(expr)))
    else:
        return expr



def apply(function, iterable):
    return function(*list(iterable))

if __name__ == '__main__':
    while True:
        print(eval(input('rkt>')))
