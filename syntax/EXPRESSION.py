from . import _binops

def plus(d, s1, s2, env):
    _binops(d, s1, s2, env, 'gen_plus', 'gen_fplus')

def minus(d, s1, s2, env):
    _binops(d, s1, s2, env, 'gen_minus', 'gen_fminus')

def term(e, t, env):
    e.place = t.place
    e.type = t.type
    e.code = t.code
