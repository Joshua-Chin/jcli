import enum

class Bytecode(enum.Enum):
    REF = 0
    DEF = 1
    POP = 2
    PUSH = 3
    BRANCH = 4
    LABEL = 5
    GOTO = 6
    LAMBDA = 7
    CALL = 8
    RETURN = 9

class label(object): pass
