from functools import partial
import parser
from scanner import get_scanner
from parser import get_parser, parse, dump_ast

class ThreeAddressCodeEnv:
    def __init__(self):
        self._last_mem = -1
        self._last_flag = -1
        self._vars = {}

    def newnode(self):
        class OBJ():
            def __getattr__(self, name):
                return self.__dict__[name]

            def __setattr__(self, name, value):
                self.__dict__[name] = value

            def __repr__(self):
                return self.__dict__.__repr__()
        return OBJ()

    def newlabel(self):
        self._last_flag += 1
        return 'label%d' % self._last_flag

    def newtemp(self, type_):
        self._last_mem += 1
        return '#%s%d' % (type_, self._last_mem)

    def newvar(self, idn, type_):
        var = self.newnode()
        self._last_mem += 1
        var.type = type_
        var.place = '#%s%d_%s' % (type_, self._last_mem, idn)
        self._vars[idn] = var
        return var

    def lookup(self, idn):
        return self._vars.get(idn)

    def gen_nothing(self):
        return ""

    def gen_assign(self, n1, n2):
        return '%s <- %s\n' % (n1, n2)

    def gen_conv(self, n1, n2, n3, n4):
        return '%s <- conv_%s_to_%s(%s)\n' % (n1, n4, n2, n3)

    def gen_plus(self, n1, n2, n3):
        return '%s <- %s + %s\n' % (n1, n2, n3)

    def gen_fplus(self, n1, n2, n3):
        return '%s <- %s +. %s\n' % (n1, n2, n3)

    def gen_minus(self, n1, n2, n3):
        return '%s <- %s - %s\n' % (n1, n2, n3)

    def gen_fminus(self, n1, n2, n3):
        return '%s <- %s -. %s\n' % (n1, n2, n3)

    def gen_multiply(self, n1, n2, n3):
        return '%s <- %s * %s\n' % (n1, n2, n3)

    def gen_fmultiply(self, n1, n2, n3):
        return '%s <- %s *. %s\n' % (n1, n2, n3)

    def gen_divide(self, n1, n2, n3):
        return '%s <- %s / %s\n' % (n1, n2, n3)

    def gen_fdivide(self, n1, n2, n3):
        return '%s <- %s /. %s\n' % (n1, n2, n3)

    def gen_if(self, n1, n2, n3, n4):
        return 'if %s %s %s, jump to %s\n' % (n1, n2, n3, n4)

    def gen_fif(self, n1, n2, n3, n4):  # float cmp if
        return 'if %s %s. %s, jump to %s\n' % (n1, n2, n3, n4)

    def gen_goto(self, n1):
        return 'jump to %s\n' % n1

    def gen_label(self, n1):
        return n1 + ':\n'


class InterpreterEnv_Var():
    def __init__(self, type_):
        self.val = None
        self.type = type_
        self.place = self

    def __repr__(self):
        return repr(self.val)

class InterpreterEnv_Obj():
    def __getattr__(self, name):
        return self.__dict__[name]

    def __setattr__(self, name, value):
        self.__dict__[name] = value

    def __repr__(self):
        return self.__dict__.__repr__()

