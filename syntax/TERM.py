def multiply(t, t1, f, env):
    t.place = env.newtemp()
    t.code = t1.code + f.code \
        + env.gen_multiply(t.place, t1.place, f.place)

def divide(t, t1, f, env):
    t.place = env.newtemp()
    t.code = t1.code + f.code \
        + env.gen_divide(t.place, t1.place, f.place)
 
def factor(t, f, env):
    t.place = f.place
    t.code = f.code
