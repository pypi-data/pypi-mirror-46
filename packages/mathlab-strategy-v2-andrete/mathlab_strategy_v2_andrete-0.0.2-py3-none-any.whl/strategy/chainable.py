import itertools

try:
    import builtins
except ImportError:
    import __builtin__ as builtins


class Chainable(object):
    def __init__(self, data, method=None):
        self.data = data
        self.method = method

    def __getattr__(self, name):
        try:
            method = getattr(self.data, name)
        except AttributeError:
            try:
                method = getattr(builtins, name)
            except AttributeError:
                method = getattr(itertools, name)

        return Chainable(self.data, method)

    def __call__(self, *args, **kwargs):
        try:
            return Chainable(list(self.method(self.data, *args, **kwargs)))
        except TypeError:
            return Chainable(list(self.method(args[0], self.data, **kwargs)))
