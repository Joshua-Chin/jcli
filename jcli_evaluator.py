from jcli_datatypes import linked_list, sym, quote, closure, car, cdr, cons, null

import jcli_tokenizer
import jcli_parser
import operator

jcli_globals = {
    sym('eval'): lambda x: (
        eval_ast(x.value, closure(jcli_globals))
        if isinstance(x, quote)
        else x),
    sym('+'): operator.add,
    sym('-'): operator.sub,
    sym('*'): operator.mul,
 #   sym('/'): operator.div,
    sym('='): operator.eq,
    sym('or'): lambda x,y: x or y,
    sym('and'): lambda x,y: x and y,
    sym('not'): lambda x: not x,
    sym('cons'): lambda x,y: cons(x, y.value),
    sym('car'): lambda x: car(x.value),
    sym('cdr'): lambda x: cdr(x.value),}

def eval(string, bindings=None, builtins=None):
    if builtins is None:
        builtins = jcli_globals
    if bindings is None:
        bindings = closure(builtins)
    else:
    	bindings = {sym(k): bindings[k] for k in bindings.keys()}
        bindings.update(builtins)
    asts = jcli_parser.parse(string)
    return list(map(lambda ast: eval_ast(ast, bindings), asts))


def eval_ast(ast, env):
    try:
        while isinstance(ast, (jcli_parser.syntax, sym, linked_list, hack)):
            if isinstance(ast, jcli_parser.syntax):
                ast = simplify(ast.value, env)
            else:
                ast = simplify(ast, env);
    except EvaluatorError:
        raise
    except Exception as e:
        if isinstance(ast, jcli_parser.syntax):
            raise EvaluatorError(
                'line %s, char %s: %s'
                %(ast.line_no, ast.char_no, str(e)))
        raise
    return ast

class hack(tuple):pass
    
def simplify(expr, env):
    if isinstance(expr, sym):
        try:
            return env[expr]
        except KeyError:
            raise NameError("symbol %s is not defined"%(expr,))
    elif isinstance(expr, hack):
        return simplify(expr[0], expr[1])
    elif isinstance(expr, linked_list):
        f = expr[0]
        if isinstance(f, jcli_parser.syntax):
            f=f.value
        if f == sym('define'):
            if len(expr) != 3:
                raise SyntaxError("bad syntax in define")
            env[expr[1].value] = eval_ast(expr[2], env)
        elif f == sym('lambda'):
            if len(expr) != 3:
                raise SyntaxError("bad syntax in lambda")                
            arg_names = expr[1].value
            body = expr[2]
            def function(*args):
                c = closure(env)
                if len(arg_names) != len(args):
                    raise TypeError(
                        'function expected %s arguments, got %s'
                        %(len(arg_names), len(args)))
                for arg_name, arg in zip(arg_names, args):
                    c[arg_name.value] = arg
                out = hack((body.value, c))
                return out
            return function
        elif f == sym('if'):
            if len(expr) != 4:
                raise SyntaxError("bad syntax in if")
            if eval_ast(expr[1], env):
                return hack((expr[2].value, env))
            else:
                return hack((expr[3].value, env))
        elif f == sym('quote'):
            if len(expr) != 2:
                raise SyntaxError("bad syntax in quote")
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

class EvaluatorError(Exception):
    pass

def apply(function, iterable):
    return function(*list(iterable))


if __name__ == '__main__':
    builtins = closure(jcli_globals)
    eval("""
(define recursion-test
(lambda (x)
(if (= x 0) 0 (recursion-test (- x 1))))) (recursion-test 1000)""", builtins)
    while True:
        for result in eval(raw_input('rkt> '), builtins):
            print(result)