class InterpreterEnv:
    def __init__(self):
        self._exec = []
        self._mem = []
        self._vars = {}
        self._labels = {}
        self._pc = 0

    def newnode(self):
        return InterpreterEnv_Obj()

    def newlabel(self):
        l = object()
        self._labels[l] = None
        return l

    def newtemp(self, type_):
        var = InterpreterEnv_Var(type_)
        self._mem.append(var)
        return var

    def newvar(self, idn, type_):
        var = self.newtemp(type_)
        self._vars[idn] = var
        return var

    def lookup(self, idn):
        return self._vars.get(idn)

    def _get(self, v):
        if hasattr(v, 'val'):
            return v.val
        else :
            return v

    def gen_nothing(self):
        return tuple()

    def _assign(self, n1, n2):
        n1.val = self._get(n2)
    def gen_assign(self, *args):
        return (partial(self._assign, *args), )

    def _conv(self, n1, n2, n3, n4):
        if n2 == 'int':
            n1.val = int(self._get(n3))
        if n2 == 'float':
            n1.val = float(self._get(n3))
        else:
            raise NotImplementedError("gen_conv(): int <-> float only, not %s -> %s" % (n4, n2))
    def gen_conv(self, *args):
        return (partial(self._conv, *args), )

    def _plus(self, n1, n2, n3):
        n1.val = self._get(n2) + self._get(n3)
    def gen_plus(self, *args):
        return (partial(self._plus, *args), )

    gen_fplus = gen_plus

    def _minus(self, n1, n2, n3):
        n1.val = self._get(n2) - self._get(n3)
    def gen_minus(self, *args):
        return (partial(self._minus, *args), )

    gen_fminus = gen_minus

    def _multiply(self, n1, n2, n3):
        n1.val = self._get(n2) * self._get(n3)
    def gen_multiply(self, *args):
        return (partial(self._multiply, *args), )

    gen_fmultiply = gen_multiply

    def _divide(self, n1, n2, n3):
        n1.val = self._get(n2) // self._get(n3)
    def gen_divide(self, *args):
        return (partial(self._divide, *args), )

    def _fdivide(self, n1, n2, n3):
        n1.val = self._get(n2) / self._get(n3)
    def gen_fdivide(self, *args):
        return (partial(self._fdivide, *args), )

    def _cmp(self, n1, n2, n3):
        if n2 == '>':
            return self._get(n1) > self._get(n3)
        if n2 == '=':
            return self._get(n1) == self._get(n3)
        if n2 == '<':
            return self._get(n1) < self._get(n3)

    def _if(self, n1, n2, n3, n4):
        if self._cmp(n1, n2, n3):
            self._pc = self._labels[n4] - 1
    def gen_if(self, *args):
        return (partial(self._if, *args), )

    gen_fif = gen_if

    def _goto(self, n1):
        self._pc = self._labels[n1] - 1
    def gen_goto(self, *args):
        return (partial(self._goto, *args), )

    def gen_label(self, n1):
        return (n1, )
    
    def receive(self, ast_result):
        for x in ast_result.code:
            if callable(x):
                self._exec.append(x)
            else:
                self._labels[x] = len(self._exec)

    def exec(self):
        print('running...')
        cycle = 0
        try:
            while self._pc < len(self._exec):
                cycle += 1
                self._exec[self._pc]()
                self._pc += 1
        except (Exception, KeyboardInterrupt) as e:
            print("ERROR: exec() stoped:", e.__class__.__name__, e)
            print("cycle:", cycle, "pc:", self._pc)
            print(self._vars)
            return

        print('done, cycle:', cycle)
        print(self._vars)


if __name__ == '__main__':

    interpreter = InterpreterEnv()

    while True:
        try:
            s = input('parse > ')
        except EOFError:
            break
        if not s: continue

        scanner = get_scanner()
        parser = get_parser()

        ast = parse(scanner, parser, s)
        if not ast:
            print("error or empty ast, abort")
            continue

        print("\n=== AST:")
        dump_ast(ast)

        print("\n=== AST on TestEnv:")
        try:
            env = ThreeAddressCodeEnv()
            result = ast(env=env)
            print("env:", env._vars)
            print("\n[CODE]")
            for line in result.code.split('\n'):
                if ':' in line:
                    print(line)
                else:
                    print('\t' + line)
        except Exception as e:
            print("ThreeAddressCodeEnv failed, code may incomplete:")
            print("ERROR:", e)

        print("\n=== AST on InterpreterEnv:")
        try:
            interpreter.receive(ast(env=interpreter))
            interpreter.exec()
        except Exception as e:
            print("InterpreterEnv failed:")
            print("ERROR:", e)
