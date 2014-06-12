import types

from bytecodes import Bytecode
from datatypes import frame, function, sym

def execute_bytecodes(bytecodes, builtins=None, debug=False):
    if builtins is None:
        builtins = frame()
        
    exec_stack = []
    call_stack = []
    instr_ptr = 0
    env = builtins

    while instr_ptr < len(bytecodes):
        bytecode = bytecodes[instr_ptr][0]
        line = bytecodes[instr_ptr][1]
        instr = bytecode[0]
        try:
            if instr == Bytecode.POP:
                exec_stack.pop()
            elif instr == Bytecode.PUSH:
                exec_stack.append(bytecode[1])
            elif instr == Bytecode.DEF:
                env[bytecode[1]] = exec_stack.pop()
            elif instr == Bytecode.REF:
                try:
                    exec_stack.append(env[bytecode[1]])
                except KeyError:
                    raise NameError("%s is not defined"%bytecode[1])
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
                    call_stack.append((bytecodes, instr_ptr, env))
                    instr_ptr = -1
                    bytecodes = func[0]
                    env = frame(func[1])
                    if func[2] != bytecode[1]:
                        raise RuntimeError('incorrect # of args')
            elif instr == Bytecode.RETURN:
                bytecodes, instr_ptr, env = call_stack.pop()
            elif instr == Bytecode.LABEL:
                pass
            else:
                raise RuntimeError('unknown bytecode: '+bytecode)
        except Exception as e:
            if debug:
                raise e
            raise RuntimeError("Error at line %s: "%line+e.args[0])
        instr_ptr += 1
        yield
    if debug:
        for expr in exec_stack:
            print(expr)
                
if __name__ == '__main__':
    import tokenizer
    import parser_
    import compiler
    import assembler
    import operator
    from builtins_ import jcli_builtins
    try:
        raw_input
    except NameError:
        raw_input = input
    globals_ = dict(jcli_builtins)
    while True:
        try:
            src = raw_input('executor> ')
            tokens = tokenizer.tokenize(src)
            ast = parser_.parse(tokens)
            asm = compiler.compile_(ast)
            bc = assembler.assemble(asm)
            ex = execute_bytecodes(bc, globals_, debug=True)
            while True:
                try:
                    next(ex)
                except StopIteration as e:
                    break
        except Exception as e:
            print(e.args[0])
