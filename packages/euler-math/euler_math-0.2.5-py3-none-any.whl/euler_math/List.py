import builtins as __builtin__
import functools as _functools


class List:

    def __init__(self, f):
        self.function = f

    def __rrshift__(self, other):
        return self.function(other)

    def __call__(self, *args, **kwargs):
        return List(lambda x: self.function(x, *args, **kwargs))


# list methods ------------------------------------


@List
def sum(list):
    return __builtin__.sum(list)


@List
def sumBy(list, f):
    return __builtin__.sum(map(f, list))


@List
def filter(list, f):
    return [x for x in list if f(x)]


@List
def map(list, f):
    return [f(x) for x in list]


@List
def max(list):
    return __builtin__.max(list)


@List
def reduce(list, f):
    return _functools.reduce(f, list)


@List
def collect(list, f):

    def gen():
        for s in map(f, list):
            for x in s:
                yield x

    return [x for x in gen()]
