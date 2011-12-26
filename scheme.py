## a subset of scheme

# import itertools

# def tokenizer(s):
#     tokens = s.replace('(', ' ( ').replace(')', ' ) ').split()
#     for tok in tokens:
#         yield tok

import functools

class Tokenizer:
    """
    Turn a string into a list of tokens
    Have the ability to rollback using the rollback instance method
    """
    def __init__(self, s):
        # separating open and close parens
        s = s.replace('(', ' ( ').replace(')', ' ) ')

        self.tokens = s.split()
        self.counter = 0

    def __next__(self):
        self.counter += 1
        try:
            return self.tokens[self.counter - 1]
        except IndexError:
            raise StopIteration

    # for compatibility
    next = __next__

    def __iter__(self):
        return self

    def rollback(self):
        """
        Rollback one token
        """
        self.counter -= 1
        return self

def parse_list(tokens):
    """
    Input: a stream of tokens that contains the content of a list
    Output: a list representing that Scheme list
    Exceptions: when reaching the end of token stream, raise SyntaxError since the close parens token is missing
    """

    retval = []
    for tok in tokens:
        if tok == ')':
            return retval
        else:
            retval.append(parse_sexp(tokens.rollback()))
    raise SyntaxError("Unexpected end of token stream")

def parse_atom(token):
    """
    Input: a token
    Output: an represented atom

    Try to turn the token into a number, else just return it
    """
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return token
    return token
    

def parse_sexp(tokens):
    """
    Input: a stream of tokens
    Output: an atom if first of stream represents a token
            a list if first of stream represents a list
    """

    try:
        tok = next(tokens)
    except (StopIteration, IndexError):
        return

    if tok == '(':
        return parse_list(tokens)
    else:
        return parse_atom(tok)

def read():
    inp = input('* ')
    return parse_sexp(Tokenizer(inp))

def isatom(a):
    if isinstance(a, int):
        return True
    else:
        return not isinstance(a, float)

def isnumber(a):
    return isinstance(a, int) or isinstance(a, float)

def islist(l):
    return isinstance(l, list)

def primitivequit():
    raise KeyboardInterrupt

def primitiveadd(*args):
    return sum(args)

def primitivemult(*args):
    retval = 1
    for i in args:
        retval *= i
    return retval

def primitivediff(*args):
    length = len(args)
    if length < 1:
        raise TypeError("Expected at least 1 arguments ({0} provided)".format(len(args)))
    # inversion
    elif length == 1:
        return -args[0]

    retval = args[0]
    for i in args[1:]:
        retval -= i
    return retval

def primitivediv(*args):
    if len(args) < 1:
        raise TypeError("Expected at least 1 arguments ({0} provided)".format(len(args)))
    retval = args[0]
    for i in args[1:]:
        retval /= i
    return retval

def makeenv(outer=None):
    """
    Make an empty environment with the outer environment specified
    """

    retval = {'outer': outer}
    return retval

def addtoglobal(globalenv):
    globalenv.update({
        'quit': primitivequit,
        '+': primitiveadd,
        '*': primitivemult,
        '-': primitivediff,
        '/': primitivediv
        })
    return globalenv

globalenv = addtoglobal(makeenv())

def apply(sexp, env=globalenv):
    op = eval(sexp[0], env)
    args = []
    for exp in sexp[1:]:
        args.append(eval(exp, env))
    return op(*args)

def eval(sexp, env=globalenv):
    if islist(sexp):
        if sexp[0] == 'lambda':
            exps = sexp[2:]
            exps.insert(0, 'begin')
            return Lambda(env, sexp[1], exps)
        elif sexp[0] == 'begin':
            for exp in sexp[1:-1]:
                eval(exp, env)
                return eval(sexp[-1], env)
        elif sexp[0] == 'quote':
            return sexp[1]
        else:
            return apply(sexp, env)
    elif isnumber(sexp):
        return sexp
    elif sexp == '#t':
        return True
    elif sexp == '#f':
        return False
    else:
        return find(sexp, env)

class Lambda:
    def __init__(self, env, arglist, sexp):
        self.arglist = arglist
        self.sexp = sexp
        self.env = env
    def __call__(self, *arg, **kwarg):
        if len(arg) != len(self.arglist):
            raise TypeError("Expected {0} arguments ({1} provided)".format(len(self.arglist), len(arg)))
        localenv = makeenv(self.env)
        localenv.update(dict(zip(self.arglist, arg)))
        return eval(self.sexp, localenv)

def error(s):
    print('ERROR:', s)

def find(sym, env):
    """
    Find a symbol in env
    If symbol not in env or any of its outer, return None
    """

    try:
        if sym in env:
            return env[sym]
        else:
            return find(sym, env['outer'])
    except TypeError:
        # once hit here, sym is nowhere to be found
        raise NameError("Undefined atom {0!r}".format(sym))

def REPL():
    try:
        while True:
            #try:
                print(eval(read()))
            #except NameError as e:
            #    print('{0}: {1}'.format(e.__class__, str(e)))
    except (KeyboardInterrupt, EOFError):
        print("Exiting... Bye!")

if __name__ == '__main__':
    REPL()
