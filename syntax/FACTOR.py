def idn(f, idn, env):
    id = env.lookup(idn)
    f.place = id.place
    f.code = ''

def integer(f, i, env):
    f.place = i
    f.code = ''
