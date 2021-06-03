from . import _conv

def _cond_jmp(c, e1, e2, env, cond):
    c.true = env.newlabel()
    c.false = env.newlabel()

    if e1.type == 'int' and e2.type == 'int':
        c.code = e1.code + e2.code \
            + env.gen_if(e1.place, cond, e2.place, c.true) \
            + env.gen_goto(c.false)
    else:
        if e1.type == 'int':
            e1 = _conv('float', e1, env)
        if e2.type == 'int':
            e2 = _conv('float', e2, env)
        c.code = e1.code + e2.code \
            + env.gen_fif(e1.place, cond, e2.place, c.true) \
            + env.gen_goto(c.false)

def larger(c, e1, e2, env):
    _cond_jmp(c, e1, e2, env, '>')

def less(c, e1, e2, env):
    _cond_jmp(c, e1, e2, env, '<')

def equal(c, e1, e2, env):
    _cond_jmp(c, e1, e2, env, '=')
