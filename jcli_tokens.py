import collections
import re

tokens = collections.OrderedDict([
('LPAREN', '\('),
('RPAREN', '\)'),
('QUOTE', '\''),
('NEWLINE', '\n'),
('COMMENT', ';.*'),
('WHITESPACE', '\s+'),
('INTEGER', '-?[0-9]+'),
('FLOAT', '-?[0-9]+(\.[0-9]*)?'),
('ID', r'[^ {}()\[\]#;"\'\s]+'),
('STRING', r'(?:"(?:[^"\n\r\\]|(?:"")|(?:\\x[0-9a-fA-F]+)|(?:\\.))*")'),])
#Copied from Java

for key, regex in tokens.items():
        tokens[key] = re.compile(regex)

ignore = {'NEWLINE', 'COMMENT', 'WHITESPACE'}
