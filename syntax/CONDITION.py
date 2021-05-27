def larger(c, e1, e2, env):
    c.true = env.newlabel()
    c.false = env.newlabel()
    c.code = e1.code + e2.code \
        + env.gen_if(e1.place, '>', e2.place, c.true) \
        + env.gen_goto(c.false)

def less(c, e1, e2, env):
    c.true = env.newlabel()
    c.false = env.newlabel()
    c.code = e1.code + e2.code \
        + env.gen_if(e1.place, '<', e2.place, c.true) \
        + env.gen_goto(c.false)

def equal(c, e1, e2, env):
    c.true = env.newlabel()
    c.false = env.newlabel()
    c.code = e1.code + e2.code \
        + env.gen_if(e1.place, '=', e2.place, c.true) \
        + env.gen_goto(c.false)
