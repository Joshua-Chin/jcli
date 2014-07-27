import StringIO
import traceback

from functools import wraps

import tokenizer
import parser_
import compiler
import assembler
import executor
from builtins_ import jcli_builtins
from datatypes import sym

def jcli_exec(srcs, steps, step, spr, callbacks=None, builtins=None, includes=None,debug=False):
    """Executes a list of sources in parallel
    srcs  [str]:  a list of sources, with the index corresponding to the id
    
    steps int:    the maximum number of steps a single source can execute
    step  func(): the function called after every single step has been executed
                  for all sources
    spr   int:    the granularity of each step
    
    callbacks {str:func(int, *args)}: a list of functions available to the
                                      sources, the first argument passed into
                                      the function is the source id
    builtins  {str:func(*args)}:      a list of functions available to the sources
    includes  str OR [str]:           a string or list of strings representing
                                      jcli src that will be executed before the
                                      main src is executed
    """
    if builtins is None:
        builtins = jcli_builtins
    if includes is None:
        includes = open('includes.jcli').read()
    if isinstance(includes, str):
        includes = [includes]
    for include in includes:
        for step in eval_lisp(include, builtins): pass
    executors = []
    for index, src in enumerate(srcs):
        globals_ = dict(builtins)
        globals_.update(gen_callbacks(index, callbacks))
        executors.append(eval_lisp(src, globals_, debug))
    out = ["Out of Time"]*len(srcs)
    for step_count in range(steps*spr):
        if not step_count % spr:
            step()
        for index, executor in enumerate(executors):
            if executor is None:
                continue
            try:
                next(executor)
            except StopIteration:
                executors[index] = None
                out[index] = None
            except Exception as e:
                if debug:
                    f = StringIO.StringIO()
                    traceback.print_tb(e, file=f)
                    out[index] = f.getvalue()
                    f.close()
                else:
                    out[index] = e.args[0]
                executors[index] = None
    return out

def gen_callbacks(index, callbacks):
    return {sym(string) : gen_callback(index, function)
           for string, function in callbacks.items()}

def gen_callback(index, function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        return function(index, *args, **kwargs)
    return wrapper

def eval_lisp(src, builtins=None, debug=False):
    if builtins is None:
        builtins = dict(jcli_builtins)
    return execute_lisp(compile_lisp(src), builtins, debug)

def compile_lisp(src):
    tokens = tokenizer.tokenize(src)
    ast = parser_.parse(tokens)
    asm = compiler.compile_(ast)
    bytecode = assembler.assemble(asm)
    return bytecode

def execute_lisp(bytecode, builtins=None, debug=False):
    if builtins is None:
        builtins = dict(jcli_builtins)
    return executor.execute_bytecodes(bytecode, builtins, debug)
    
if __name__ == '__main__':
    import tokenizer
    import parser_
    import compiler
    import assembler
    import operator
    import executor
    
    from builtins_ import jcli_builtins as builtins
    try:
        raw_input
    except NameError:
        raw_input = input
    includes = open('includes.jcli').read()
    if isinstance(includes, str):
        includes = [includes]
    for include in includes:
        for step in eval_lisp(include, builtins): pass
    globals_ = dict(builtins)
    while True:
        try:
            src = raw_input('executor> ')
            tokens = tokenizer.tokenize(src)
            ast = parser_.parse(tokens)
            asm = compiler.compile_(ast)
            bc = assembler.assemble(asm)
            ex = executor.execute_bytecodes(bc, globals_, debug=True)
            while True:
                try:
                    next(ex)
                except StopIteration as e:
                    break
        except Exception as e:
            print(e.args[0])
