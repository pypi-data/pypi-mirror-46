class BadArgument(TypeError):
    def __init__(self, fun, number, got, expected):
        TypeError.__init__(self, "Bad arg %d to %s: got '%s', expected '%s'." % (number, fun, got.__name__, expected.__name__,))

def check_arg(fun, nr, arg, typ):
    if not isinstance(arg, typ):
        raise BadArgument(fun, nr, type(arg), typ)
