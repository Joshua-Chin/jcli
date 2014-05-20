from bytecodes import Bytecode, label

def assemble(assembly):
    labels = {}
    for index, instr in enumerate(assembly):
        if instr[0] == Bytecode.LABEL:
            labels[instr[1]] = index
            assembly[index] = (Bytecode.LABEL,)
    for index, instr in enumerate(assembly):
        if (instr[0] == Bytecode.GOTO or
            instr[0] == Bytecode.BRANCH):
            assembly[index] = (instr[0], labels[instr[1]])
        elif instr[0] == Bytecode.LAMBDA:
            assembly[index] =(
                instr[0],
                (labels[instr[1][0]],
                 instr[1][1]))
    return assembly

if __name__ == '__main__':
    import tokenizer
    import parser_
    import compiler
    while True:
        src = input('assembler> ')
        tokens = tokenizer.tokenize(src)
        ast = parser_.parse(tokens)
        asm = compiler.compile_(ast)
        bc = assemble(asm)
        for b in bc:
            print(b)
