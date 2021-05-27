def idn(f, idn, env):
    id = env.lookup(idn)
    f.place = id.place
    f.code = ''

def integer(f, i, env):
    f.place = i
    f.code = ''

def expression(f, e, env):
    f.place = e.place
    f.code = e.code
