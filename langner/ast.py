from operator import *
from collections import MutableMapping
from itertools import product
from threading import *
import thread
import threading

class Object(MutableMapping):

    def __init__(self):
        self.fields = {}
        self.__deleted__  = False

    def __len__(self):
        return self.fields.__len__()

    def __iter__(self):
        return self.fields.__iter__()
    
    def __contains__(self, key):
        return key in self.fields

    def __getitem__(self, key):
        return self.fields.get(key, Object.UNDEF)

    def __setitem__(self, key, value):
        if value == Object.UNDEF:
            del self.fields[key]
        else:
            self.fields[key] = value

    def __delitem__(self, key):
        self.fields.remove(key)

    def values(self):
        return self.fields.values()

    def items(self):
        return self.fields.items()

    def __str__(self):
        return str(self.fields)

    def __getattr__(self, name):
        try:
            return self.fields[name]
        except KeyError:
            raise AttributeError

class ObjectWrapper(Object):

    def __init__(self, wrapped):
        self.wrapped = wrapped
        self.__deleted__  = False

    def __len__(self):
        return len(dir(self.wrapped))

    def __iter__(self):
        return iter(dir(self.wrapped))
    
    def __contains__(self, key):
        return hasattr(self.wrapped, key)

    def __getitem__(self, key):
        try:
            result = getattr(self.wrapped, key)
            if result is None:
                return Object.UNDEF
            else:
                return result
        except AttributeError:
            return Object.UNDEF

    def __setitem__(self, key, value):
        if value == Object.UNDEF:
            value = None   
        setattr(self.wrapped, key, value)

    def __delitem__(self, key):
        pass

    def values(self):
        return [ getattr(self.wrapped, name) for name in dir(self.wrapped) ]

    def items(self):
        return dir(self.wrapped)

    def __str__(self):
        return str(self.wrapped)

    def __getattr__(self, name):
        return getattr(self.wrapped, name)


class UndefException(Exception):

    def __str__(self):
        return "Cannot modify undefined!"

class Undef(Object):

    def __setitem__(self, key, value):
        raise UndefException()

    def __delitem__(self, key):
        raise UndefException()

    def dfs(self, callback):
        callback(self)

# Singleton for undefined:
Object.UNDEF = Undef()

#o = Object()

class Variable:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def evaluate(self, **context):
        return context[self.name] is not Object.UNDEF

    def execute(self, **context):
        return context[self.name] 

    def dfs(self, callback):
        callback(self)


class Selection:
    def __init__(self, variable, selection_path):
        self.variable = variable
        self.selection_path = selection_path

    def __str__(self):
        result = str(self.variable) 
        if self.selection_path:
            for r in self.selection_path:
                result += ".%s" % str(r)
        return result

    def is_strict(self):
        return self.selection_path is not None

    def assign(self, value, **context):
        cursor = self.variable.execute(**context)
        if self.selection_path:
            for name in self.selection_path[:-1]:
                cursor = cursor.get(name, None)
                # TODO: Error handling needed
                if not cursor:
                    tmp = Object()
                    cursor[name] = tmp
                    cursor = tmp
        cursor[self.selection_path[-1]] = value

    def execute(self, **context):
        result = self.variable.execute(**context)
        if self.selection_path:
            for name in self.selection_path:
                result = result[name]
        return result 

    def evaluate(self, **context):
        result = self.variable.execute(**context)
        if self.selection_path:
            for name in self.selection_path:
                result = result[name]
        return result

    def link(self, functions):
        pass

    @property
    def variables(self):
        return set([self.variable.name])

    def dfs(self, callback):
        callback(self)
        self.variable.dfs(callback)


class Event:
    def __init__(self, name, variables):
        self.name = name
        self.variables = variables or []

    def __str__(self):
        var_list = ""
        if self.variables: 
            for r in self.variables[:-1]:
                var_list += "%s, " % str(r)
            var_list += str(self.variables[-1])
        return "#%s(%s)" % (str(self.name), var_list)

    @property
    def variables(self):
        return set([x.name for x in self.variables])

    def dfs(self, callback):
        callback(self)
        for variable in self.variables:
            variable.dfs(callback)

    def evaluate(self, **context):
        return True

