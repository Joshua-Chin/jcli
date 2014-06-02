from __future__ import print_function, division
import operator
from datatypes import sym, linked_list, cons, car, cdr, null

try:
    div = operator.div
except AttributeError:
    div = operator.truediv

jcli_builtins = {
    sym('+'): operator.add,
    sym('-'): operator.sub,
    sym('/'): div,
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
    sym('equal?'):operator.is_,
	sym('list'):lambda *args:linked_list(args),
	sym('cons'):cons,
	sym('car'):car,
	sym('cdr'):cdr,
	sym('null'):null}
