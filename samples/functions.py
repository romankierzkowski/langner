from langner import build
from random import random

input = '''
    (True) -> (print(random()));
'''

strat = build(input, functions=[random])
strat.run()
