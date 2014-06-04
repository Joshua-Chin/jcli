import collections
import enum
import re

from datatypes import sym

class Token(enum.Enum):
    left_paren = '('
    right_paren = ')'
    quote = '\''
    quasiquote = '`'
    unquote = ','

def tokenize_str(string):
    return string[1:-1].encode('utf8').decode('unicode-escape')
    
token_types = collections.OrderedDict([
    (float, r'(-|\+)?((\d+\.\d*)|(\d*\.\d+))'),
    (int, r'(-|\+)?\d+'),
    (tokenize_str, r'"(\\"|[^"])*"'),
    (lambda x: x=='#t', r'#t|#f'),
    (Token, r'[\(\)\',`]'),
    (None, r'(\s+|;.*)'),
    (sym, r'[^"\'`,\.#;\s\(\)\[\]\{\}]+'),])

def compile_(tokens):
    for token, regex in list(tokens.items()):
        tokens[token] = re.compile(regex)
compile_(token_types)

def tokenize(string, tokens=None):
    if tokens is None:
        tokens = token_types
    out = []
    index = 0
    line = 0
    while index < len(string):
        head = string[index:]
        for token, regex in list(tokens.items()):
            match = regex.match(head)
            if match:
                group = match.group()
                index += len(group)
                line += group.count('\n')
                if token is not None:
                    out.append((token(group), line))
                else:
                    out.append(None)
                break
        else:
            raise SyntaxError("Syntax Error at line %s: %s..."%(line, head[:10]))
    for a, b in zip(out, out[1:]):
        if  a is None or isinstance(a[0], Token):
            continue
        if b is None or isinstance(b[0], Token):
            continue
        raise SyntaxError("Syntax Error at line %s: %s..."%(b[1], a[0]))
    return filter(None, out)

if __name__ == '__main__':
    while True:
        print((tokenize(raw_input("tokenize> "))))
