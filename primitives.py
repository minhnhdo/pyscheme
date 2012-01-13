def islist(a):
    return isinstance(a, list)

def isnumber(a):
    return isinstance(a, (int, float))

def isatom(a):
    return isinstance(a, str)

def isbool(a):
    return isinstance(a, bool)
