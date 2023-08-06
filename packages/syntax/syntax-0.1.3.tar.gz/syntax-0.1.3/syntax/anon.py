import types

def new(*args, **kwargs):
    """
    Create anonymous object with given keyword arguments. Automatically binds all functions
    as bound methods. Non-keyword arguments serve as base classes. Constructors are not run!
    """

    class AnonymousClass(*args):
        def __repr__(self):
            return "<AnonymousClass> {}".format(self.__dict__)

    for k, v in kwargs.items():
        if k.startswith("__") and k.endswith("__"):
            setattr(AnonymousClass, k, v)
    obj = AnonymousClass()
    for k, v in kwargs.items():
        if not (k.startswith("__") and k.endswith("__")):
            if isinstance(v, types.FunctionType):
                setattr(obj, k, types.MethodType(v, obj))
            else:
                setattr(obj, k, v)
    return obj
