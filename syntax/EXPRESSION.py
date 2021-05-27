def plus(e, e1, t, env):
    e.place = env.newtemp()
    e.code = e1.code + t.code \
        + env.gen_plus(e.place, e1.place, t.place)

def minus(e, e1, t, env):
    e.place = env.newtemp()
    e.code = e1.code + t.code \
        + env.gen_minus(e.place, e1.place, t.place)

def term(e, t, env):
    e.place = t.place
    e.code = t.code
