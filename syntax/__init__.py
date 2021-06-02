# some public syntax function defined here

# General type conversion
def _conv(new_type, src, env):
    dst = env.newnode()
    dst.type = new_type
    dst.place = env.newtemp(new_type)
    dst.code = src.code + env.gen_conv(dst.place, new_type, src.place)
    return dst

# General binary operations
def _binops(d, s1, s2, env, env_gen_func_name_int, env_gen_func_name_float):
    if s1.type == 'int' and s2.type == 'int':
        d.place = env.newtemp('int')
        d.type = 'int'
        d.code = s1.code + s2.code \
            + getattr(env, env_gen_func_name_int)(d.place, s1.place, s2.place)
    else:
        if s1.type == 'int':
            s1 = _conv('float', s1, env)
        if s2.type == 'int':
            s2 = _conv('float', s2, env)
        d.place = env.newtemp('float')
        d.type = 'float'
        d.code = s1.code + s2.code \
            + getattr(env, env_gen_func_name_float)(d.place, s1.place, s2.place)
