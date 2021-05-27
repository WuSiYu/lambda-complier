def assign(s, idn, e, env):
    id = env.lookup(idn)
    if not id:
        id = env.newvar(idn)
    s.code = e.code + env.gen_assign(id.place, e.place)

def if_then(s, c, s1, env):
    c.true = env.newlabel()
    c.false = s.next
    s1.next = s.next
    s.code = c.code + env.gen_label(c.true) + s1.code

def if_then_else(s, c, s1, s2, env):
    c.true = env.newlabel()
    c.false = env.newlabel()
    s1.next = s.next
    s2.next = s.next
    s.code = c.code \
        + env.gen_label(c.true)+ s1.code + env.gen_goto(s.next) \
        + env.gen_label(c.false) + s2.code

def while_do(s, c, s1, env):
    s.begin = env.newlabel()
    c.true = env.newlabel()
    c.false = s.next
    s1.next = s.begin
    s.code = env.gen_label(s.begin) + c.code \
        + env.gen_label(c.true) + s1.code + env.gen_goto(s.begin)

def codeblock(s, p):
    s.code = p.code

