def idn(f, idn, env):
    id = env.lookup(idn)
    f.place = id.place
    f.code = env.gen_nothing()

def integer(f, v, env):
    f.place = v
    f.type = 'int'
    f.code = env.gen_nothing()

def float(f, v, env):
    f.place = v
    f.type = 'float'
    f.code = env.gen_nothing()

def expression(f, e, env):
    f.place = e.place
    f.code = e.code
