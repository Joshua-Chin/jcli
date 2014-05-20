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
    (int, r'(-|\+)?\d+'),
    (float, r'(-|\+)?\d+\.\d+'),
    (tokenize_str, r'"(\\"|[^"])*"'),
    (lambda x: x=='#t', r'#t|#f'),
    (Token, r'[\(\)\',`]'),
    (None, r'(\s+|;.*)'),
    (sym, r'[^"\'`,\.#;\s\(\)\[\]\{\}]*'),])

def compile_(tokens):
    for token, regex in tokens.items():
        tokens[token] = re.compile(regex)
compile_(token_types)

def tokenize(string, tokens=None):
    if tokens is None:
        tokens = token_types
    out = []
    index = 0
    while index < len(string):
        head = string[index:]
        for token, regex in tokens.items():
            match = regex.match(head)
            if match:
                group = match.group()
                index += len(group)
                if token is not None:
                    out.append(token(group))
                break
        else:
            raise AssertionError(head)
    return out

if __name__ == '__main__':
    while True:
        print(tokenize(input("tokenize> ")))
