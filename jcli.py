import tokenizer
import parser_
import compiler
import assembler
import executor
from jcli_builtins import jcli_builtins

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
