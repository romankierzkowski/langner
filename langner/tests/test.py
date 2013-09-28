import unittest
from langner.parser import parser
from langner.ast import Object

class SyntaxTests(unittest.TestCase):

    def testEmpty(self):
        self.check("")

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
        self.check_modified('(x + +y)->(new y);', '(x + y)->(new y);')
        self.check('(x + -y)->(new y);')
        self.check_modified('(x ** -y ** +-z)->(new y);', '(x ** -y ** -z)->(new y);')

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
    
    def testAtoms(self):
        self.check('(x.a == 2)->(x.a = x + y);')
        self.check('(x.a == x.b)->(x.a = x + y);')
        self.check('(x.a == "abc")->(x.a = x + y);')
        self.check('("abc")->(x.a = x + y);')
        self.check('(1.23)->(x.a = x + y);')
        self.check('(True)->(x.a = x + y);')
        self.check('(False)->(x.a = x + y);')

    def check(self, code):
        parsed = parser.parse(code)
        self.assertEqual(code, str(parsed))

    def check_modified(self, code, output):
        parsed = parser.parse(code)
        self.assertEqual(output, str(parsed))

    # Evaluation:

    def testEvaluate(self):
        self.evaluate("True", True)
        self.evaluate("!True", False)
        self.evaluate("1 == 1", True)
        self.evaluate("1 == 2", False)
        self.evaluate('"a" == "b"', False)
        self.evaluate('"a" == "a"', True)
        self.evaluate('1 + 2 * 6 - 3', 10)
        self.evaluate('2 + 2 == 5', False)
        self.evaluate('2 ** 4 + 1', 17)
        self.evaluate('"a" + "b"',"ab")
        self.evaluate('x + y', 4, context={"x":2,"y":2})
        self.evaluate('x.y + y', 4, context={"x":{"x":2,"y":2},"y":2})
        # self.evaluate("True and True", False)
        # self.evaluate("True and True", False)
        pass 

    def evaluate(self, condition, expected, **kwargs):
        context = kwargs.get("context", {})
        rule = "(%s)->(new x);" % condition
        strategy = parser.parse(rule);
        result = strategy.rules[0].conditions[0].evaluate(**context)
        self.assertEqual(result, expected)

    # Variables

    def testVariables(self):
        self.variables("x", [], ['x'])
        self.variables("x, y", [], ['x', 'y'])
        self.variables("x, y", [], ['x', 'y'])
        self.variables("x, y, foo(a,b)", [], ['x', 'y', 'a', 'b'])
        self.variables("x, y, foo(a.foo, b > y)", [], ['x', 'y', 'a', 'b'])


    def variables(self, condition, event_vars, loose_vars):
        rule = "(%s)->(new x);" % condition
        strategy = parser.parse(rule);
        result = strategy.rules[0].variables()
        self.assertEqual(result, (set(event_vars), set(loose_vars)))

    # Object:

    def testObject(self):
        o = Object()
        o["a"] = 1
        o["b"] = 3
        self.assertEqual(len(o), 2)
        self.assertEqual("a" in o, True)
        self.assertEqual("c" in o, False)
        self.assertTrue(iter(o))
        self.assertTrue(o["a"], 1)
        self.assertTrue(o["b"], 3)
        self.assertEqual(o["c"], Object.UNDEF)
        self.assertEqual(o.items(), [("a", 1), ("b", 3)])
        self.assertEqual(o.values(), [1, 3])

def main():
    unittest.main()

if __name__ == '__main__':
    main()
