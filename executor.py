from parser import build
from ast import Object, ObjectWrapper

input = '''
    (a) -> (print(a));
	(a.x == 0) -> (new b, b.x = 0);
	(a) -> (a.x = a.x + 1);
	(a.x == 4) -> (delete a);
    (True)->(print("--------------"));
'''


strat = build(input, {})

o = Object()
o["x"] = 0

strat.addToGos(o)

strat.run()