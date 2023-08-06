from functools import wraps


def with_types(*types):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for tp, arg in zip(types, args):
                if not isinstance(arg, tp):
                    raise TypeError
            return fn(*args, **kwargs)
        return wrapper
    return decorator
