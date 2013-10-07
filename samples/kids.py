from langner import build
import functions

input = '''
    (
        x.sex=="f", y.sex=="m",
        x.dad != y, y.mom != x
    ) -> (
        new kid,
            kid.sex=sex(),
            kid.name=name(kid.sex, x.name, y.name),
            kid.mom=x,
            kid.dad=y,
            print(x.name + " " + y.name + " are having kid " + kid.name + ".")
    );
    (True)->(print("-------"));
'''

def sex():
    return functions.choice(["f","m"])

def name(sex, mom, dad):
    if "f" == sex:
        return mom + " Jr."
    return dad + " Jr."

strat = build(input, functions={"sex":sex, "name":name})

# Girls:
strat.add_to_gos({"name":"Kate", "sex":"f"})
strat.add_to_gos({"name":"Meg", "sex":"f"})
strat.add_to_gos({"name":"Sandy", "sex":"f"})

# Boys:
strat.add_to_gos({"name":"John", "sex":"m"})
strat.add_to_gos({"name":"Ben", "sex":"m"})
strat.add_to_gos({"name":"Alex", "sex":"m"})

strat.run()
