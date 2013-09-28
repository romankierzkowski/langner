Langner
=====
What is Langer?
-----------------------
Langer is a programming **language for expressing strategies**. Enigmatic? Have you ever wondered to make an intelligent robot? (No? Really, not even once? Weirdo...) The robots are performing actions to accomplish their goals. They must adjust their behavior to things that happen. That's behavior strategy - the way the decisions on actions are made according to events that occur. Langner was created to describe it in convenient and readable form.


Why new language?
-----------------------
The generic answer would be: because the existing languages does not suit the need. Of course, there are well developed languages for reasoning. For example Prolog. But they work in question - answer mode, rather than action - reaction. 
Instead of .


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
