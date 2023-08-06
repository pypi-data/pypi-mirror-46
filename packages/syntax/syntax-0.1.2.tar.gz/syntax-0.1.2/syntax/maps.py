from .extension_methods import *

class Pipeable:
    """
    Any callback that can be evaluated via piping.
    Can be negated to become a map
    Can be unchained with unary + (changes it into lambda)
    is, not is and such don't work
    Normal accessors should work perfectly
    """
    def __init__(self, callback):
        self._eval = callback
    
    def __ror__(self, other):
        return self._eval(other)

    def __neg__(self):
        return Pipeable(lambda x: [self._eval(x) for x in x])


class DelayedAccessor(Pipeable):
    """
    Creates delayed accessor
    Does not work for: &, |, ~, unary + and -
    
    """

    def __getattribute__(self, v):
        if v not in ["__ror__", "_eval", "__neg__", "__pos__", "__init__", "__add__", "_DelayedAccessor__extended_syntax"]:
            return DelayedAccessor(self.__extended_syntax(v))
        else:
            return super().__getattribute__(v)

    def __str__(self):
        return DelayedAccessor(lambda x: self._eval(x).__str__())

    def __pos__(self):
        return lambda x: x | self

    def __call__(self, *args):
        return DelayedAccessor(lambda x: self._eval(x)(*args))

    def __add__(self, other):
        return DelayedAccessor(lambda x: self._eval(x) + other)

    def __sub__(self, other):
        return DelayedAccessor(lambda x: self._eval(x) - other)

    def __mul__(self, other):
        return DelayedAccessor(lambda x: self._eval(x) * other)

    def __truediv__(self, other):
        return DelayedAccessor(lambda x: self._eval(x) / other)

    def __floordiv__(self, other):
        return DelayedAccessor(lambda x: self._eval(x) // other)

    def __pow__(self, other):
        return DelayedAccessor(lambda x: self._eval(x) ** other)

    def __lshift__(self, other):
        return DelayedAccessor(lambda x: self._eval(x) << other)

    def __rshift__(self, other):
        return DelayedAccessor(lambda x: self._eval(x) >> other)

    def __lt__(self, other):
        return DelayedAccessor(lambda x: self._eval(x) < other)

    def __le__(self, other):
        return DelayedAccessor(lambda x: self._eval(x) <= other)

    def __eq__(self, other):
        return DelayedAccessor(lambda x: self._eval(x) == other)

    def __ne__(self, other):
        return DelayedAccessor(lambda x: self._eval(x) != other)

    def __gt__(self, other):
        return DelayedAccessor(lambda x: self._eval(x) > other)

    def __ge__(self, other):
        return DelayedAccessor(lambda x: self._eval(x) >= other)

    def __radd__(self, other):
        return DelayedAccessor(lambda x: other + self._eval(x))

    def __rsub__(self, other):
        return DelayedAccessor(lambda x: other - self._eval(x))

    def __rmul__(self, other):
        return DelayedAccessor(lambda x: other * self._eval(x))

    def __rtruediv__(self, other):
        return DelayedAccessor(lambda x: other / self._eval(x))

    def __rfloordiv__(self, other):
        return DelayedAccessor(lambda x: other // self._eval(x))

    def __rpow__(self, other):
        return DelayedAccessor(lambda x: other ** self._eval(x))

    def __rlshift__(self, other):
        return DelayedAccessor(lambda x: other << self._eval(x))

    def __rrshift__(self, other):
        return DelayedAccessor(lambda x: other >> self._eval(x))

    def __rlt__(self, other):
        return DelayedAccessor(lambda x: other < self._eval(x))

    def __rle__(self, other):
        return DelayedAccessor(lambda x: other <= self._eval(x))

    def __req__(self, other):
        return DelayedAccessor(lambda x: other == self._eval(x))

    def __rne__(self, other):
        return DelayedAccessor(lambda x: other != self._eval(x))

    def __rgt__(self, other):
        return DelayedAccessor(lambda x: other > self._eval(x))

    def __rge__(self, other):
        return DelayedAccessor(lambda x: other >= self._eval(x))

    def __not__(self):
        return DelayedAccessor(lambda x: not self._eval(x))

    def __bool__(self):
        return DelayedAccessor(lambda x: bool(self._eval(x)))

    def __extended_syntax(self, v):
        default = lambda x: self._eval(x).__getattribute__(v)
        if v == "replace" and isinstance(v, list):
            return lambda *args: list_replace(x, *args)
        return default


it = DelayedAccessor(lambda x: x)
_ = it

