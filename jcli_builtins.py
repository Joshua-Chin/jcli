import operator
from datatypes import sym

jcli_builtins = {
    sym('print'): print,
    sym('+'): operator.add,
    sym('-'): operator.sub,
    sym('/'): operator.truediv,
    sym('*'): operator.mul,
    sym('pow'): operator.pow,
    sym('abs'): operator.abs,
    sym('mod'): operator.mod,
    sym('='): operator.eq,
    sym('!='): operator.ne,
    sym('<'): operator.lt,
    sym('<='): operator.le,
    sym('>'): operator.gt,
    sym('>='): operator.ge,
    sym('not'): operator.not_,
    sym('or'): operator.or_,
    sym('and'): operator.and_,
    sym('equal?'):operator.is_,}
