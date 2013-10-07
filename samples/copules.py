from langner import build

input = '''
    (x.sex=="f", y.sex=="m", x.score == y.score) -> (print(x.name + " dates " + y.name));
'''

strat = build(input)

# Girls:
strat.add_to_gos({"name":"Kate", "sex":"f", "score":3})
strat.add_to_gos({"name":"Meg", "sex":"f", "score":7})
strat.add_to_gos({"name":"Sandy", "sex":"f", "score":10})

# Boys:
strat.add_to_gos({"name":"John", "sex":"m", "score":3})
strat.add_to_gos({"name":"Ben", "sex":"m", "score":7})
strat.add_to_gos({"name":"Alex", "sex":"m", "score":10})

strat.run()
