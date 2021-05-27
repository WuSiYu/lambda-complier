import parser
from scanner import get_scanner
from parser import get_parser


class TestEnv:
    def __init__(self):
        self._last_mem = -1
        self._last_code = -1
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
        return 'newlabel()'
    
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
        return '(%s <- %s)' % (n1, n2)

    def gen_plus(self, n1, n2, n3):
        return '(%s <- %s + %s)' % (n1, n2, n3)

    def gen_minus(self, n1, n2, n3):
        return '(%s <- %s - %s)' % (n1, n2, n3)

    def gen_multiply(self, n1, n2, n3):
        return '(%s <- %s * %s)' % (n1, n2, n3)

    def gen_divide(self, n1, n2, n3):
        return '(%s <- %s / %s)' % (n1, n2, n3)


if __name__ == '__main__':

    while True:
        try:
            s = input('parse > ')
        except EOFError:
            break
        if not s: continue

        scanner = get_scanner()
        parser = get_parser()
        ast = parser.parse(s)

        print("\n=== AST:")
        print(ast)

        env = TestEnv()
        print("\n=== AST on TestEnv:")
        result = ast(env=env)
        print("env:", env)
        print("result:", result)
