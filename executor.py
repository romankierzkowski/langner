from parser import build
from ast import Object, ObjectWrapper

input = '''
    (a) -> (new b);
    (a) -> (print(a)) 
    (True)->(print("--------------"))
'''


strat = build(input, {})

o = Object()
o.x = 0

strat.addToGos(o)

strat.run()