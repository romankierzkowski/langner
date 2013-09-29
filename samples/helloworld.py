from langner import build

input = '''
    (True) -> (print("Hello world!"));
'''

strat = build(input)
strat.run()

