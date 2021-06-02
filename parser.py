from functools import partial
from ply.lex import Lexer
import ply.yacc as yacc

from scanner import tokens
from syntax import CONDITION, FACTOR, PROGRAM, LINE, SENTENCE, EXPRESSION, TERM

def dump_ast(lambda_node, depth=0):
    if isinstance(lambda_node, partial):
        func = lambda_node.args[0]
        args = lambda_node.args[1:]
        print('    '*depth, "+", func.__module__.split('.')[1] + ' <- ' + func.__name__ + '()')
        for arg in args:
            dump_ast(arg, depth+1)
    else:
        print('    '*depth, "-", repr(lambda_node))

def get_parser():
    def F(func, *args):
        def wrapper(func, *args, env):
            node = env.newnode()
            func(node, *(x(env=env) if callable(x) else x for x in args), env)
            return node
        return partial(wrapper, func, *args)

    def p_PROGRAM_line(p):
        'P : L'
        p[0] = F(PROGRAM.line, p[1])

    def p_PROGRAM_line_program(p):
        'P : L P'
        p[0] = F(PROGRAM.line_program, p[1], p[2])

    def p_LINE_sentence(p):
        'L : S ENDLINE'
        p[0] = F(LINE.sentence, p[1])

    def p_SENTENCE_assign(p):
        'S : IDN EQUAL E'
        p[0] = F(SENTENCE.assign, p[1], p[3])

    def p_SENTENCE_if_then(p):
        'S : IF C THEN S'
        p[0] = F(SENTENCE.if_then, p[2], p[4])

    def p_SENTENCE_if_then_else(p):
        'S : IF C THEN S ELSE S'
        p[0] = F(SENTENCE.if_then_else, p[2], p[4], p[6])

    def p_SENTENCE_while_do(p):
        'S : WHILE C DO S'
        p[0] = F(SENTENCE.while_do, p[2], p[4])

    def p_SENTENCE_codeblock(p):
        'S : LBLOCK P RBLOCK'
        p[0] = F(SENTENCE.codeblock, p[2])

    def p_CONDITION_larger(p):
        'C : E LARGER E'
        p[0] = F(CONDITION.larger, p[1], p[3])

    def p_CONDITION_less(p):
        'C : E LESS E'
        p[0] = F(CONDITION.less, p[1], p[3])

    def p_CONDITION_equal(p):
        'C : E EQUAL E'
        p[0] = F(CONDITION.equal, p[1], p[3])

    def p_EXPRESSION_plus(p):
        'E : E PLUS T'
        p[0] = F(EXPRESSION.plus, p[1], p[3])

    def p_EXPRESSION_minus(p):
        'E : E MINUS T'
        p[0] = F(EXPRESSION.minus, p[1], p[3])

    def p_EXPRESSION_term(p):
        'E : T'
        p[0] = F(EXPRESSION.term, p[1])

    def p_TERM_multiply(p):
        'T : T MULTIPLY F'
        p[0] = F(TERM.multiply, p[1], p[3])

    def p_TERM_divide(p):
        'T : T DIVIDE F'
        p[0] = F(TERM.divide, p[1], p[3])

    def p_TERM_factor(p):
        'T : F'
        p[0] = F(TERM.factor, p[1])

    def p_FACTOR_idn(p):
        'F : IDN'
        p[0] = F(FACTOR.idn, p[1])

    def p_FACTOR_int(p):
        '''F : INT8
            | INT10
            | INT16'''
        p[0] = F(FACTOR.integer, p[1])

    def p_FACTOR_float(p):
        '''F : FLOAT8
            | FLOAT10
            | FLOAT16'''
        p[0] = F(FACTOR.float, p[1])

    def p_FACTOR_expression(p):
        'F : LPAREN E RPAREN'
        p[0] = F(FACTOR.expression, p[2])

    def p_error(p):
        if p:
            print("ERROR: syntax error at token: %s" % p)
            parser.errok()
        else:
            raise ValueError("ERROR: unexcepted EOF")

    parser = yacc.yacc(debug=1)
    return parser
