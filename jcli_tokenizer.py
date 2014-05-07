import collections
import functools

import jcli_tokens

token = collections.namedtuple(
    'token', ['name', 'string', 'line_no', 'char_no'])


def strict_generator(generator):
    @functools.wraps(generator)
    def wrapper(*args, **kwargs):
        return list(generator(*args, **kwargs))
    return wrapper

@strict_generator
def tokenize(string, token_types=None, ignore_types=None):

    if token_types is None:
        token_types = jcli_tokens.tokens
    if ignore_types is None:
        ignore_types = jcli_tokens.ignore

    line_no = 0
    char_no = 0

    while char_no < len(string):
        chars = string[char_no:]
        for name, regex in token_types.items():
            match = regex.match(chars)
            if match is not None:
                group = match.group()
                if name not in ignore_types:
                    yield token(name, group, line_no, char_no)
                    
                line_no += group.count('\n')
                char_no += len(group)
                
                break
        else:
            raise TokenizerError(chars, line_no, char_no)

class TokenizerError(Exception):

    def __init__(self, string, line_no, char_no):
        self.string = string
        self.line_no = line_no
        self.char_no = char_no

    def __str__(self):
        return ("Syntax error at line %s, char %s: %s..."
                %(self.line_no, self.char_no, self.string[:10]))
        
    

if __name__ == '__main__':
    print(tokenize('(print Hello World")'))
