from langner import build
from time import sleep

input = '''
    (True) -> (print("na na"));
    (#show_message(msg)) -> (print(msg));
'''

strat = build(input)

strat.daemon = True
strat.start() # It starts strategy as a separate thread.

while(True):
    strat.show_message("Batman!")
    sleep(0.01)


