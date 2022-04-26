#internal cache of locally-computed properties

def lazy(f):

    def wrapper(*args, **kwargs):

        o = args[0]

        if "_lazy" not in o.__dict__:
            o.__dict__["_lazy"] = {}

        s = f"{f.__name__}_{str(args)}_{str(kwargs)}"

        if s not in o.__dict__["_lazy"]:
            o.__dict__["_lazy"][s]=f(*args, **kwargs)

        return o.__dict__["_lazy"][s]

    wrapper.__name__ = f.__name__
    return wrapper