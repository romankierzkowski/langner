from langner import build

input = '''
    (True || False, True) -> (print("Hello"), print("World"));
'''

strat = build(input)

strat.run()
