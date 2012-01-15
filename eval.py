## a subset of scheme

from env import Env
from primitives import islist, isnumber

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
