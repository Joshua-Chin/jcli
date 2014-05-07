import collections
import tokenizer

from datatypes import linked_list, sym, quote

syntax = collections.namedtuple(
    'syntax', ['value', 'line_no', 'char_no'])

def parse(string):
    return parse_tokens(tokenizer.tokenize(string))

def parse_tokens(tokens):
    match = match_exprs(tokens)
    if match is not None:
        return match[0]

def match_exprs(tokens):
    index = 0
    out = []
    while index < len(tokens):
        match = match_expr(tokens[index:])
        if match is None:
            raise ParserError(tokens[index])
        out.append(match[0])
        index += match[1]
    return out, index
            

def match_expr(tokens):
    out = (match_compound(tokens) or
     match_quote(tokens) or
     match_literal(tokens))
    return out

def match_compound(tokens):
    if len(tokens) <= 1:
        return None
    if tokens[0].name != 'LPAREN':
        return None
    output = []
    index = 1
    while index < len(tokens) - 1:
        match = match_expr(tokens[index:])
        if match is None:
            break
        output.append(match[0])
        index += match[1]
    if tokens[index].name != 'RPAREN':
        return None
    output = linked_list(output)
    return syntax(output,
                  tokens[0].line_no,
                  tokens[0].char_no), index + 1
    
def match_quote(tokens):
    if len(tokens) <= 2:
        return None
    if tokens[0].name != 'QUOTE':
        return None
    match = match_expr(tokens[1:])
    if match is not None:
        return quote(match[0]), match[1] + 1

def match_literal(tokens):
    if len(tokens) == 0:
        return None
    token = tokens[0]
    name = token.name
    string = token.string
    value = None
    if name == 'INTEGER':
        value = int(string)
    if name == 'FLOAT':
        value = float(string)
    if name == 'BOOL':
        value = bool(string)
    if name == 'STRING':
        value = str(string)
    if name == 'ID':
        value = sym(string)
    if value is not None:
        return syntax(value, token.line_no, token.char_no), 1

class ParserError(Exception):

    def __init__(self, token):
        self.token = token

    def __str__(self):
        t = self.token
        return ("Syntax error at line %s, char %s: %s"%(
            t.line_no, t.char_no, t.string))
    
if __name__ == '__main__':
    import tokenizer
    tokens = tokenizer.tokenize("'()")
    print(parse_tokens(tokens))
