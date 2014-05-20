from tokenizer import Token
from datatypes import linked_list

__all__ = ['parse']

def parse(tokens):
    try:
        return match_exprs(tokens)
    except Exception as e:
        raise ParserException(e)

def match_exprs(tokens):
    out = []
    index = 0
    while index < len(tokens):
        match = match_expr(tokens[index:])
        if match is None:
            raise AssertionError(tokens[index:])
        out.append(match[0])
        index += match[1]
    return out

def match_expr(tokens):
    return match_literal(tokens) or match_compound(tokens)

def match_compound(tokens):
    out = []
    index = 1
    if tokens[0] is not Token.left_paren:
        return
    while True:
        head = tokens[index:]
        if not head:
            raise AssertionError(head)
        if head[0] is Token.right_paren:
            return linked_list(out), index+1
        
        match = match_expr(head)
        if not match:
            raise AssertionError(head)
        out.append(match[0])
        index += match[1]

def match_literal(tokens):
    if not isinstance(tokens[0], Token):
        return tokens[0], 1

class ParserException(Exception): pass

if __name__ == '__main__':
    import tokenizer
    while True:
        print((parse(tokenizer.tokenize(eval(input('parser> '))))))
