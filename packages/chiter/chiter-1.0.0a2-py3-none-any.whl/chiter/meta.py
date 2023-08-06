from abc import ABCMeta

from .helpers import is_chiter, to_chiter


class ChIterMeta(ABCMeta):
    def __new__(mcs, name, bases, defaults):
        cls = super().__new__(mcs, name, bases, defaults)
        iterables = {k: v for k, v in defaults.items() if is_chiter(cls, v)}

        for name, f in iterables.items():
            setattr(cls, name, to_chiter(copy_length_hint=False)(f))
        return cls
