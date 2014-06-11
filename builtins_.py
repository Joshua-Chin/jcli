from __future__ import print_function, division
import operator

from functools import wraps
from datatypes import sym, linked_list, cons, car, cdr, null

try:
    div = operator.div
except AttributeError:
    div = operator.truediv

def f(func):
    @wraps(func)
    def wrapper(*args):
        return all(map(lambda arg:func(*arg), zip(args, args[1:])))
    return wrapper

jcli_builtins = {
    sym('+'): lambda *args:sum(args),
    sym('-'): lambda *args: -args[0] if len(args)==1 else args[0]-sum(args[1:]),
    sym('/'): lambda *args: 1/args[0] if len(args)==1 else args[0]/reduce(operator.mul, args, 1),
    sym('*'): lambda *args:reduce(operator.mul, args, 1),
    sym('expt'): operator.pow,
    sym('abs'): operator.abs,
    sym('modulo'): operator.mod,
    sym('='): f(operator.eq),
    sym('!='): f(operator.ne),
    sym('<'): f(operator.lt),
    sym('<='): f(operator.le),
    sym('>'): f(operator.gt),
    sym('>='): f(operator.ge),
    sym('not'): operator.not_,
    sym('or'): lambda *args:any(args),
    sym('and'): lambda *args:all(args),
    sym('equal?'): f(operator.is_),
    sym('list'): lambda *args:linked_list(args),
    sym('cons'): cons,
    sym('car'): car,
    sym('cdr'): cdr,
    sym('null'): null,
    sym('null?'): lambda x: x is null,
    }