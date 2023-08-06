"""
list | G[:, ...] (getter)   (one capital letter programs...)
"""

from .anon import new as _new
from .maps import Pipeable as _Pipeable

def _getter(x, index, try_=False):
    """
    For indexer in tuple:
        if it's : (None) - then copy all of them
    """
    try:
        return x[index]
    except Exception:
        """
        TODO: handle special case of index being singular value, not a tuple

        :, 1
        [[0,1], [2,3]] - select :
        [[0,1], [2,3]] - select 1 on the first level
        [1, 3]

        :, 1, :
        [[[1, 2], [3, 4]], [[5, 6], [7, 8]]] - select :
        [[3, 4], [7, 8]] - select 1 on first level
        [[3, 4], [7, 8]] - copy all on this level

        Composition of maps where mapping func is a getter
        """
        map_indices = []
        base = current = []
        for level, i in enumerate(index):
            if isinstance(i, slice):
                callback = map(lambda x: x[i], current)
            else:
                x[i]
        return current

def _g_func(_, index):
    return _Pipeable(lambda x: _getter(x, index, try_=False))

def _try_g_func(_, index):
    return _Pipeable(lambda x: _getter(x, index, try_=True))
        
G = _new(__getitem__=_g_func, Try=_new(__getitem__=_try_g_func))

def G_test():
    assert ([[0, 1], [2, 3]] | G[:, 1]) == [1, 3]
    assert ([[0, 1], [2, 3]] | G[1, :]) == [2, 3]
    assert ([[0, 1], [2, 3]] | G[1, 1]) == 3
    assert ([[0, 1], [2, 3]] | G[:, :]) == [[0, 1], [2, 3]]
