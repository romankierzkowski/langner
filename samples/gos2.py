from langner import build

input = '''
    (x.ok) -> (print(x.msg));
'''

strat = build(input)

strat.add_to_gos({"ok":True, "msg":"Hello"})
strat.add_to_gos({"ok":False, "msg":"Goodbye"})
strat.add_to_gos({"ok":True, "msg":"World!"})

strat.run()
