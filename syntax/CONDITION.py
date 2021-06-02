def _cond_jmp(cond):
    def ops(c, e1, e2, env):
        c.true = env.newlabel()
        c.false = env.newlabel()
        c.code = e1.code + e2.code \
            + env.gen_if(e1.place, cond, e2.place, c.true) \
            + env.gen_goto(c.false)
    return ops

larger = _cond_jmp('>')
less = _cond_jmp('<')
equal = _cond_jmp('=')
