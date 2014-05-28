import tokenizer
import parser_
import compiler
import assembler
import executor
from jcli_builtins import jcli_builtins
from datatypes import sym

def jcli_exec(srcs, iterations, callbacks=None, builtins=None):
    if builtins is None:
        builtins = jcli_builtins
    executors = []
    for index, src in enumerate(srcs):
        globals_ = dict(builtins)
        globals_.update(gen_callbacks(index, callbacks))
        executors.append(eval_list(src))
    out = [None]*len(srcs)
    for _ in range(iterations):
        for index, executor in enumerate(executors):
            try:
                next(executor)
            except StopIteration:
                pass
            except Exception as e:
                out[index] = type(e).__name__ + ": " + e.message
    return out

def gen_callbacks(index, callbacks):
        return {sym(s):lambda *args, **kwargs: f(index, *args, **kwargs)
                for s,f in callbacks.items()}

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
