import math, operator
from functools import reduce

from primitives import islist, isbool, isatom, isnumber

class Env(dict):
    def __init__(self, outer=None):
        """
        Make an empty environment with the outer environment specified
        """

        self['outer'] = outer

    def find(self, sym):
        """
        Find a symbol in env
        If symbol not in env or any of its outer, return None
        """

        try:
            return self[sym]
        except KeyError:
            try: return self['outer'].find(sym)
            except AttributeError:
                # once hit here, sym is nowhere to be found
                raise NameError("Undefined atom {0!r}".format(sym))

def addtoglobal(env):
    def primitivequit():
        raise KeyboardInterrupt

    env.update(vars(math))

    env.update({
        'quit': primitivequit,
        '+': lambda *args: sum(args),
        '*': lambda *args: reduce(lambda x, y: x * y, args, 1),
        '-': lambda *args: -args[0] if len(args) == 0 else args[0] - sum(args[1:]),
        '/': lambda *args: reduce(lambda x, y: x / y, args[1:], args[0]),
        '<': operator.lt,
        '>': operator.gt,
        '=': operator.eq,
        'eq?': operator.is_,
        'zero?': lambda x: x == 0,
        'null?': lambda x: x == [],
        'atom?': isatom,
        'number?': isnumber,
        'list?': islist,
        'not': lambda x: not x,
        'cons': lambda x, l: [x] + l,
        'car': lambda l: l[0],
        'cdr': lambda l: l[1:],
        'map': lambda *args: list(map(*args)),
        'reduce': reduce,
        'filter': lambda *args: list(filter(*args)),
        'else': True
        })
    return env

globalenv = addtoglobal(Env())