class Strategy(threading.Thread):

    def __init__(self, rules):
        threading.Thread.__init__(self)
        self.rules = rules
        self.gos = []
        self.events = []
        self.events_lock = Lock()


    def __str__(self):
        result = ""
        for r in self.rules:
            result += "%s;" % r
        return result

    def link(self, functions = None):
        self.linked = True
        if functions:
            f = dict(self._functions.items() + functions.items())
        else:
            f = self._functions
        for rule in self.rules:
            rule.link(f)

    def _trigger_event(self, name, *args):
        self.events.append((name, args))

    def run(self):
        self._run()

    def _run(self):
        cycle = 0
        while True:
            
            self.events_lock.acquire()
            triggered = list(self.events)
            del self.events[0:len(self.events)]
            self.events_lock.release()
            
            to_execute = []

            # EVALUATION:
            for rule in self.rules:
                events = rule.events()
                if events:
                    name, params_names = events[0]
                    filtered = [e for e in triggered if e[0] == name]
                    for _, values in filtered:
                        ev_context = dict(zip(params_names, values))
                        _, variables = rule.variables()
                        for values in product(self.gos, repeat = len(variables)):
                            context = dict(zip(variables, values))
                            context.update(ev_context)
                            if rule.evaluate(**context):
                                to_execute.append((context, rule))
                else:
                    _, variables = rule.variables()
                    for values in product(self.gos, repeat = len(variables)):
                        context = dict(zip(variables, values))
                        if rule.evaluate(**context):
                            to_execute.append((context, rule))
            
            # EXECUTION:
            to_gos = []
            for context, rule in to_execute:
                to_gos += rule.execute(**context)
            self.gos = self.gos + to_gos

            # REMOVAL:
            for item in self.gos:
                if item.__deleted__:
                    self.gos.remove(item)

    def _normalize(self, dictionary):
        for k, v in dictionary.iteritems():
            if v is not None:
                if isinstance(v, dict):
                    dictionary[k] = self._normalize(v)
                else:
                    dictionary[k] = v
        result = Object()
        result.fields = dictionary
        return result

    def add_to_gos(self, obj):
        if isinstance(obj, dict):
            self.gos.append(self._normalize(obj))
        elif isinstance(obj, Object):
            self.gos.append(obj)
        else:
            self.gos.append(ObjectWrapper(obj))

    def dfs(self, callback):
        callback(self)
        for rule in self.rules:
            rule.dfs(callback)
        

class Rule:

    def _comaseparate(self, input):
        output = ""
        for r in input[:-1]:
            output += "%s, " % str(r)
        output += str(input[-1])
        return output

    def __init__(self, conditions, actions):
        self.conditions = conditions
        self.actions = actions

    def __str__(self):
        conditions = self._comaseparate(self.conditions)
        actions = self._comaseparate(self.actions)
        return "(%s)->(%s)" % (conditions, actions)

    def variables(self):
        event_variables = set([])
        loose_variables = set([])
        first = True
        for condition in self.conditions:
            if isinstance(condition, Event):
                if first:
                    event_variables.union(condition.variables)
                    first = False
            else:
                loose_variables = loose_variables.union(condition.variables)
        return (event_variables, loose_variables)

    def events(self):
        result = []
        for condition in self.conditions:
            if isinstance(condition, Event):
                result.append((condition.name, [c.name for c in condition.variables]))
        return result

    def evaluate(self, **context):
        result = True
        for condition in self.conditions:
            result = result and condition.evaluate(**context)
        return result

    def execute(self, **context):
        output = []
        for action in self.actions:
            result = action.execute(**context)
            if result:
                name, obj = result
                context[name] = obj
                output.append(obj)
        return output

    def link(self, functions):
        for condition in self.conditions:
            condition.link(functions)
        for action in self.actions:
            action.link(functions)

    def dfs(self, callback):
        callback(self)
        for condition in self.conditions:
            condition.dfs(callback)
        for action in self.actions:
            action.dfs(callback)

class Condition:
    pass

class Operator(Condition):
    
    def _parenth(self, operand):
        if hasattr(operand, "priority") and operand.priority < self.priority:
            return "(%s)" % str(operand)
        else:
            return str(operand)  


class UnaryOperator(Operator):

    def __init__(self, operand):
        self.operand = operand

    def __str__(self):
        return "%s%s" % (self.operator, self._parenth(self.operand))

    def execute(self, **context):
        return self.operation(self.operand.execute(**context))

    def evaluate(self, **context):
        return self.operation(self.operand.evaluate(**context))

    @property
    def variables(self):
        return self.operand.variables

    def dfs(self, callback):
        callback(self)
        self.operand.dfs(callback)

class BinnaryOperator(Operator):
    
    def __init__(self, loperand, roperand):
        self.loperand = loperand
        self.roperand = roperand

    def __str__(self):
        return "%s %s %s" % (self._parenth(self.loperand), self.operator, self._parenth(self.roperand))

    def execute(self, **context):
        return self.operation(self.loperand.execute(**context), self.roperand.execute(**context))

    def evaluate(self, **context):
        return self.operation(self.loperand.evaluate(**context), self.roperand.evaluate(**context))

    @property
    def variables(self):
        return self.roperand.variables.union(self.loperand.variables)

    def dfs(self, callback):
        callback(self)
        self.loperand.dfs(callback)
        self.roperand.dfs(callback)

