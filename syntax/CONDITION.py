def _cond_jmp(c, e1, e2, env, cond):
    c.true = env.newlabel()
    c.false = env.newlabel()
    c.code = e1.code + e2.code \
        + env.gen_if(e1.place, cond, e2.place, c.true) \
        + env.gen_goto(c.false)

def larger(c, e1, e2, env):
    _cond_jmp(c, e1, e2, env, '>')

def less(c, e1, e2, env):
    _cond_jmp(c, e1, e2, env, '<')

def equal(c, e1, e2, env):
    _cond_jmp(c, e1, e2, env, '=')
