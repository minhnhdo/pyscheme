## a subset of scheme

from __future__ import division

from parse import parse, parse_continuous, Tokenizer
from env import makeglobalenv, Env
from primitives import islist, isbool, isatom, isnumber

try:
    input = raw_input
except NameError:
    pass

def eval(sexp, env):
    if islist(sexp):
        op = sexp[0]
        if op == 'begin':
            for exp in sexp[1:-1]:
                eval(exp, env)
            return eval(sexp[-1], env)
        elif op == 'quote':
            return sexp[1]
        elif op == 'lambda':
            exps = sexp[2:]
            exps.insert(0, 'begin')
            return Lambda(env, sexp[1], exps)
        elif op == 'cond':
            for cond_exp in sexp[1:]:
                cond = cond_exp[0]
                exp = cond_exp[1:]
                if eval(cond, env):
                    exp.insert(0, 'begin')
                    return eval(exp, env)
        elif op == 'define':
            defn = eval(sexp[2], env)
            env.update({sexp[1]: defn})
            return defn
        elif op == 'and':
            for exp in sexp[1:]:
                if not eval(exp, env):
                    return False
            return True
        elif op == 'or':
            for exp in sexp[1:]:
                if eval(exp, env):
                    return True
            return False
        else: # apply
            op = eval(sexp[0], env)
            args = []
            for exp in sexp[1:]:
                args.append(eval(exp, env))
            return op(*args)
    elif sexp == '#t':
        return True
    elif sexp == '#f':
        return False
    elif isnumber(sexp):
        return sexp
    else:
        return env.find(sexp)

class Lambda:
    def __init__(self, env, arglist, sexp):
        self.arglist = arglist
        self.sexp = sexp
        self.outerenv = env
    def __repr__(self):
        return '<compound function at 0x%x>' % id(self)
    def __call__(self, *arg):
        if len(arg) != len(self.arglist):
            raise TypeError("Expected %d arguments (%d provided)" % (len(self.arglist), len(arg)))
        localenv = Env(self.outerenv)
        localenv.update(dict(zip(self.arglist, arg)))
        return eval(self.sexp, localenv)

def tostring(a):
    if islist(a):
        return '(' + ' '.join(map(str, a)) + ')'
    elif isbool(a):
        return '#t' if a else '#f'
    else:
        return str(a)

def REPL():
    globalenv = makeglobalenv()

    while True:
        try:
            inp = input('* ')
            while True:
                try:
                    sexp = parse(inp)
                    break
                except SyntaxError as e:
                    if e.msg == 'Unexpected end of token stream':
                        inp += ' ' + input('  ')
                    else:
                        raise e
            print(tostring(eval(sexp, globalenv)))
        except (KeyboardInterrupt, EOFError):
            print("Exiting... Bye!")
            return
        #except Exception as e:
        #    print(str(e))

if __name__ == '__main__':
    REPL()
