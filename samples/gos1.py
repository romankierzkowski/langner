from langner import build

input = '''
    (x) -> (print(x.msg));
'''

strat = build(input)
strat.add_to_gos({"msg":"Hello"})
strat.add_to_gos({"msg":"World!"})

strat.run()
