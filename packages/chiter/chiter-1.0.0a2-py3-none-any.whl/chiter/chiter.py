from __future__ import annotations

import itertools
import operator
from functools import reduce
from typing import Any, Callable, Optional, Iterable, Iterator, Set, FrozenSet, List, Tuple, Dict

from .deferred_iterator import DeferredIterator
from .helpers import to_chiter
from .meta import ChIterMeta


class ChIter(Iterator[Any], metaclass=ChIterMeta):
    __slots__ = ("_iterable", "_length_hint")

    @classmethod
    def from_iterables(cls, *iterables) -> ChIter:
        obj = cls(itertools.chain(*iterables))
        obj._length_hint = sum(map(operator.length_hint, iterables))
        return obj

    def __init__(self, iterable: Iterable):
        self._length_hint = operator.length_hint(iterable)
        self._iterable = iter(iterable)

    def __iter__(self) -> Iterator:
        return self

    def __next__(self) -> Any:
        if self._length_hint:
            self._length_hint -= 1
        return next(self._iterable)

    def __add__(self, other) -> ChIter:
        if not hasattr(other, "__iter__"):
            return NotImplemented
        return type(self).from_iterables(self, other)

    def __radd__(self, other) -> ChIter:
        if not hasattr(other, "__iter__"):
            return NotImplemented
        return type(self).from_iterables(other, self)

    def __length_hint__(self) -> int:
        return self._length_hint

    def filter(self, func: Optional[Callable]) -> ChIter:
        return filter(func, self)

    @to_chiter(copy_length_hint=True)
    def map(self, func: Callable) -> ChIter:
        return map(func, self)

    @to_chiter(copy_length_hint=True)
    def enumerate(self, start: int = 0) -> ChIter:
        return enumerate(self, start=start)

    def zip(self) -> ChIter:
        return zip(*self)

    def reduce(self, function: Callable, initial=None) -> Any:
        args = (i for i in (self, initial) if i is not None)
        return reduce(function, *args)

    @to_chiter(copy_length_hint=True)
    def sorted(self, key: Optional[Callable] = None, reverse: bool = False) -> ChIter:
        return DeferredIterator(lambda: sorted(self, key=key, reverse=reverse))

    @to_chiter(copy_length_hint=True)
    def reversed(self) -> ChIter:
        return DeferredIterator(lambda: reversed(tuple(self)))

    def sum(self, start=0) -> int:
        return sum(self, start)

    def all(self) -> bool:
        return all(self)

    def any(self) -> bool:
        return any(self)

    def set(self) -> Set[Any]:
        return set(self)

    def frozenset(self) -> FrozenSet[Any]:
        return frozenset(self)

    def list(self) -> List[Any]:
        return list(self)

    def tuple(self) -> Tuple[Any]:
        return tuple(self)

    def dict(self) -> Dict[Any, Any]:
        return dict(self)

    def accumulate(self, func=operator.add) -> ChIter:
        return itertools.accumulate(self, func)

    def combinations(self, r: int) -> ChIter:
        return itertools.combinations(self, r)

    def combinations_with_replacement(self, r: int) -> ChIter:
        return itertools.combinations_with_replacement(self, r)

    def compress(self, selectors: Iterable[bool]) -> ChIter:
        return itertools.compress(self, selectors)

    def dropwhile(self, predicate: Callable) -> ChIter:
        return itertools.dropwhile(predicate, self)

    def groupby(self, key: Optional[Callable] = None) -> ChIter:
        return itertools.groupby(self, key=key)

    def filterfalse(self, predicate: Callable) -> ChIter:
        return itertools.filterfalse(predicate, self)

    def slice(self, start: int, stop: Optional[int] = None, step: Optional[int] = None) -> ChIter:
        args = (start, stop, step)
        start_is_stop = all((i is None for i in args[1:]))
        slice_args = args[:1] if start_is_stop else args
        return itertools.islice(self, *slice_args)

    def permutations(self, r: Optional[int] = None) -> ChIter:
        return itertools.permutations(self, r)

    def product(self, *, repeat=1) -> ChIter:
        return itertools.product(self, repeat=repeat)

    def takewhile(self, func=Callable) -> ChIter:
        return itertools.takewhile(func, self)

    @to_chiter(copy_length_hint=True)
    def starmap(self, func: Callable) -> ChIter:
        return itertools.starmap(func, self)

    def tee(self, n: int = 2) -> ChIter:
        return map(type(self), itertools.tee(self, n))

    def cycle(self) -> ChIter:
        return itertools.cycle(self)

    @to_chiter(copy_length_hint=True)
    def zip_longest(self, *, fillvalue=None) -> ChIter:
        return itertools.zip_longest(*self, fillvalue=fillvalue)

    def flat(self) -> ChIter:
        return itertools.chain.from_iterable(self)
