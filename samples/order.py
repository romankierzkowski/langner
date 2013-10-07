from langner import build

input = '''
    (o("A"), o("B")) -> (o("C"), o("D"));
    (o("F"), o("G")) -> (o("G"), o("H"));
    (True)->(print("-----------------"));
'''

def o(v):
    print v
    return True

strat = build(input, functions=[o])
strat.run()
