# Sourced from my Data Structures & Algorithms practical worksheet 6 submission,
# with modifications.

from .array import Array

from itertools import count, takewhile
from math import ceil, floor, sqrt
from typing import Generic, Hashable, Iterator, Optional, Tuple, TypeVar


__all__ = [
    "HashTable"
]


K = TypeVar("K", bound=Hashable)
V = TypeVar("V")


class HashTable(Generic[K, V]):
    class _Entry(Generic[K, V]):
        NEVER_USED = 0
        PREV_USED = 1
        USED = 2

        def __init__(self, key: Optional[K] = None, value: Optional[V] = None,
                     state: int = NEVER_USED) -> None:
            self.state = state
            self.key = key
            self.value = value

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

    # On delete(), load factors <= this amount trigger the capacity to be reduced.
    # Should be in the range [0, 1].
    MIN_LOAD_FACTOR = 0.1
    # On put(), load factors >= this amount trigger the capacity to be increased.
    # Should be in the range [0, 1].
    MAX_LOAD_FACTOR = 0.7
    # Minimum fraction decrease in capacity when a capacity reduction is triggered.
    # (Unless the resulting capacity would be too small to fit all key, value pairs.)
    MIN_SHRINK = 0.1
    # Minimum fraction increase in capacity when a capacity increase is triggered.
    MIN_GROWTH = 0.5

    # Initialises the hashtable with the given starting capacity.
    # capacity must be >= 1.
    def __init__(self, capacity: int) -> None:
        if capacity < 1:
            raise ValueError(f"capacity must be >=1, got {capacity}.")
        capacity = self._next_prime(ceil(capacity / self.MAX_LOAD_FACTOR))
        self._array = Array(capacity)
        for i in range(self.capacity):
            self._array[i] = self._Entry()
        self._used = 0

    # The ratio of key, value pairs currently stored to the capacity.
    @property
    def load_factor(self) -> float:
        assert self.capacity > 0
        return len(self) / self.capacity

    # The maximum number of key, value pairs able to be stored in the hash table currently.
    # Note: this amount automatically adjusts as the table grows and shrinks.
    @property
    def capacity(self) -> int:
        return len(self._array)

    # Returns an iterator of all key, value pairs.
    def items(self) -> Iterator[Tuple[K, V]]:
        return map(lambda entry: (entry.key, entry.value),
                   filter(lambda entry: entry.state == self._Entry.USED,
                          self._array))

    # The number of key, value pairs currently stored.
    def __len__(self) -> int:
        return self._used

    # Gets the value with the given key, or raises KeyError if there is no such key.
    def __getitem__(self, key: K) -> V:
        return self._get(key).value

    # Adds the key, value pair to the hashtable, or if the key already exists, updates the value.
    def __setitem__(self, key: K, value: V) -> None:
        self._put(key, value)
        # MAX_LOAD_FACTOR > 1 would prevent capacity increases, allowing load factor to reach 1, which will break things.
        assert self.MAX_LOAD_FACTOR <= 1.0
        if self.load_factor >= self.MAX_LOAD_FACTOR:
            self._increase_capacity()

    # Deletes the key, value pair with the given key, or raises KeyError if there is no such key.
    def __delitem__(self, key: K) -> None:
        entry = self._get(key)
        entry.state = self._Entry.PREV_USED
        self._used -= 1
        if self.load_factor <= self.MIN_LOAD_FACTOR:
            self._decrease_capacity()

    def __contains__(self, key: K) -> bool:
        try:
            _ = self[key]
        except KeyError:
            res = False
        else:
            res = True
        return res

    # Iterates the keys stored.
    def __iter__(self) -> Iterator[K]:
        return map(lambda entry: entry.key,
                   filter(lambda entry: entry.state == self._Entry.USED,
                          self._array))

    # Inserts a key, value pair into the array, or updates an existing key's value.
    # If the key is new, increments _used.
    # The array must have at least one free entry.
    def _put(self, key: K, value: V) -> None:
        # Algorithm assumes array never becomes 100% full.
        assert len(self) < self.capacity
        idx = self._hash(key, self.capacity)
        step = self._step_hash(key, self.capacity)
        done = False
        while not done:
            entry = self._array[idx]
            free = entry.state != self._Entry.USED
            if free or entry.key == key:
                if free:
                    entry.key = key
                    entry.state = self._Entry.USED
                    self._used += 1
                entry.value = value
                done = True
            else:
                idx = (idx + step) % self.capacity

    # Gets the entry object with the given key, or raises KeyError if there is no such key.
    def _get(self, key: K) -> _Entry[K, V]:
        idx = self._hash(key, self.capacity)
        step = self._step_hash(key, self.capacity)
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

    # Increases the capacity by at least the amount specified by MIN_GROWTH.
    # New capacity is a prime number.
    def _increase_capacity(self) -> None:
        assert self.capacity > 0
        assert self.MIN_GROWTH > 0
        new_capacity = ceil(self.capacity * (1.0 + self.MIN_GROWTH))
        new_capacity = self._next_prime(new_capacity)
        self._set_capacity(new_capacity)

    # Decreases the capacity by the amount specified by MIN_SHRINK, if possible.
    # New capacity is a prime number.
    def _decrease_capacity(self) -> None:
        assert 0 <= self.MIN_SHRINK < 1
        new_capacity = floor(self.capacity * (1.0 - self.MIN_SHRINK))
        new_capacity = self._prev_prime(new_capacity)
        min_capacity = len(self) + 1
        if new_capacity < min_capacity:
            new_capacity = self._next_prime(min_capacity)
        # Possible that the new capacity ends up greater than the old due to distribution of primes and whatnot.
        if new_capacity < self.capacity:
            self._set_capacity(new_capacity)

    # Resizes the current array and rehashes all key, value pairs back into it.
    # new_size must be >= the number of key, value pairs stored.
    def _set_capacity(self, new_capacity: int) -> None:
        assert new_capacity >= len(self)
        old_array = self._array
        self._array = Array(new_capacity)
        self._used = 0
        for i in range(new_capacity):
            self._array[i] = self._Entry()
        for entry in old_array:
            if entry.state == self._Entry.USED:
                self._put(entry.key, entry.value)

    @staticmethod
    def _hash(key: Hashable, array_size: int) -> int:
        # Note! Looks like it uses Python in-built hash function, but actually calls key.__hash__(),
        # which I manually implement for the types I'll be using with this HashTable class.
        return hash(key) % array_size

    @staticmethod
    def _step_hash(key: Hashable, array_size: int) -> int:
        # I don't think this really matters too much.
        return max(1, (33 * abs(hash(key))) % array_size)

    # Returns the smallest prime larger than x.
    # For x < 2, returns 2.
    @staticmethod
    def _next_prime(x: int) -> int:
        if x < 2:
            res = 2
        else:
            x += 1
            if x % 2 == 0:
                x += 1
            res = next(filter(HashTable._is_prime, count(x, 2)))
        return res

    # Returns the largest prime smaller than x.
    # However for x < 2, returns 2.
    @staticmethod
    def _prev_prime(x: int) -> int:
        if x <= 3:
            res = 2
        else:
            x -= 1
            if x % 2 == 0:
                x -= 1
            res = next(filter(HashTable._is_prime, count(x, -2)))
        return res

    # Checks if x is a prime number.
    # For efficiency, only defined for x > 2.
    @staticmethod
    def _is_prime(x: int) -> bool:
        assert x > 2
        res = True
        for i in takewhile(lambda _: res, range(2, 1 + ceil(sqrt(x)))):
            res = x % i != 0
        return res
