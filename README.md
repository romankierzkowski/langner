Langner
=======
**Disclaimer:** Langner is in **very alpha**. The criticism, ideas and forbearance are **highly appreciated**. If you have any question or remark feel free to share it on the [Langner forum](https://groups.google.com/forum/#!forum/langner).

What is Langer?
-----------------------
Langer is an **object oriented, rule based programming language**. Its interpreter is shipped as an **Python library**.  It was created to express behavior strategies. It has simple syntax based on languages like Python and C. It was designed to be convenient and readable for a programmer, but it can be easily used in [genetic programming](http://en.wikipedia.org/wiki/Genetic_programming) as well.  

Langner was created as an research language. It is **not general purpose**, but it is general enough that it might be useful in other areas as well. It is avilable under [MIT license](http://opensource.org/licenses/MIT).

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

strat = build(input)
strat.run()
```

The ouput:

```
Hello world!
Hello world!
Hello world!
...
```

Langner parser is avilable as a `build()` function in `langner` module. It takes code in a string. The **white space characters are ommited** when the input is parsed. Any formatting should be accepted. The functions returns the langner.ast.Strategy object. The Strategy extends `threading.Thread` class. It can be run by executing `start()` method, but in most of the examples we prefare just to execute `run()` method in the main thread. The program blocks until its  interrupted (CTRL+C). If there is no change in the code, the following examples will present only the `input` variable.

The Langner code is **list of rules separated with semicolons**. Each rule has two sections - **conditions and actions**. The rule has the following syntax:
```
(cond1, cond2, ..., condN) -> (action1, action2, ..., actionN);
```

The Langer **strategy is evaluted in an infinite loop**. If the condtions are true, the actions are executed. In the given example the condition is always true and the action executes embaded function `print()` that prints to the standard output. The strategy will greet the world for the infinity.

### Global Object Space ###

The key concept behind the Langner is the **Global Object Space (GOS)**. The rules are evaluate against objects in GOS.
```python
from langner import build

input = '''
    (x) -> (print(x.msg));
'''

strat = build(input)
strat.add_to_gos({"msg":"Hello"})
strat.add_to_gos({"msg":"World!"})

strat.run()
```

The output:
```
Hello
World!
Hello
World!
...
```

One was of getting objects to GOS is by adding them with `add_to_gos()` method. This method takes dictionaries that maps a field name to a field value.

When the variable appears in a condition you may read it as an **universal quantification**. In the given example we would read the rule as: 

*For each object x in GOS, print x.msg to the console.* 

Then each object in GOS is substituted under x. The variable condition is always true for each object in a GOS. Let's consider more complicated example:

```python
from langner import build

input = '''
    (x.ok) -> (print(x.msg));
'''

strat = build(input)

strat.add_to_gos({"ok":True, "msg":"Hello"})
strat.add_to_gos({"ok":False, "msg":"Goodbye"})
strat.add_to_gos({"ok":True, "msg":"World!"})

strat.run()
```

The following code will generate exactly the same output as previous example. The "Goodbye" message will not be printed. The rule can be read:

*For each object x in GOS that x.ok is true, print x.msg to the console.*

Although, the real world might be bit more complex than the next example let's face the truth about dating: 

```python
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

```
The output:
```
Kate dates John
Meg dates Ben
Sandy dates Alex
Kate dates John
Meg dates Ben
Sandy dates Alex
...
```

The following rule contains two variables. **The actions are executed only if, each condition in the rule is fullfilled.** In the given example the rule might be read:

*For each object x and for each object y, that x is a female and y is a male and x and y have the same score, print the copule to the console.*

### Creating and Removing Objects from GOS ###

The object can be added to GOS with `new <variable>` action and removed from GOS with `delete <variable>` action. After the object is created, it can be access via variable name in the subsequent actions.  

```python
from langner import build

input = '''
    (x) -> (print(x.value));
    (a.value > 0) -> (a.value = a.value - 1);
    (a.value == 0) -> (new b, b.value = 3, delete a);
'''

strat = build(input)
strat.add_to_gos({"value":3})

strat.run()
```
The output:
```
3
2
1
0
3
2
1
0
...
```

Every evaluation cycle the `value` field in the object is decreased by one. When the field is equal 0 then the object is removed form GOS and the new object is created and initialized with a `value` equal 3. In the example, there is always one object in the GOS.

### Undefined fields ###

Langner object is bit different then objects in Python. First, it **does not have the methods**. Second, **the field can be either number, string, boolean or other object**. There is **no null value** in Langer. The field either have value or is undefined. If not existing field is access `undef` is returned. You can assign `undef` to a field. It means that you undefine this field and it does not exist any longer. The `undef` has one more interesting property:  

```python
from langner import build

input = '''
    (x) -> (print(x.foo + " " + x.foo.bar));
'''

strat = build(input)
strat.add_to_gos({})
strat.run()
```

The output:
```
undef undef
undef undef
undef undef
...
```

If the unidefined field is accessed as an object it returns `undef` as well.

### Functions ###

You can **execute almost any function from Python in the context of Langner** providing you have passed it in the `build` function in `functions` parameter. You can **use functions both in actions and conditions**.  In the given example the standard `random` function is used:

```python
from langner import build
from random import random

input = '''
    (True) -> (print(random()));
'''

strat = build(input, functions=[random])
strat.run()
```

The output:
```
0.653709135292
0.475016218464
0.394916852958
0.132886618414
...
```

### Events ###

The events in Langer is a mechanism of an input. It is a way that external world can communicate with a strategy. Event is a kind of condition. This **condition is fullfiled when an event has been triggered**. The parameters of an event are available for other conditions and actions of the rule. To differenciate event from a function call, event name is preceaded with *# symbol*. To trigger an event, you have to execute method of a strategy, with a parameters you want to pass.

*Note:* There should be *only one event per rule*!

Let's consider [real life example](http://youtu.be/EtoMN_xi-AM):

```python
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
```

The output:
```
na na
na na
na na
na na
na na
na na
na na
na na
na na
Batman!
na na
na na
na na
...
```

In this example the strategy is started as a deamon. Once every 0.01 second event `show_message` is triggered. It passes "Batman" to the context of a rule.

### Operators ###

Langner use following operators (the precedence is exactly the same as in Python):

<table>
  <tr>
    <td>||</td><td>Or</td>
  </tr>
  <tr>
    <td>&&</td><td>And</td>
  </tr>
  <tr>
    <td>!</td><td>Logical Negation</td>
  </tr>
  <tr>
    <td>==, &lt;=, &gt;=, &lt;, &gt;</td><td>Comparison</td>
  </tr>
  <tr>
    <td>|</td><td>Bitwise Or</td>
  </tr>
  <tr>
    <td>^</td><td>Bitwise Xor</td>
  </tr>
  <tr>
    <td>&</td><td>Bitwise And</td>
  </tr>
  <tr>
    <td>&lt;&lt;</td><td>Shift Left</td>
  </tr>
  <tr>
    <td>&gt;&gt;</td><td>Shift Right</td>
  </tr>
  <tr>
    <td>+, -</td><td>Addition and Subtraction</td>
  </tr>
  <tr>
    <td>*, /, %, //</td><td>Multiplication, Division, Modulo, Floor Division</td>
  </tr>
  <tr>
    <td>-, ~</td><td>Arithmetic Negation, Bitwise Inversion</td>
  </tr>
  <tr>
    <td>**</td><td>Power</td>
  </tr>
  
</table>

### Execution Order ###



Why a new language?
-----------------------
For my research I needed a language that:

1. allows experssing behaviour strategy in a simple rule based fashion,
2. the strategy would be able to react to events from the environment,
3. the language should have a syntax that can be used in [genetic programming (GP)](http://en.wikipedia.org/wiki/Genetic_programming).

The procedural programming languages could match two first goals, but their syntax is too complicated for GP. There are well developed rule based languages - for example Prolog. They are intended to work in question and answer mode rather than continious flow that changes its directions on the events.
