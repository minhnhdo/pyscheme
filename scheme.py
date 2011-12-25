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
    Note: still a very rudimentary implementation, i.e. the identity function
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

def makeenv(outer=None):
    """
    Make an empty environment with the outer environment specified
    """

    retval = {'outer': outer}
    return retval

def addtoglobal(globalenv):
    globalenv.update({
        })
    return globalenv

globalenv = addtoglobal(makeenv())

def eval(sexp, env=globalenv):
    if islist(sexp):
        if sexp[0] == 'quit':
            raise KeyboardInterrupt
        elif sexp[0] == 'quote':
            return sexp[1]
        elif sexp[0] == '+':
            return sum(sexp[1:])
        elif sexp[0] == 'cond':
            for exp in sexp[1:]:
                if eval(exp[0], env):
                    return eval(exp[1], env)
        elif sexp[0] == '<':
            return eval(sexp[1], env) < eval(sexp[2], env)
        elif sexp[0] == '>':
            return eval(sexp[1], env) > eval(sexp[2], env)
        elif sexp[0] == '<=':
            return eval(sexp[1], env) <= eval(sexp[2], env)
        elif sexp[0] == '>=':
            return eval(sexp[1], env) >= eval(sexp[2], env)
        elif sexp[0] == 'lambda':
            pass
        else:
            op = find(sexp[0], globalenv)
            return op(*sexp[1:])
    elif isnumber(sexp):
        return sexp
    elif sexp == '#t':
        return True
    elif sexp == '#f':
        return False
    # isidentifier
    else:
        return find(sexp, env)

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
