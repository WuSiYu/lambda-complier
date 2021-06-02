from . import _binops

def multiply(d, s1, s2, env):
    _binops(d, s1, s2, env, 'gen_multiply', 'gen_fmultiply')

def divide(d, s1, s2, env):
    _binops(d, s1, s2, env, 'gen_divide', 'gen_fdivide')

def factor(t, f, env):
    t.place = f.place
    t.type = f.type
    t.code = f.code
