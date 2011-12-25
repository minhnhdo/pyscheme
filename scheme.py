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

read = functools.partial(input, '>>>')
isnumber = str.isdigit
isatom = str.isalpha

def number(sexp):
    return int(sexp)

def primitiveadd(*arg):
    retval = 0
    try:
        for i in arg:
            retval += i
        return retval
    except TypeError:
        retval += arg
        return retval

def islist(l):
    return isinstance(l, list)

def eval(sexp, env):
    if islist(sexp):
        l = []
        for exp in sexp:
            l.append(eval(exp, env))
        (op, *arg) = l
        return op(*arg)
        #return apply(op, arg, env)
    elif isnumber(sexp):
        return number(sexp)
    # isidentifier
    else:
        return find(sexp, env)

def error(s):
    print('ERROR:', s)

def makeenv(outer=None):
    """
    Make an empty environment with the outer environment specified
    """

    retval = {'outer': outer}
    return retval

def addtoglobal(globalenv):
    globalenv.update({
        '#t': True,
        '#f': False,
        '+': primitiveadd,
        'atom?': isatom
        })
    return globalenv

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
        return None

def REPL():
    while True:
        try:
            eval(read())
        except (KeyboardInterrupt, EOFError):
            print("Exiting... Bye!")

globalenv = addtoglobal(makeenv())

if __name__ == '__main__':
    REPL()
