from sys import stdin
from typing import Tuple
import ply.lex as lex

reserved = {
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'while': 'WHILE',
    'do': 'DO'
}

tokens = (
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'LESS',
    'LARGER',
    'EQUAL',
    'LPAREN',
    'RPAREN',
    'LBLOCK',
    'RBLOCK',
    'SEMICOLON',
    'IDN',
    'FLOAT8',
    'FLOAT10',
    'FLOAT16',
    'INT8',
    'INT16',
    'INT10'
) + tuple(reserved.values())

def get_scanner() -> Tuple[lex.Lexer, list]:
    t_PLUS      = r'\+'
    t_MINUS     = r'-'
    t_MULTIPLY  = r'\*'
    t_DIVIDE    = r'/'
    t_LESS      = r'\<'
    t_LARGER    = r'\>'
    t_EQUAL     = r'='
    t_LPAREN    = r'\('
    t_RPAREN    = r'\)'
    t_LBLOCK    = r'\{'
    t_RBLOCK    = r'\}'
    t_SEMICOLON = r';'

    def _str_to_real(s, base):
        parts = s.split('.')
        num = int(parts[0], base)
        factor = 1
        for n in parts[1]:
            factor /= base
            num += int(n, base) * factor
        return num
    
    def t_IDN(t):
        r'[a-zA-Z][0-9a-zA-Z]*(?:(?:_|\.)[0-9a-zA-Z]+)?'
        t.type = reserved.get(t.value, 'IDN')
        return t

    def t_FLOAT8(t):
        r'0[0-7]+\.[0-7]+'
        t.value = _str_to_real(t.value, 8)
        return t

    def t_FLOAT10(t):
        r'(?:0|[1-9]\d*)\.\d+'
        t.value = float(t.value)
        return t

    def t_FLOAT16(t):
        r'0[xX][0-9a-fA-F]+\.[0-9a-fA-F]+'
        t.value = _str_to_real(t.value, 16)
        return t

    def t_INT8(t):
        r'0[0-7]+'
        t.value = int(t.value, 8)
        return t

    def t_INT16(t):
        r'0[xX][0-9a-fA-F]+'
        t.value = int(t.value, 16)
        return t

    def t_INT10(t):
        r'(?:0|[1-9]\d*)'
        t.value = int(t.value)
        return t

    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    t_ignore = ' \t'

    def t_error(t):
        error_list.append((t.lineno, t.value[0]))
        t.lexer.skip(1)

    error_list = []
    return lex.lex(), error_list

if __name__ == '__main__':
    lexer, error_list = get_scanner()
    lexer.input(stdin.read())
    
    outputs = ["%s %s\t (line=%d, offset=%d)" % (x.type.ljust(10), x.value, x.lineno, x.lexpos) for x in lexer]
    if error_list:
        print(*('ERROR: line %d: Illegal character \'%s\'' % x for x in error_list), sep='\n')
    print(*outputs, sep='\n')