class Action:

    def link(self, functions):
        pass

class Assignment(Action):

    def __init__(self, selection, test):
        self.selection = selection
        self.test = test

    def __str__(self):
        return "%s = %s" % (str(self.selection), str(self.test))

    def link(self, functions):
        self.test.link(functions)

    def execute(self, **context):
        value = self.test.execute(**context)
        self.selection.assign(value, **context)

    def dfs(self, callback):
        callback(self)
        self.selection.dfs(callback)
        self.test.dfs(callback)

class New(Action):
    def __init__(self, variable):
        self.variable = variable

    def __str__(self):
        return "new %s" % str(self.variable)

    def execute(self, **context):
        return (self.variable.name, Object())

    def dfs(self, callback):
        callback(self)
        self.variable.dfs(callback)

class Delete(Action):
    def __init__(self, variable):
        self.variable = variable

    def __str__(self):
        return "delete %s" % str(self.variable)

    def execute(self, **context):
        context[self.variable.name].__deleted__ = True

    def dfs(self, callback):
        callback(self)
        self.variable.dfs(callback)

class Or(BinnaryOperator):
    operator = "||"
    priority = 0
    operation = or_

class And(BinnaryOperator):
    operator = "&&"
    priority =  1
    operation = and_

class Not(UnaryOperator):
    operator = "!"
    priority =  3
    operation = not_

class Comparison(BinnaryOperator):
    priority = 4

class LT(Comparison):
    operator = "<"
    operation = lt

class LE(Comparison):
    operator = "<="
    operation = le

class EQ(Comparison):
    operator = "=="
    operation = eq

class NE(Comparison):
    operator = "!="
    operation = ne

class GE(Comparison):
    operator = ">="
    operation = ge

class GT(Comparison):
    operator = ">"
    operation = gt

class BitOr(BinnaryOperator):
    operator = "|"
    priority = 5
    operation = or_

class BitXor(BinnaryOperator):
    operator = "^"
    priority = 6
    operation = xor

class BitAnd(BinnaryOperator):
    operator = "&"
    priority = 7
    operation = and_

class Shift(BinnaryOperator):
    priority = 8

class LeftShift(Shift):
    operator = "<<"
    operation = lshift

class RightShift(Shift):
    operator = ">>"
    operation = rshift

class Add(BinnaryOperator):
    operator = "+"
    priority = 9
    operation = add

class Substract(BinnaryOperator):
    operator = "-"
    priority = 9
    operation = sub

class Multiply(BinnaryOperator):
    operator = "*"
    priority = 10
    operation = mul

class Divide(BinnaryOperator):
    operator = "/"
    priority = 10
    operation = truediv

class Modulo(BinnaryOperator):
    operator = "%"
    priority = 10
    operation = mod

class FloorDivide(BinnaryOperator):
    operator = "//"
    priority = 10
    operation = floordiv

class Negation(UnaryOperator):
    operator = "-"
    priority = 12
    operation = neg

class Inversion(UnaryOperator):
    operator = "~"
    priority = 12
    operation = invert

class Power(BinnaryOperator):
    operator = "**"
    priority = 12
    operation = pow

class Literal:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

    def evaluate(self, **context):
        return self.value

    def execute(self, **context):
        return self.value

    @property
    def variables(self):
        return set()

    def dfs(self, callback):
        callback(self)

class StringLiteral(Literal):
    def __str__(self):
        result = list(repr(self.value))
        result[0] = result[-1] = '"'
        return "".join(result)

class BooleanLiteral(Literal):
    pass

class NumberLiteral(Literal):
    pass

class FunctionExecution(Condition, Action):

    def __init__(self, name, params):
        self.name = name
        self.params = params

    def __str__(self):
        param_list = ""
        if self.params != None: 
            for r in self.params[:-1]:
                param_list += "%s, " % str(r)
            param_list += str(self.params[-1])
        return "%s(%s)" % (str(self.name), param_list)

    def execute(self, **context):
        param_list = []
        for p in self.params:
            param_list.append(p.execute(**context))
        return self.impl(*param_list)

    @property
    def variables(self):
        result = set()
        for param in self.params:
            result = result.union(param.variables)
        return result

    def link(self, impl):
        self.impl = impl

    def dfs(self, callback):
        callback(self)
        for param in self.params:
            param.dfs(callback)
