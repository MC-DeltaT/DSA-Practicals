from itertools import count, takewhile
from math import ceil, sqrt
from typing import Any

import numpy


__all__ = [
    'DSAHashTable'
]


class DSAHashTable:
    class _Entry:
        NEVER_USED = 0
        PREV_USED = 1
        USED = 2

        def __init__(self) -> None:
            self.state = self.NEVER_USED
            self.key = None
            self.value = None

        # For debugging purposes only.
        def __repr__(self) -> str:
            if self.state == self.USED:
                res = f"{self.key}, {self.value}"
            elif self.state == self.NEVER_USED:
                res = "NEVER_USED"
            elif self.state == self.PREV_USED:
                res = "PREV_USED"
            else:
                raise AssertionError(f"Didn't expect state `{self.state}`.")
            return res

    MAX_LOAD_FACTOR = 0.5
    MIN_GROWTH = 20

    def __init__(self, capacity: int) -> None:
        if capacity < 1:
            raise ValueError(f"capacity must be >=1, got {capacity}.")
        capacity = self._next_prime(capacity)
        self._array = numpy.empty(capacity, dtype=numpy.object)
        for i in range(self.capacity):
            self._array[i] = self._Entry()
        self._used = 0

    def put(self, key: str, value: Any) -> None:
        self._put(self._array, key, value)
        self._used += 1
        if self.load_factor >= self.MAX_LOAD_FACTOR:
            self._grow_array()

    def get(self, key: str) -> Any:
        return self._get(key).value

    def delete(self, key: str) -> None:
        entry = self._get(key)
        entry.state = self._Entry.PREV_USED
        self._used -= 1

    def has(self, key: str) -> bool:
        try:
            _ = self.get(key)
            res = True
        except KeyError:
            res = False
        return res

    @property
    def size(self) -> int:
        return self._used

    @property
    def load_factor(self) -> float:
        return self.size / self.capacity

    @property
    def capacity(self) -> int:
        return self._array.size

    def _get(self, key: str) -> _Entry:
        idx = self._hash(key, self.capacity)
        step = DSAHashTable._step_hash(key, self.capacity)
        original_idx = idx
        found = False
        while not found:
            entry = self._array[idx]
            if entry.state == self._Entry.USED and entry.key == key:
                res = entry
                found = True
            else:
                if entry.state in (self._Entry.USED, self._Entry.PREV_USED):
                    idx = (idx + step) % self.capacity
                if entry.state == self._Entry.NEVER_USED or idx == original_idx:
                    raise KeyError(f"Key `{key}` not in hash table.")
        return res

    def _grow_array(self) -> None:
        new_size = self._next_prime(self.capacity + self.MIN_GROWTH)
        new_array = numpy.empty(new_size, dtype=numpy.object)
        for i in range(new_size):
            new_array[i] = self._Entry()
        for entry in self._array:
            if entry.state == self._Entry.USED:
                self._put(new_array, entry.key, entry.value)
        self._array = new_array

    @staticmethod
    def _put(array: numpy.ndarray, key: str, value: Any) -> None:
        idx = DSAHashTable._hash(key, array.size)
        step = DSAHashTable._step_hash(key, array.size)
        # Assumes array never becomes 100% full.
        done = False
        while not done:
            entry = array[idx]
            free = entry.state != DSAHashTable._Entry.USED
            if free or entry.key == key:
                if free:
                    entry.key = key
                    entry.state = DSAHashTable._Entry.USED
                entry.value = value
                done = True
            else:
                idx = (idx + step) % array.size

    @staticmethod
    def _hash(key: str, array_size: int) -> int:
        res = 0
        for c in key:
            res = 33 * res + ord(c)
        return res % array_size

    @staticmethod
    def _step_hash(key: str, array_size: int) -> int:
        return max(1, (sum(map(ord, key)) + len(key)) % array_size)

    @staticmethod
    def _next_prime(x: int) -> int:
        def _is_prime(x: int) -> bool:
            assert x > 2
            res = True
            for i in takewhile(lambda _: res, range(2, 1 + ceil(sqrt(x)))):
                if x % i == 0:
                    res = False
            return res

        assert x >= 1
        if x == 1:
            res = 2
        else:
            x += 1
            if x % 2 == 0:
                x += 1
            res = next(filter(_is_prime, count(x, 2)))
        return res
