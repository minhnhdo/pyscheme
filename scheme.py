## a subset of scheme

# import itertools

# def tokenizer(s):
#     tokens = s.replace('(', ' ( ').replace(')', ' ) ').split()
#     for tok in tokens:
#         yield tok

class Tokenizer:
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
    next = __next__
    def __iter__(self):
        return self
    def rollback(self):
        self.counter -= 1
        return self

def parse_list(tokens):
    retval = []
    for tok in tokens:
        if tok == ')':
            return retval
        else:
            retval.append(parse_sexp(tokens.rollback()))
    raise SyntaxError("Unexpected end of token stream")

def parse_atom(token):
    return token
    

def parse_sexp(tokens):
    try:
        tok = next(tokens)
    except (StopIteration, IndexError):
        return

    if tok == '(':
        return parse_list(tokens)
    else:
        return parse_atom(tok)

read = input
isnumber = str.isdigit
isatom = str.isalpha

def islist(l):
    return isinstance(l, list)

def eval(sexp):
    if islist(sexp):
        l = []
        for exp in sexp:
            l.append(eval(exp))
        (op, *arg) = l
        return apply(op, arg)
    elif isnumber(sexp):
        return int(sexp)
    elif isatom(sexp):
        return sexp
    else:
        return sexp

def error(s):
    print('ERROR:', s)

def apply(op, arg):
    if op == '+':
        return sum(arg)