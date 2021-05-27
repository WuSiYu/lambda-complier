def line(p, l, env):
    p.code = l.code

def line_program(p1, l, p2, env):
    p1.code = l.code + p2.code
