def assign(s, idn, e, env):
    id = env.lookup(idn)
    if not id:
        id = env.newvar(idn)
    s.code = e.code + env.gen_assign(id.place, e.place)

def if_then(s, c, s1, env):
    s.code = c.code + env.gen_label(c.true) + s1.code + env.gen_label(c.false)

def if_then_else(s, c, s1, s2, env):
    s.next = env.newlabel()
    s.code = c.code \
        + env.gen_label(c.true)+ s1.code + env.gen_goto(s.next) \
        + env.gen_label(c.false) + s2.code + env.gen_label(s.next)

def while_do(s, c, s1, env):
    s.begin = env.newlabel()
    s.code = env.gen_label(s.begin) + c.code \
        + env.gen_label(c.true) + s1.code + env.gen_goto(s.begin) \
        + env.gen_label(c.false)

def codeblock(s, p, env):
    s.code = p.code

