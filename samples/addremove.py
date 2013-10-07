from langner import build

input = '''
    (x) -> (print(x.value));
    (a.value > 0) -> (a.value = a.value - 1);
    (a.value == 0) -> (new b, b.value = 3, delete a);
'''

strat = build(input)
strat.add_to_gos({"value":3})

strat.run()
