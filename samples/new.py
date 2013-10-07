from langner import build
import functions

input = '''
    (True)->(print("On the planet: "));
    (x)->(print(x));
    (x.age > 14, x.age < 20)->(new kid, kid.age=0);
    (x.age == 40) -> (delete x, print("Funeral"));
    (x)->(x.age = x.age + 1);
    (True)->(print("New year!"));
    '''

strat = build(input)

# Girls:
strat.add_to_gos({"name":"Eva", "age":16})

strat.run()
