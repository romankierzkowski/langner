from langner import build

input = '''
    (x) -> (print(x.foo + " " + x.foo.bar));
'''

strat = build(input)
strat.add_to_gos({})
strat.run()

