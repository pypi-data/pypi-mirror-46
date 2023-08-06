import copy as _copy
import os as _os
import pickle as _pickle
from collections import UserDict as _UserDict


class PersistentState(_UserDict):
    def __init__(self, path):
        self.path = path
        if _os.path.isfile(path):
            with open(path, "rb") as f:
                self.data = _pickle.load(f)
        else:
            self.data = {}

    def copy(self):
        raise ValueError("Cannot create a new instance of PersistentState at the same path")

    def __getitem__(self, k):
        return self.data[k]

    def __setitem__(self, k, v):
        # ensure that v is pickleable
        self.data[k] = v
        with open(self.path, "wb") as f:
            _pickle.dump(self.data, f)

    def __delitem__(self, k):
        del self.data[k]

    def __contains__(self, what):
        return self.data.__contains__(what)

    def __iter__(self):
        return self.data.__iter__()


def zdict(*args):
    return dict(zip(*args))

def lrange(arg):
    return range(len(arg))

def timer(timed):
    """@timeit but logs instead of printing"""
    def timer_wrapper(*args, **kwargs):
        start_time = time.time()
        timed(*args, **kwargs)
        end_time = time.time() - start_time
        logger.info('%s done in %s seconds', timed.__name__, round(end_time, 2))
    return timer_wrapper


class Frame(_UserDict):
    """
    For interpreter development - frame for function call and so on
    """
    def __init__(self, parent=None):
        self.parent = parent
        self.data = data

    def setv(self, k, v):
        while self.parent is not None:
            self = self.parent
        self.data[k] = v

    def new_frame(self):
        return Frame(self)

    def copy(self):
        return _copy.copy(self)

    def __getitem__(self, k):
        if k in self.data.keys():
            return self.data[k]
        if self.parent is not None:
            return self.parent[k]
        raise KeyError("No such item as {}".format(k))

    def __setitem__(self, k, v):
        self.data[k] = v

    def __delitem__(self, k):
        del self.data[k]

    def __contains__(self, what):
        return self.data.__contains__(what)

    def __iter__(self):
        return self.data.__iter__()
