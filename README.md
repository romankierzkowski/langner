Langner
=======
**Disclaimer:** Langner is in **very alpha**. The criticism, ideas and forbearance are **highly appreciated**. If you have any question or remark feel free to share it on the [Langner forum](https://groups.google.com/forum/#!forum/langner).

What is Langer?
-----------------------
Langer is an **object oriented, rule based programming language**. Its interpreter is shipped as an **Python library**.  It was created to express behavior strategies. It has simple syntax based on languages like Python and C. It was designed to be convenient and readable for a programmer, that it can be easily used in [genetic programming](http://en.wikipedia.org/wiki/Genetic_programming). 

Langner was created as an research language. It is **not general purpose**, but it is general enough that it might be useful in other areas. 

Where can I get it?
-----------------------
The easiest option is via Python package manager:
```bash
 $ pip install langner
```

Getting Started Guide
-----------------------
### 'Hello world' in Langer? ###

```python
from langner import build

input = '''
    (True) -> (print("Hello world!"));
'''

strat = build(input, {})
strat.run()
```

As you can see in the snipet 


To build an Langner code use library

```
Hello world!
Hello world!
Hello world!
...
```

Why a new language?
-----------------------
For my research I needed a language that:

1. allows experssing behaviour strategy in a simple rule based fashion (if x is true, do y),
2. the strategy would be able to react to events from the environment (if z happend, do v),
3. the language should have a syntax that can be used in [genetic programming (GP)](http://en.wikipedia.org/wiki/Genetic_programming) (still easily readable for a human).

The procedural programming languages could match two first goals, but their syntax is to complicated for GP. There are well developed rule based languages - for example Prolog. They are intended to work in question and answer mode rather than continious flow that changes its directions on the events.
