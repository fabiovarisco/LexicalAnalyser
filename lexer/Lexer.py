'''
@author: FABIO VARISCO, GABRIEL RECH
'''
from TokenModule import Token
import re

WHITESPACE = 'whitespace'
BEGIN_COMMENT_BLOCK = 'BEGIN_COMMENT_BLOCK'
END_COMMENT_BLOCK = 'END_COMMENT_BLOCK'
COMMENT_LINE = 'COMMENT_LINE'

class SyntaxErr(Exception):
    def __init__(self, line, col, value):
        self.line = line
        self.col = col
        self.value = value
        
    def __str__(self):
        return repr('Incorrect syntax detected at: Line: {}; Column: {}; Value: {}.'.format(self.line, self.col, self.value))

class Lexer(object):
    '''
    Lexical Analyzer for language C
    '''
    
    def __init__(self, text):
        self.text = text
        self.tokens = []
        self.keywords = ['void', 'return', '#include',
                         'float', 'int', 'double', 'string', 'bool'
                         'if', 'else', 'do', 'while', 'switch', 'case', 'break', 'for']

        token_specification = [(WHITESPACE, r'\s+'),
                               (Token.TYPE_STRING_LITERAL, r'".*"'),
                               (Token.TYPE_ID, r'[A-Za-z][A-Za-z0-9_]*'),
                               (BEGIN_COMMENT_BLOCK, r'\/\*'),
                               (END_COMMENT_BLOCK, r'\*\/'),
                               (COMMENT_LINE, r'\/\/.*'),
                               (Token.TYPE_ARIT_OP, r'\+|-|\*|/'),
                               #(Token.TYPE_FLOAT, r'\d+\.\d+'),
                               (Token.TYPE_NUM, r'\d+(\.\d+)?'),
                               (Token.TYPE_PAREN_L, r'\('),
                               (Token.TYPE_PAREN_R, r'\)'),
                               (Token.TYPE_BRACKET_L, r'\{'),
                               (Token.TYPE_BRACKET_R, r'\}'),
                               (Token.TYPE_SQ_BRACKET_L, r'\['),
                               (Token.TYPE_SQ_BRACKET_R, r'\]'),
                               (Token.TYPE_EQUAL, r'='),
                               (Token.TYPE_COMMA, r','),
                               (Token.TYPE_SEMICOLON, r';'),
                               (Token.TYPE_RELATIONAL_OP, r'<|<=|==|!=|>=|>'),
                               (Token.TYPE_LOGICAL_OP, r'\|\||&&'),
                               (Token.TYPE_INCLUDE, r'((?i)\#include).*'),
                               (Token.TYPE_POINTER_IDENTIFIER, r'(\*+)|&')
                               ]
        
        self.tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    
    def evaluate(self):
        line_num = 0
        is_comment = False
        for line in text:
            last_col = 0
            for mo in re.finditer(self.tok_regex, line):
                
                if (not is_comment and mo.start() - last_col > 0):
                    raise SyntaxErr(line_num + 1, last_col, line[last_col:mo.start()])
                last_col = mo.end()
                kind = mo.lastgroup
                value = mo.group(kind)
                if (kind == BEGIN_COMMENT_BLOCK):
                    is_comment = True
                if (kind != WHITESPACE and is_comment == False and kind != COMMENT_LINE):
                    if (kind == Token.TYPE_ID and value in self.keywords):
                        kind = Token.TYPE_RESERVED_WORD
                    self.tokens.append(Token(kind, value, line_num, mo.start()))
                if (kind == END_COMMENT_BLOCK):
                    is_comment = False
            line_num += 1
    def printTokens(self):
        for t in self.tokens:
            print(t)

if __name__ == "__main__":
    with open('entrada.txt','r') as f:
        text = f.readlines()
        text = [l.strip() for l in text]
        
    lexer = Lexer(text)
    lexer.evaluate()
    lexer.printTokens()
    