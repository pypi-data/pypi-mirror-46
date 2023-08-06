from functools import wraps


def is_chiter(cls, f) -> bool:
    if not hasattr(f, "__annotations__"):
        return False

    return_type = f.__annotations__.get("return", "")
    parts = str(return_type).split(".")
    return any((p for p in parts if p.startswith(cls.__name__)))


def to_chiter(*, copy_length_hint=False):
    def wrapper(func):
        @wraps(func)
        def inner(self, *args, **kwargs):
            cls = type(self)
            result = func(self, *args, **kwargs)

            if result is NotImplemented or hasattr(result, "__wrapped__") and is_chiter(cls, result.__wrapped__):
                return result

            chiter = cls(result)
            if copy_length_hint:
                chiter._length_hint = self._length_hint

            return chiter

        return inner

    return wrapper
