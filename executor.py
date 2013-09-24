from parser import build


input = '''
    (True) -> (print("Hello world!"));
'''

strat = build(input, {})
strat.run()

raw_input()

