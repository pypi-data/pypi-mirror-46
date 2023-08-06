from typing import Iterator, Callable


class DeferredIterator(Iterator):
    def __init__(self, func: Callable):
        self.func = func
        self._iterator = None

    @property
    def iterator(self):
        if self._iterator is None:
            self._iterator = iter(self.func())
        return self._iterator

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.iterator)
