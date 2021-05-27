from sys import stdin
import ply.lex as lex

tokens = (
    'IDN',
    'FLOAT8',
    'FLOAT10',
    'FLOAT16',
    'INT8',
    'INT16',
    'INT10',
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
    'ENDLINE',
    'IF',
    'THEN',
    'ELSE',
    'WHILE',
    'DO'
)

def get_scanner():
    t_IDN       = r'[a-zA-Z][0-9a-zA-Z]*(?:(?:_|\.)[0-9a-zA-Z]+)?'
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
    t_ENDLINE   = r';'
    t_IF        = r'if'
    t_THEN      = r'then'
    t_ELSE      = r'else'
    t_WHILE     = r'while'
    t_DO        = r'do'

    def t_FLOAT8(t):
        r'0[0-7]+\.[0-7]+'
        parts = t.value.split('.')
        t.value = int(parts[0], 8)
        factor = 1
        for n in parts[1]:
            factor /= 8
            t.value += int(n, 8) * factor
        return t

    def t_FLOAT10(t):
        r'(?:0|[1-9]\d*)\.\d+'
        t.value = float(t.value)
        return t

    def t_FLOAT16(t):
        r'0[xX][0-9a-fA-F]+\.[0-9a-fA-F]+'
        parts = t.value.split('.')
        t.value = int(parts[0], 16)
        factor = 1
        for n in parts[1]:
            factor /= 16
            t.value += int(n, 16) * factor
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
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    return lex.lex()

if __name__ == '__main__':
    lexer = get_lexer()
    lexer.input(stdin.read())
    print(*lexer, sep='\n')
