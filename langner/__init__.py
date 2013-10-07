from parser import parser
from ast import FunctionExecution, Event

# Standard functions:
def _print(x):
    print x

def linker(functions):
    def link(node):
        if isinstance(node, FunctionExecution):
            node.link(functions[node.name])
    return link

import types

def triggers_creator_factory(strategy):
    def triggers_creator(node):
        if isinstance(node, Event):
            def trigger(self, *args):
                self._trigger_event(node.name, *args)
            setattr(strategy, node.name, types.MethodType(trigger, strategy))
    return triggers_creator


def build(code, functions = {}):
    if not isinstance(functions, dict):
        functions = dict([(f.__name__, f) for f in functions])
    strategy = parser.parse(code)
    standard = { "print": _print }
    strategy.dfs(linker(dict(standard.items() + functions.items())))
    strategy.dfs(triggers_creator_factory(strategy))
    return strategy