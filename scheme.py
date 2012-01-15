## a subset of scheme

from parse import parse, Tokenizer
from env import makeglobalenv
from primitives import islist, isbool
from eval import eval

try:
    input = raw_input
except NameError:
    pass

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
        except Exception as e:
            print(str(e))

if __name__ == '__main__':
    REPL()
