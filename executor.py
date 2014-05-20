import types

from bytecodes import Bytecode
from datatypes import frame, function, sym

def execute_bytecodes(bytecodes, builtins=None):
    if builtins is None:
        builtins = frame()
        
    exec_stack = []
    call_stack = []
    instr_ptr = 0
    env = builtins

    while instr_ptr < len(bytecodes):
        bytecode = bytecodes[instr_ptr]
        instr = bytecode[0]

        if instr == Bytecode.POP:
            exec_stack.pop()
        elif instr == Bytecode.PUSH:
            exec_stack.append(bytecode[1])
        elif instr == Bytecode.DEF:
            env[bytecode[1]] = exec_stack.pop()
        elif instr == Bytecode.REF:
            exec_stack.append(env[bytecode[1]])
        elif instr == Bytecode.GOTO:
            instr_ptr = bytecode[1]
        elif instr == Bytecode.BRANCH:
            if exec_stack.pop():
                instr_ptr = bytecode[1]
        elif instr == Bytecode.LAMBDA:
            b = bytecode
            exec_stack.append(function((b[1][0], env, b[1][1])))
        elif instr == Bytecode.CALL:
            func = exec_stack.pop()
            if hasattr(func, '__call__'):
                args = [exec_stack.pop()
                        for _ in range(bytecode[1])]
                exec_stack.append(func(*args))
            else:
                call_stack.append((instr_ptr, env))
                instr_ptr = func[0]
                env = frame(func[1])
                if func[2] != bytecode[1]:
                    raise AssertionError('incorrect # of args')
        elif instr == Bytecode.RETURN:
            instr_ptr, env = call_stack.pop()
        elif instr == Bytecode.LABEL:
            pass
        else:
            raise AssertionError('unknown bytecode: '+bytecode)
        instr_ptr += 1
    return exec_stack
                
if __name__ == '__main__':
    import tokenizer
    import parser_
    import compiler
    import assembler
    import operator
    from jcli_builtins import jcli_builtins
    globals_ = dict(jcli_builtins)
    while True:
        src = raw_input('executor> ')
        tokens = tokenizer.tokenize(src)
        ast = parser_.parse(tokens)
        asm = compiler.compile_(ast)
        bc = assembler.assemble(asm)
        for result in (execute_bytecodes(bc, globals_)):
            print(result)
