import inspect

def typecheck(obj, t):
    """Private function for type checking"""
    if isinstance(obj, t):
        return True
    if type(t) in (tuple, list):
        if any([isinstance(obj, x) for x in t]):
            return True
    return False

def require(template, value, prune=False):
    """
    Compare types of struct and prune them if necessary
    """
    for key, typ in template.items():
        v = value.get(key)
        if not isinstance(v, typ):
            raise AssertionError("{} is not of type {}".format(key, typ))
    if prune:
        return {k: value[k] for k in template.keys()}
    return value


def constructor(init):
    """
    Set all parameters from the __init__ as in every normal
    object oriented type of constructor..., omit selfs
    """
    def __init__(self, *args, **kwargs):
        spec = inspect.getfullargspec(init)
        settings = dict(zip(spec.args, args))
        if spec.varargs is not None:
            settings[spec.varargs] = args[len(spec.args):]
        else:
            if len(spec.args) < len(args):
                keys = spec.kwonlyargs[:len(args) - len(spec.args)]
                settings.update(dict(zip(keys, args[len(spec.args):])))
        settings.update(kwargs)
        settings.update({k:v for k, v in zip(reversed(spec.args), reversed(spec.defaults)) if k not in settings})
        settings.update({k:v for k, v in spec.kwonlydefaults.items() if k not in settings})
        for k, v in settings.items():
            self.__setattr__(k, v)
        init(*args, **kwargs)
    return __init__

def typed(*signature, **kwargs_signature):
    """
    Ensure that the function call is typed, to avoid pointless crashes
    after long computation
    """
	# TODO: add for BoundMethods and ClassMethods
    signature = list(signature)
    def decorator(function):
        """
        Decorator that adds typechecking to the function or method
        """
        unbounded = inspect.getfullargspec(function).args[len(signature):]
        for k in unbounded:
            if k in kwargs_signature.keys():
                signature.append(kwargs_signature.pop(k))
            else:
                signature.append(object)
        def wrapped(*args, **kwargs):
            for ix, (i, t) in enumerate(zip(args, signature)):
                if not typecheck(i, t):
                    raise TypeError("Argument nr {} has incorrect type".format(ix + 1))
            for k, v in zip(kwargs.items()):
                try:
                    assert typecheck(v, kwargs_signature[k])
                except KeyError:
                    raise TypeError("Keyword argument {} is not permitted".format(k))
            return function(*args, **kwargs)
        return wrapped
    return decorator



class decorator(object):
    # TODO
    
    def __getattribute__(self, name):
        if name == '__class__':
            # calling type(decorator()) will return <type 'function'>
            # this is used to trick the inspect module >:)
            return types.FunctionType
        return super(decorator, self).__getattribute__(name)

    def __init__(self, fn):
        # let's pretend for just a second that this class
        # is actually a function. Explicity copying the attributes
        # allows for stacked decorators.
        self.__call__ = fn.__call__
        self.__closure__ = fn.__closure__
        self.__code__ = fn.__code__
        self.__doc__ = fn.__doc__
        self.__name__ = fn.__name__
        self.__defaults__ = fn.__defaults__
        self.func_defaults = fn.func_defaults
        self.func_closure = fn.func_closure
        self.func_code = fn.func_code
        self.func_dict = fn.func_dict
        self.func_doc = fn.func_doc
        self.func_globals = fn.func_globals
        self.func_name = fn.func_name
        # any attributes that need to be added should be added
        # *after* converting the class to a function
        self.args = None
        self.kwargs = None
        self.result = None
        self.function = fn
        self.__curry__ = True

    def __call__(self, *args, **kwargs):
        if self.__curry__:
            pass
    		# will analyze for all _ values in the args//kwargs and return curried function then
        self.args = args
        self.kwargs = kwargs

        self.before_call()
        self.result = self.function(*args, **kwargs)
        self.after_call()

        return self.result

    def before_call(self):
        pass

    def after_call(self):
        pass

    def __ror__(self):
        pass


class Show:
    def __str__(self):
        return "\n".join(["{}: {}".format(k, v) for k, v in dict(vars(self)).items() if not k.startswith("_")])

    def __repr__(self):
        return "\n".join(["{}: {}".format(k, v) for k, v in dict(vars(self)).items() if not k.startswith("_")])

    def __format__(self):
        return "\n".join(["{}: {}".format(k, v) for k, v in dict(vars(self)).items() if not k.startswith("_")])

    class Meta(type):
        def __str__(cls):
            return "\n".join(["{}: {}".format(k, v) for k, v in dict(vars(cls)).items() if not k.startswith("_")])
    
        def __repr__(cls):
            return "\n".join(["{}: {}".format(k, v) for k, v in dict(vars(cls)).items() if not k.startswith("_")])
    
        def __format__(cls):
            return "\n".join(["{}: {}".format(k, v) for k, v in dict(vars(cls)).items() if not k.startswith("_")])
