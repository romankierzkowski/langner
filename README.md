Langner
=====
What is Langer?
-----------------------
**Disclaimer:** Langner is in **very alpha**. The criticism, ideas and forbearance are highly appreciated.

Langer is an **object oriented, rule based programming language**. Its interpreter is shipped as an **Python library**.  It was created to express behavior strategies. It has simple syntax based on languages like Python and C. It was designed to be convenient and readable for a programmer, plus it can be easily used in [genetic programming](http://en.wikipedia.org/wiki/Genetic_programming). 

Langner was created as an research language. It is not general purpose language, but it is general enough that it might be useful in other areas.

Where can I get it?
-----------------------
The easiest option is via Python package manager:
```bash
 $ pip install langner
```

Why a new language?
-----------------------
For my research I needed a language that:
1. Allows expressing behaviour strategies in simple rule based fashion.
2. The strategy would be able to react to events from the environment.
3. The language should have a syntax that can be used in [genetic programming (GP)](http://en.wikipedia.org/wiki/Genetic_programming) (still easily readable for a human).

The procedural programming languages could match two first goals, but their syntax is not very compatible. There are languages like Prolog. I like the a

Of course, there are well developed languages for reasoning. For example Prolog. But they work in question - answer mode, rather than action - reaction. 
Instead of .

What Langer is not?
-----------------------



'Hello world' in Langer?
------------------------

```python
from langner import build

input = '''
    (True) -> (print("Hello world!"));
'''

strat = build(input, {})
strat.run()
```

```
Hello world!
Hello world!
Hello world!
...
```
