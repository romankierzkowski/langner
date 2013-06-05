import unittest
from parser import parser

class SyntaxTests(unittest.TestCase):

    def testBasic(self):
        self.check('(x.a)->(new y);(x.a)->(new y);')

    def testBinary(self):
        self.check('(x || x.a)->(new y);')
        self.check('(x && x.a)->(new y);')
        self.check('(!x, !!x)->(new y);')
        self.check('(x && y || z && u)->(new y);')        

    def testComparison(self):
        self.check('(x < y)->(new y);')
        self.check('(x <= y)->(new y);')
        self.check('(x == y)->(new y);')
        self.check('(x != y)->(new y);')
        self.check('(x > y)->(new y);')
        self.check('(x >= y)->(new y);')

    def testBit(self):
        self.check('(x | x == x)->(new y);')
        self.check('(x ^ x == x)->(new y);')
        self.check('(x & x == x)->(new y);')
        self.check('(x << y == x)->(new y);')
        self.check('(x >> y == x)->(new y);')
        self.check('(~x)->(new y);')

    def testArithm(self):
        self.check('(x + y)->(new y);')
        self.check('(x - y)->(new y);')
        self.check('(x * y)->(new y);')
        self.check('(x / y)->(new y);')
        self.check('(x % y)->(new y);')
        self.check('(x // y)->(new y);')
        self.check('(x + +y)->(new y);')
        self.check('(x + -y)->(new y);')
        self.check('(x ** -y ** +-z)->(new y);')

    def testAtoms(self):
        self.check('(False)->(new y);')
        self.check('(True)->(new y);')
        self.check('(1.0)->(new y);')
        self.check('(1)->(new y);')
        self.check('("ab\\n\\tc")->(new y);')
        self.check('(x + (-y))->(new y);')

    def testFunction(self):
        self.check('(a())->(new y);')
        self.check('(a(1.0, 1, a.x, "abc"))->(new y);')

    def testEvents(self):
        self.check('(#a())->(new y);')
        self.check('(#a(x, y, z))->(new y);')

    def testActions(self):
        self.check('(x)->(x.a = x + y);')
        self.check('(x)->(new y, y.a = x + y, b(x + y, x.a, x == b));')
    
    def check(self, code):
        parsed = parser.parse(code)
        self.assertEqual(code, str(parsed))

def main():
    unittest.main()

if __name__ == '__main__':
    main()
