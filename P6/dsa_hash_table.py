from itertools import count, takewhile
from math import ceil, sqrt
from typing import Any

import numpy


__all__ = [
    'DSAHashTable'
]


def _is_prime(x: int) -> bool:
    res = True
    for i in takewhile(lambda _: res, range(3, ceil(sqrt(x)))):
        if x % i == 0:
            res = False
    return res


class DSAHashTable:
    class _Entry:
        NEVER_USED = 0
        PREV_USED = 1
        USED = 2

        def __init__(self) -> None:
            self.state = self.NEVER_USED
            self.key = None
            self.value = None

        def __repr__(self) -> str:
            if self.state == self.USED:
                res = f"{self.key}, {self.value}"
            elif self.state == self.NEVER_USED:
                res = "NEVER_USED"
            elif self.state == self.PREV_USED:
                res = "PREV_USED"
            return res

    MAX_LOAD_FACTOR = 0.5
    MIN_GROWTH = 10

    def __init__(self, size: int) -> None:
        self._array = numpy.empty(size, dtype=numpy.object)
        for i in range(self.capacity):
            self._array[i] = self._Entry()
        self._used = 0

    def put(self, key: str, value: Any) -> None:
        self._put(self._array, key, value)
        self._used += 1

        if self.load_factor >= self.MAX_LOAD_FACTOR:
            self._grow_array()

    def get(self, key: str) -> Any:
        idx = DSAHashTable._hash(key) % self.capacity
        original_idx = idx
        found = False
        while not found:
            entry = self._array[idx]
            if entry.state == self._Entry.USED and entry.key == key:
                res = entry.value
                found = True
            else:
                if entry.state in (self._Entry.USED, self._Entry.PREV_USED):
                    idx = (idx + 1) % self.capacity
                if entry.state == self._Entry.NEVER_USED or idx == original_idx:
                    raise KeyError(f"Key `{key}` not in hash table.")
        return res

    def has(self, key: str) -> bool:
        try:
            _ = self.get(key)
            res = True
        except KeyError:
            res = False
        return res

    @property
    def load_factor(self) -> float:
        return self._used / self.capacity

    @property
    def capacity(self) -> int:
        return self._array.size

    def _grow_array(self) -> None:
        new_size = next(filter(_is_prime, count(self.capacity + self.MIN_GROWTH)))
        new_array = numpy.empty(new_size, dtype=numpy.object)
        for i in range(new_size):
            new_array[i] = self._Entry()
        for entry in self._array:
            if entry.state == self._Entry.USED:
                self._put(new_array, entry.key, entry.value)
        self._array = new_array

    @staticmethod
    def _hash(key: str) -> int:
        res = 0
        for c in key:
            res = 33 * res + ord(c)
        return res

    @staticmethod
    def _put(array: numpy.ndarray, key: str, value: Any) -> None:
        idx = DSAHashTable._hash(key) % array.size
        # Assumes array never becomes 100% full.
        while array[idx].state == DSAHashTable._Entry.USED:
            idx = (idx + 1) % array.size
        array[idx].key = key
        array[idx].value = value
        array[idx].state = DSAHashTable._Entry.USED
