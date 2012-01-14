class TokenStreamError(Exception):
    """
    Token stream error
    """

class Tokenizer:
    """
    Turn a string into a list of tokens
    Have the ability to rollback using the rollback instance method
    """
    def __init__(self, s):
        # separating open and close parens
        s = s.replace('(', ' ( ').replace(')', ' ) ')
        # separating quotes
        s = s.replace("'", " ' ")

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
        if tok == '(':
            return parse_list(tokens)
        elif tok == "'":
            retval = ['quote']
            retval.append(parse_sexp(tokens))
            return retval
        elif tok == ')':
            raise TokenStreamError('Unexpected )')
        else:
            return parse_atom(tok)
    except (StopIteration, IndexError):
        raise SyntaxError('Unexpected end of token stream')

def parse(s):
    """
    Tokenize then parse
    """
    return parse_sexp(Tokenizer(s))
