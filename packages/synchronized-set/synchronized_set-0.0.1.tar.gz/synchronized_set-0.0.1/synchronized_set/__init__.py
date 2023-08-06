"""
Signatures taken from setobject.h:
https://github.com/python/cpython/blob/e42b705188271da108de42b55d9344642170aa2b/Include/setobject.h
https://github.com/python/cpython/blob/e42b705188271da108de42b55d9344642170aa2b/Objects/setobject.c
"""
from threading import Lock, get_ident
import logging
from typing import TypeVar, Generic, Iterable, Set

T = TypeVar('T')


class SynchronizedSet(set, Generic[T]):

    class synchronize:
        _logger = logging.getLogger('SynchronizedSet.synchronize')
        def __call__(self, func):  # noqa: E301
            def inner(outerself, *args):
                if not outerself._synchronized:
                    return func(outerself, *args)
                else:
                    self._logger.debug(f'Thread-{hex(get_ident())} -  locking SynchronizedSet@{hex(id(outerself))}')
                    with outerself._lock:
                        self._logger.debug(f'Thread-{hex(get_ident())} -   locked SynchronizedSet@{hex(id(outerself))}')
                        r = func(outerself, *args)
                    self._logger.debug(f'Thread-{hex(get_ident())} - unlocked SynchronizedSet@{hex(id(outerself))}')
                    return r
            return inner

    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(cls, 'SynchronizedSetType'):
    #         cls.SynchronizedSetType = TypeVar('SynchronizedSetType', bound=cls.__class__)
    #     return super().__new__(*args, **kwargs)

    def __init__(self, s: Iterable[T], synchronized: bool = True):
        self._synchronized = synchronized
        if self._synchronized:
            self._lock = Lock()
        super().__init__(s)

    @synchronize()
    def add(self, t: T):
        """
        Add an element to a set.
        This has no effect if the element is already present.
        """
        return super().add(t)

    @synchronize()
    def clear(self):
        """
        Remove all elements from this set.
        """
        return super().clear()

    @synchronize()
    def copy(self) -> Set[T]:
        """
        Return a shallow copy of a set.
        """
        return self.__class__(super().copy(), synchronized=self._synchronized)

    @synchronize()
    def difference(self, *ts: Iterable[T]) -> Set[T]:
        """
        Return the difference of two or more sets as a new set.
        (i.e. all elements that are in this set but not the others.)
        """
        return super().difference(*ts)

    @synchronize()
    def difference_update(self, *ts: Iterable[T]):
        """
        Remove all elements of another set from this set.
        """
        return super().difference_update(*ts)

    @synchronize()
    def discard(self, t: T):
        """
        Remove an element from a set if it is a member.
        If the element is not a member, do nothing.
        """
        return super().discard(t)

    @synchronize()
    def intersection(self, *s: Iterable[T]) -> Set[T]:
        """
        Return the intersection of two sets as a new set.
        (i.e. all elements that are in both sets.)
        """
        return super().intersection(*s)

    @synchronize()
    def intersection_update(self, *s: Iterable[T]):
        """
        Update a set with the intersection of itself and another.
        """
        return super().intersection_update(*s)

    @synchronize()
    def isdisjoint(self, ts: Iterable[T]) -> bool:
        return super().isdisjoint(ts)

    @synchronize()
    def issubset(self, ts: Iterable[T]) -> bool:
        """
        Report whether another set contains this set.
        """
        return super().issubset(ts)

    @synchronize()
    def issuperset(self, ts: Iterable[T]) -> bool:
        """
        Report whether this set contains another set.
        """
        return super().issuperset(ts)

    @synchronize()
    def pop(self) -> T:
        """
        Remove and return an arbitrary set element.
        Raises KeyError if the set is empty.
        """
        return super().pop()

    @synchronize()
    def remove(self, t: T):
        """
        Remove an element from a set; it must be a member.
        If the element is not a member, raise a KeyError
        """
        return super().remove(t)

    @synchronize()
    def symmetric_difference(self, ts: Iterable[T]) -> Set[T]:
        """
        Return the symmetric difference of two sets as a new set.
        (i.e. all elements that are in exactly one of the sets.)
        """
        return self.__class__(super().symmetric_difference(ts), synchronized=self._synchronized)

    @synchronize()
    def symmetric_difference_update(self, ts: Iterable[T]):
        """
        Update a set with the symmetric difference of itself and another.
        """
        return super().symmetric_difference_update(ts)

    @synchronize()
    def union(self, *ts: Iterable[T]) -> Set[T]:
        """
        Return the union of sets as a new set.
        (i.e. all elements that are in either set.)
        """
        return self.__class__(super().union(*ts), synchronized=self._synchronized)

    @synchronize()
    def update(self, *ts: Iterable[T]):
        """
        Update a set with the union of itself and others.
        """
        return super().update(*ts)
