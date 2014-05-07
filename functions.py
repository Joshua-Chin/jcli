from linked_list import linked_list

def eval(syntax, env):
    expr = syntax
    while isinstance(expr, (linked_list, sym)):
        expr = simplfiy(expr, env)
    return expr
    
def simplify(expr, env):
    if isinstance(expr, sym):
        return env[sym]
    if isinstance()

def apply(function, iterable):
    function(*list(iterable))
