from functools import wraps

import tokenizer
import parser_
import compiler
import assembler
import executor
from jcli_builtins import jcli_builtins
from datatypes import sym

def jcli_exec(srcs, steps, step, spr, callbacks=None, builtins=None):
    if builtins is None:
        builtins = jcli_builtins
    executors = []
    for index, src in enumerate(srcs):
        globals_ = dict(builtins)
        globals_.update(gen_callbacks(index, callbacks))
        executors.append(eval_lisp(src, globals_))
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
            except Exception as e:
                out[index] = e.args[0]
                executors[index] = None
    return out

def gen_callbacks(index, callbacks):
    return {sym(string) : gen_callback(function)
           for string, function in callbacks.items()}

def gen_callback(index, function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        return function(index, *args, **kwargs)
    return wrapper

def eval_lisp(src, builtins=None):
    if builtins is None:
        builtins = dict(jcli_builtins)
    return execute_lisp(compile_lisp(src), builtins)

def compile_lisp(src):
    tokens = tokenizer.tokenize(src)
    ast = parser_.parse(tokens)
    asm = compiler.compile_(ast)
    bytecode = assembler.assemble(asm)
    return bytecode

def execute_lisp(bytecode, builtins=None):
    if builtins is None:
        builtins = dict(jcli_builtins)
    return executor.execute_bytecodes(bytecode, builtins)
