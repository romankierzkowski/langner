from operator import *

class Variable:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def evaluate(self, context):
        return context[self.name]

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
        return selection_path != None

    def evaluate(self, context):
        result = self.variable.evaluate(context)
        if self.selection_path:
            for name in self.selection_path:
                result = result[name]
        return result

    def variables(self):
        return set([self.variable.name])

class Event:
    def __init__(self, name, variables):
        self.name = name
        self.variables = variables

    def __str__(self):
        var_list = ""
        if self.variables != None: 
            for r in self.variables[:-1]:
                var_list += "%s, " % str(r)
            var_list += str(self.variables[-1])
        return "#%s(%s)" % (str(self.name), var_list)

    def variable(self):
        return set([x.name for x in self.variables])

class Strategy:
    def __init__(self, rules):
        self.rules = rules

    def __str__(self):
        result = ""
        for r in self.rules:
            result += "%s;" % r
        return result


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
        event_variables = set()
        loose_variables = set()
        first = True
        for condition in self.conditions:
            if isinstance(condition, Event):
                if first:
                    event.union(condition.variables())
                    first = False
            else:
                loose_variables = loose_variables.union(condition.variables())
                return (event_variables, loose_variables)

class Test:
    pass

class Operator(Test):
    
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

    def evaluate(self, context):
        return self.operation(self.operand.evaluate(context))

    def variables(self):
        return self.operand.variables()

class BinnaryOperator(Operator):
    
    def __init__(self, loperand, roperand):
        self.loperand = loperand
        self.roperand = roperand

    def __str__(self):
        return "%s %s %s" % (self._parenth(self.loperand), self.operator, self._parenth(self.roperand))

    def evaluate(self, context):
        return self.operation(self.loperand.evaluate(context), self.roperand.evaluate(context))

    def variables(self):
        return self.roperand.variables().union(self.loperand.variables())

class Assignment:

    def __init__(self, selection, test):
        self.selection = selection
        self.test = test

    def __str__(self):
        return "%s = %s" % (str(self.selection), str(self.test))

class New:
    def __init__(self, variable):
        self.variable = variable

    def __str__(self):
        return "new %s" % str(self.variable)

class Delete:
    def __init__(self, variable):
        self.variable = variable

    def __str__(self):
        return "delete %s" % str(self.variable)

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

class Literal(Test):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

    def evaluate(self, context):
        return self.value

    def variables(self):
        return set()

class StringLiteral(Literal):
    def __str__(self):
        result = list(repr(self.value))
        result[0] = result[-1] = '"'
        return "".join(result)

class BooleanLiteral(Literal):
    pass

class NumberLiteral(Literal):
    pass

class FunctionExecution(Test):

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