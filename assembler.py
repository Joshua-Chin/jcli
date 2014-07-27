from bytecodes import Bytecode, label

def assemble(assembly):
    labels = {}
    for index, instr in enumerate(assembly):
        line = instr[1]
        instr = instr[0]
        if instr[0] == Bytecode.LABEL:
            labels[instr[1]] = index
            assembly[index] = (Bytecode.LABEL,), line
    for index, instr in enumerate(assembly):
        line = instr[1]
        instr = instr[0]
        if (instr[0] == Bytecode.GOTO or
            instr[0] == Bytecode.BRANCH):
            assembly[index] = (instr[0], labels[instr[1]]), line
        if instr[0]  == Bytecode.LAMBDA:
            assembly[index] = (instr[0], (assemble(instr[1][0]), instr[1][1])), line
    return assembly

if __name__ == '__main__':
    import tokenizer
    import parser_
    import compiler
    while True:
        src = raw_input('assembler> ')
        tokens = tokenizer.tokenize(src)
        ast = parser_.parse(tokens)
        asm = compiler.compile_(ast)
        bc = assemble(asm)
        for b in bc:
            print(b)
