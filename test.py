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

    def check(self, code):
        parsed = parser.parse(code)
        self.assertEqual(code, str(parsed))

def main():
    unittest.main()

if __name__ == '__main__':
    main()
