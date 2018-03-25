'''
Created on 22 de mar de 2018

@author: I844141
'''
from TokenModule import Token
import re

WHITESPACE = 'whitespace'

class Lexer(object):
    '''
    Lexical Analyzer for language C
    '''
    
    def __init__(self, text):
        self.text = text
        self.tokens = []
        self.keywords = ['void', 'float', 'int', 'if', 'while', 'return']
        token_specification = [(WHITESPACE, r'\s+'),
                               (Token.TYPE_ID, r'[A-Za-z]([A-Za-z0-9]*_?)*'),
                               (Token.TYPE_ARIT_OP, r'\+|-|\*|/'),
                               (Token.TYPE_FLOAT, r'\d+\.\d+'),
                               (Token.TYPE_NUM, r'\d+'),
                               (Token.TYPE_PAREN_L, r'\('),
                               (Token.TYPE_PAREN_R, r'\)'),
                               (Token.TYPE_COMMA, r','),
                               (Token.TYPE_SEMICOLON, r';')]
        
        self.tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    
    def evaluate(self):
        line_num = 0
        for line in text:
            for mo in re.finditer(self.tok_regex, line):
                kind = mo.lastgroup
                value = mo.group(kind)
                if (kind != WHITESPACE):
                    if (kind == Token.TYPE_ID and value in self.keywords):
                        kind = Token.TYPE_RESERVED_WORD
                    self.tokens.append(Token(kind, value, line_num, mo.start()))
            line_num += 1
    def printTokens(self):
        for t in self.tokens:
            print(t)

if __name__ == "__main__":
    text = ['6 + 1', '1.1 * 1221', 'void main1_221()']
    lexer = Lexer(text)
    lexer.evaluate()
    lexer.printTokens()
    