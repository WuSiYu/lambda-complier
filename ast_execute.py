import parser
from scanner import get_scanner
from parser import get_parser, dump_ast

class TestEnv:
    def __init__(self):
        self._last_mem = -1
        self._last_flag = -1
        self._vars = {}

    def __repr__(self):
        return "vars: " + str(self._vars)

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


if __name__ == '__main__':

    while True:
        try:
            s = input('parse > ')
        except EOFError:
            break
        if not s: continue

        scanner = get_scanner()
        parser = get_parser()

        scanner.input(s)
        print(*scanner, sep='\n')

        ast = parser.parse(s)

        print("\n=== AST:")
        print(ast)
        dump_ast(ast)

        env = TestEnv()
        print("\n=== AST on TestEnv:")
        result = ast(env=env)
        print("env:", env)
        print("result:", result)
        print("[CODE]")
        for line in result.code.split('\n'):
            if ':' in line:
                print(line)
            else:
                print('\t' + line)
        # print(result.code)
