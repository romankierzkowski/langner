from langner import build

input = '''
    (True || False) -> (print(1+2*3));
'''

strat = build(input)
strat.add_to_gos({"msg":"Hello"})
strat.add_to_gos({"msg":"World!"})

strat.run()
