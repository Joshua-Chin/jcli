from tokenizer import Token
from datatypes import linked_list

__all__ = ['parse']

def parse(tokens):
    try:
        return match_exprs(tokens)
    except SystemExit:
        pass
    except KeyboardInterrupt:
        pass
    except Exception as e:
        raise

def match_exprs(tokens):
    out = []
    index = 0
    while index < len(tokens):
        match = match_expr(tokens[index:])
        try:
            out.append(match[0])
            index += match[1]
        except TypeError:
            raise SyntaxError("Syntax Error at line %s, %s..."%(tokens[index][1], tokens[index][0]))
    return out

def match_expr(tokens):
    return match_literal(tokens) or match_compound(tokens)

def match_compound(tokens):
    out = []
    index = 1
    if tokens[0][0] is not Token.left_paren:
        return
    while True:
        head = tokens[index:]
        if not head:
            raise SyntaxError("EOF while scanning for closing parens")
        if head[0][0] is Token.right_paren:
            return (linked_list(out), tokens[0][1]), index+1
        match = match_expr(head)
        if not match:
            raise SyntaxError("Syntax Error at line %s, %s..."%(head[0][1], [x[0] for x in head[:5]]))
        out.append(match[0])
        index += match[1]

def match_literal(tokens):
    if not isinstance(tokens[0][0], Token):
        return tokens[0], 1

if __name__ == '__main__':
    import tokenizer
    while True:
        print((parse(tokenizer.tokenize(raw_input('parser> ')))))
