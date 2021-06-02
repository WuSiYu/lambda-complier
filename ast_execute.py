import parser
from scanner import get_scanner
from parser import get_parser, dump_ast

class TestEnv:
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

    def newtemp(self):
        self._last_mem += 1
        return '#%d' % self._last_mem

    def newvar(self, idn):
        var = self.newnode()
        self._last_mem += 1
        var.place = '#%d' % self._last_mem
        self._vars[idn] = var
        return var

    def lookup(self, idn):
        return self._vars.get(idn)

    def gen_nothing(self):
        return ""

    def gen_assign(self, n1, n2):
        return '%s <- %s\n' % (n1, n2)

    def gen_plus(self, n1, n2, n3):
        return '%s <- %s + %s\n' % (n1, n2, n3)

    def gen_minus(self, n1, n2, n3):
        return '%s <- %s - %s\n' % (n1, n2, n3)

    def gen_multiply(self, n1, n2, n3):
        return '%s <- %s * %s\n' % (n1, n2, n3)

    def gen_divide(self, n1, n2, n3):
        return '%s <- %s / %s\n' % (n1, n2, n3)

    def gen_if(self, n1, n2, n3, n4):
        return 'if %s %s %s, jump to %s\n' % (n1, n2, n3, n4)

    def gen_goto(self, n1):
        return 'jump to %s\n' % n1

    def gen_label(self, n1):
        return n1 + ':\n'

class InterpreterEnv:
    def __init__(self):
        self._exec = []
        self._mem = []
        self._vars = {}
        self._labels = {}
        self._pc = 0

    def newnode(self):
        class Obj():
            def __getattr__(self, name):
                return self.__dict__[name]

            def __setattr__(self, name, value):
                self.__dict__[name] = value

            def __repr__(self):
                return self.__dict__.__repr__()
        return Obj()

    def newlabel(self):
        l = object()
        self._labels[l] = None
        return l

    def newtemp(self):
        class Var():
            def __init__(self):
                self.val = None
                self.place = self

            def __repr__(self):
                return repr(self.val)
        var = Var()
        self._mem.append(var)
        return var

    def newvar(self, idn):
        var = self.newtemp()
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

    def gen_assign(self, n1, n2):
        def f():
            n1.val = self._get(n2)
        return (f, )

    def gen_plus(self, n1, n2, n3):
        def f():
            n1.val = self._get(n2) + self._get(n3)
        return (f, )

    def gen_minus(self, n1, n2, n3):
        def f():
            n1.val = self._get(n2) - self._get(n3)
        return (f, )

    def gen_multiply(self, n1, n2, n3):
        def f():
            n1.val = self._get(n2) * self._get(n3)
        return (f, )

    def gen_divide(self, n1, n2, n3):
        def f():
            n1.val = self._get(n2) / self._get(n3)
        return (f, )

    def _cmp(self, n1, n2, n3):
        if n2 == '>':
            return self._get(n1) > self._get(n3)
        if n2 == '=':
            return self._get(n1) == self._get(n3)
        if n2 == '<':
            return self._get(n1) < self._get(n3)

    def gen_if(self, n1, n2, n3, n4):
        def f():
            if self._cmp(n1, n2, n3):
                self._pc = self._labels[n4] - 1
        return (f, )

    def gen_goto(self, n1):
        def f():
            self._pc = self._labels[n1] - 1
        return (f, )

    def gen_label(self, n1):
        return (n1, )
    
    def receive(self, ast_result):
        for x in ast_result:
            if callable(x):
                self._exec.append(x)
            else:
                self._labels[x] = len(self._exec)

    def exec(self):
        print('running...')
        cycle = 0
        while self._pc < len(self._exec):
            cycle += 1
            self._exec[self._pc]()
            self._pc += 1
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

        # scanner.input(s)
        # print(*scanner, sep='\n')

        ast = parser.parse(s)

        print("\n=== AST:")
        print("# print(ast):")
        print(ast)
        print("\n# dump_ast(ast):")
        dump_ast(ast)

        print("\n=== AST on TestEnv:")
        try:
            env = TestEnv()
            result = ast(env=env)
            print("env:", env._vars)
            print("result:", result)
            print("\n[CODE]")
            for line in result.code.split('\n'):
                if ':' in line:
                    print(line)
                else:
                    print('\t' + line)
        except Exception as e:
            print("TestEnv failed, code may incomplete:", e)

        print("\n=== AST on InterpreterEnv:")
        interpreter.receive(ast(env=interpreter).code)
        interpreter.exec()
