Langner
=====
What is Langer?
-----------------------
What intialized by @romankierzkowski 

'Hello world' in Langer?
------------------------

```python
from parser import build

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
