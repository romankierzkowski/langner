from parser import build
from ast import Object, ObjectWrapper
import sys

input = '''
    (#event()) -> (new x, x.a = 1);
    (#event(), x) -> (x.a = x.a + 1);
    (#remove(), x) -> (delete x);
    (x) -> (print(x.a));
'''


strat = build(input, {})
dir(strat)

# o = Object()
# o["x"] = 0

# strat.addToGos(o)

strat.run()

while True: 
	s = raw_input('--> ')
	if s == "rem":
		strat.remove()
	else:
		strat.event(s)